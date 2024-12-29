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

"""AWS Lambda actions for CodePipeline."""

import logging
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools.utilities.data_classes import (
    CodePipelineJobEvent,
    event_source,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_cloudfront import CloudFrontClient
from mypy_boto3_codepipeline import CodePipelineClient

# Configure module-level logging.
logger = logging.getLogger(__name__)

# Connect to AWS services.
cloudfront: CloudFrontClient = boto3.client("cloudfront")
codepipeline: CodePipelineClient = boto3.client("codepipeline")


@event_source(data_class=CodePipelineJobEvent)
def invalidate_distribution(
    event: CodePipelineJobEvent, context: LambdaContext
) -> Dict[str, Any]:
    """When triggered by CodePipeline, flush the given CloudFront
    distribution's cache."""
    try:
        # Parse the event data.
        params: dict = event.decoded_user_parameters
        paths: List[str] = params["object_paths"]

        # The pipeline tells us what paths to invalidate so as to not
        # flush the entire cache.
        cloudfront.create_invalidation(
            DistributionId=params["distribution_id"],
            InvalidationBatch={
                "Paths": {"Quantity": len(paths), "Items": paths},
                "CallerReference": event.get_id,
            },
        )
    except Exception as exc:
        # If that fails for some reason, report the error to the
        # pipeline.
        codepipeline.put_job_failure_result(
            jobId=event.get_id,
            failureDetails={"type": "JobFailed", "message": str(exc)},
        )
    else:
        codepipeline.put_job_success_result(jobId=event.get_id)
