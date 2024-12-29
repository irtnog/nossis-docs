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

"""Configure test fixtures (mocks)."""

import os
from datetime import UTC, datetime

import boto3
import pytest
from moto import mock_aws
from mypy_boto3_cloudfront import CloudFrontClient
from mypy_boto3_cloudfront.type_defs import CreateDistributionResultTypeDef


@pytest.fixture
def _aws_credentials():
    """Avoid mutating real AWS infrastructure."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "True"
    os.environ["AWS_DEFAULT_REGION"] = "antarctica"


@pytest.fixture
def cloudfront(_aws_credentials) -> CloudFrontClient:
    """Mock up a CloudFront client."""
    with mock_aws():
        yield boto3.client("cloudfront")


@pytest.fixture
def mock_distribution(cloudfront: CloudFrontClient) -> CreateDistributionResultTypeDef:
    """Mock up a CloudFront distribution."""

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_distribution.html
    return cloudfront.create_distribution(
        DistributionConfig={
            "CallerReference": datetime.now(UTC).isoformat(),
            "DefaultRootObject": "index.html",
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "Id": (origin_id := "test-origin"),
                        "DomainName": "www.example.com",
                        "CustomOriginConfig": {  # TODO: use a mock S3 bucket
                            "HTTPPort": 80,
                            "HTTPSPort": 443,
                            "OriginProtocolPolicy": "https-only",
                            "OriginSslProtocols": {"Quantity": 1, "Items": ["TLSv1.2"]},
                        },
                    },
                ],
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": origin_id,
                "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {
                    "Quantity": 2,
                    "Items": ["GET", "HEAD"],
                    "CachedMethods": {
                        "Quantity": 2,
                        "Items": ["GET", "HEAD"],
                    },
                },
                "Compress": True,
                "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
                "OriginRequestPolicyId": "acba4595-bd28-49b8-b9fe-13317c0390fa",
                "ResponseHeadersPolicyId": "67f7725c-6f97-4210-82d7-5512b31e9d03",
            },
            "CustomErrorResponses": {
                "Quantity": len(
                    custom_error_responses := [
                        {
                            "ErrorCode": r,
                            "ResponseCode": str(r),
                            "ResponsePagePath": "/error.html",
                        }
                        for r in [400, 403, 404, 405, 414, 416, 500, 501, 502, 503, 504]
                    ]
                ),
                "Items": custom_error_responses,
            },
            "Comment": "Test Fixture",
            "Logging": {
                "Enabled": False,
                "IncludeCookies": False,
                "Bucket": "",
                "Prefix": "",
            },
            "PriceClass": "PriceClass_100",
            "Enabled": True,
            "ViewerCertificate": {
                "CloudFrontDefaultCertificate": True,
                "MinimumProtocolVersion": "TLSv1.2_2021",
            },
            "Restrictions": {
                "GeoRestriction": {
                    "RestrictionType": "none",
                    "Quantity": 0,
                    "Items": [],
                }
            },
            "IsIPV6Enabled": True,
            "Staging": False,
        }
    )
