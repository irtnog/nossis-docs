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

"""AWS Lambda actions for CodePipeline."""

from typing import List

import boto3
import humps
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.data_classes import (
    CodePipelineJobEvent,
    event_source,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from mypy_boto3_cloudfront import CloudFrontClient
from mypy_boto3_cloudfront.type_defs import CreateInvalidationResultTypeDef
from mypy_boto3_codepipeline import CodePipelineClient

from . import __app_name__

logger = Logger()
"""Configure module-level logging."""

metrics = Metrics(
    namespace=humps.pascalize(__app_name__),
    service=humps.pascalize(__name__.split(".")[-1]),
)
"""Configure module-level metrics.

The metric namespace is the package's name converted to Pascal case;
the metric service, this submodule's name.

"""

tracer = Tracer()
"""Configure module-level tracing."""


@event_source(data_class=CodePipelineJobEvent)
@logger.inject_lambda_context
@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
def invalidate_distribution(
    event: CodePipelineJobEvent, context: LambdaContext
) -> None:
    """Flush the given CloudFront distribution's cache.

    `event`
    : [A CodePipeline job event](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-Lambda.html).

    `context`
    : The execution context of the Lambda function.

    As the Lambda function is invoked asynchronously and updates the
    calling CodePipeline job's status directly,
    [this has no return value](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html#python-handler-return).

    """  # noqa: B950
    try:
        # Connect to AWS services.
        cloudfront: CloudFrontClient = boto3.client("cloudfront")
        codepipeline: CodePipelineClient = boto3.client("codepipeline")

        # Parse the event data.
        params: dict = event.decoded_user_parameters
        distribution_id: str = params["distribution_id"]
        paths: List[str] = params["object_paths"]
        logger.debug(f"Object paths: {', '.join(paths)}")

        # The pipeline tells us what paths to invalidate so as to not
        # flush the entire cache.
        inv: CreateInvalidationResultTypeDef = cloudfront.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                "Paths": {"Quantity": len(paths), "Items": paths},
                "CallerReference": event.get_id,
            },
        )
        logger.info(
            f"Invalidation {inv['Invalidation']['Id']} created for {distribution_id} "
            f"by {event.get_id}."
        )
        metrics.add_metric("InvalidationsCreated", MetricUnit.Count, value=1)
        codepipeline.put_job_success_result(jobId=event.get_id)
    except Exception as exc:
        # Signal the pipeline if anything fails for any reason.
        logger.error(f"Invalidation on behalf of {event.get_id} failed: {str(exc)}")
        metrics.add_metric("InvalidationErrors", MetricUnit.Count, value=1)
        codepipeline.put_job_failure_result(
            jobId=event.get_id,
            failureDetails={"type": "JobFailed", "message": str(exc)},
        )
