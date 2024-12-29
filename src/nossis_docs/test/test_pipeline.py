# nossis-docs, serverless hosting for static, private web sites that
# works like GitHub Pages
#
# Copyright (C) 2024  Matthew X. Economou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

import json
from unittest.mock import patch

import pytest
from aws_lambda_powertools.utilities.data_classes import CodePipelineJobEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.client import BaseClient
from mypy_boto3_cloudfront.type_defs import CreateDistributionResultTypeDef


@pytest.mark.smoke
def test_invalidate_distribution(
    distribution: CreateDistributionResultTypeDef,
) -> None:
    """Simulate a CodePipeline deploy stage signaling Lambda to
    invalidate paths in a CloudFront distribution.

    :param distribution: A mock CloudFront distribution.

    """

    # To ensure AWS test fixtures get set up BEFORE creating any boto3
    # clients, import the code to be tested at the function level
    # (i.e., here), not at the module level (above).  Otherwise, those
    # boto3 clients may not use the test fixtures and could
    # potentially alter real AWS infrastructure.
    from nossis_docs.pipeline import invalidate_distribution

    # https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-Lambda.html#action-reference-Lambda-event
    event = CodePipelineJobEvent(
        {
            "CodePipeline.job": {
                "id": (job_id := "11111111-abcd-1111-abcd-111111abcdef"),
                "accountId": "111111111111",
                "data": {
                    "actionConfiguration": {
                        "configuration": {
                            "FunctionName": "MyLambdaFunction",
                            "UserParameters": json.dumps(
                                {
                                    "distribution_id": distribution["Distribution"][
                                        "Id"
                                    ],
                                    "object_paths": ["/test-project/*"],
                                }
                            ),
                        }
                    },
                    "inputArtifacts": [
                        {
                            "location": {
                                "s3Location": {
                                    "bucketName": "bucket_name",
                                    "objectKey": "filename",
                                },
                                "type": "S3",
                            },
                            "revision": None,
                            "name": "ArtifactName",
                        }
                    ],
                    "outputArtifacts": [],
                    "artifactCredentials": {
                        "secretAccessKey": "secret_key",
                        "sessionToken": "session_token",
                        "accessKeyId": "access_key_ID",
                    },
                    "continuationToken": "token_ID",
                    "encryptionKey": {
                        "id": (
                            "arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-"
                            "56ef-1234567890ab"
                        ),
                        "type": "KMS",
                    },
                },
            }
        }
    )
    context = LambdaContext()

    # Moto hasn't implemented CloudFront's PutJobFailureResult and
    # PutJobSuccessResult API calls, so patch them here.
    orig_make_api_call = BaseClient._make_api_call

    def mock_make_api_call(self: BaseClient, operation_name: str, api_params):
        """Intercept calls to PutJobFailureResult and
        PutJobSuccessResult.

        :param self: An instance of botocore's AWS API client.
        :param operation_name: The API being called.
        :param api_params: Any parameters.
        :return: The result of the API call.

        """

        match operation_name:
            # https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobFailureResult.html
            case "PutJobFailureResult":
                raise AssertionError()
                return
            # https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobSuccessResult.html
            case "PutJobSuccessResult":
                assert api_params["jobId"] == job_id
                return

        # Fall through to the original _make_api_call function (well,
        # not the ORIGINAL original---Moto's patched version).
        return orig_make_api_call(self, operation_name, api_params)

    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        invalidate_distribution(event, context)
