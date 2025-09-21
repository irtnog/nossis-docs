# Nossis Docs, serverless hosting for static, private web sites
#
# Copyright (C) 2024-2025  Matthew X. Economou
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

"""Check content update handling."""

import json
from unittest.mock import patch

import pytest
from aws_lambda_powertools.utilities.data_classes import CodePipelineJobEvent
from botocore.client import BaseClient
from mypy_boto3_cloudfront.type_defs import CreateDistributionResultTypeDef

from ..pipeline import invalidate_distribution
from .helpers import _LambdaContext


@pytest.fixture
def content_update_event(
    distribution: CreateDistributionResultTypeDef,
) -> CodePipelineJobEvent:
    """Simulate a web site content update event.

    This event contains the data
    [CodePipeline includes when invoking a Lambda function](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-Lambda.html)
    after an update to a GitHub repository's `gh-pages` branch.

    `distribution`

    """  # noqa: B950
    distribution_id = distribution["Distribution"]["Id"]
    return CodePipelineJobEvent(
        {
            "CodePipeline.job": {
                "id": "11111111-abcd-1111-abcd-111111abcdef",
                "accountId": "111111111111",
                "data": {
                    "actionConfiguration": {
                        "configuration": {
                            "FunctionName": "MyLambdaFunction",
                            "UserParameters": json.dumps(
                                {
                                    "distribution_id": distribution_id,
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


@pytest.mark.smoke
def test_cache_invalidation(
    content_update_event: CodePipelineJobEvent, lambda_context: _LambdaContext
) -> None:
    """Simulate a CodePipeline deploy stage.

    The test signals a Lambda function to remove outdated content from
    a CloudFront distribution's cache.

    `content_update_event`
    : A mock CodePipeline job event.

    `lambda_context`
    : Mock Lambda execution context.

    """
    orig_make_api_call = BaseClient._make_api_call

    def mock_make_api_call(self: BaseClient, operation_name: str, api_params):
        """Intercept calls to PutJobFailureResult/PutJobSuccessResult.

        At the time this was written, Moto hadn't implemented the
        [PutJobFailureResult](https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobFailureResult.html)
        and
        [PutJobSuccessResult](https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_PutJobSuccessResult.html)
        API calls, so this test patches them itself.

        `self`
        : An instance of botocore's AWS API client.

        `operation_name`
        : The API being called.

        `api_params`
        : Any parameters.

        Returns the result of the API call.

        """
        match operation_name:
            case "PutJobFailureResult":
                raise AssertionError()
                return
            case "PutJobSuccessResult":
                assert api_params["jobId"] == content_update_event.get_id
                return

        # Fall through to the original _make_api_call function (well,
        # not the ORIGINAL original---Moto's patched version).
        return orig_make_api_call(self, operation_name, api_params)

    with patch("botocore.client.BaseClient._make_api_call", new=mock_make_api_call):
        invalidate_distribution(content_update_event, lambda_context)
