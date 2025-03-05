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

terraform {
  required_version = ">= 1.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.46"
    }
  }
}

provider "aws" {
  default_tags {
    tags = jsondecode(var.TAGS_ALL)
  }
}

data "aws_partition" "current" {}

locals {
  with_s3_sse_kms = alltrue([
    var.S3_SERVER_SIDE_ENCRYPTION == "SSE-KMS",
    var.S3_ENCRYPTION_KEY_ARN != "",
  ])

  with_route53_dns_dcv = alltrue([
    var.CERTIFICATE_ARN == "",
    var.CERT_DCV_METHOD == "DNS",
    var.HOSTED_ZONE_ID != "",
  ])

  fqdn = "${var.HOSTNAME}.${var.DOMAIN_NAME}"

  s3_origin_id = "${var.STACK_NAME}-s3-origin"

  git_repos = jsondecode(var.GIT_REPOS)
}


# Request a certificate if one wasn't specified.
resource "aws_acm_certificate" "this" {
  count = var.CERTIFICATE_ARN == "" ? 1 : 0

  domain_name       = local.fqdn
  validation_method = var.CERT_DCV_METHOD

  validation_option {
    domain_name       = local.fqdn
    validation_domain = var.DOMAIN_NAME
  }

  lifecycle {
    create_before_destroy = true
  }
}


# If requesting a certificate, prove ownership of the web site by
# publishing a special record in DNS (only supports DNS domains hosted
# by Route 53).
resource "aws_route53_record" "this" {
  # Because this creates a variable number of aws_acm_certificate.this
  # objects and because they are represented as a set, we have to
  # iterate over them.  Build a list of certificates' domain
  # validation options, convert that list to function arguments, and
  # merge them into a single mapping.
  for_each = local.with_route53_dns_dcv ? merge([
    for cert in aws_acm_certificate.this : {
      for dvo in cert.domain_validation_options : dvo.domain_name => {
        name   = dvo.resource_record_name
        record = dvo.resource_record_value
        type   = dvo.resource_record_type
      }
    }
  ]...) : {}

  # Create a DCV record for each domain name in every certificate.
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.HOSTED_ZONE_ID
}


# If requesting a certificate, wait for ACM to issue it before
# proceeding.
resource "aws_acm_certificate_validation" "this" {
  for_each = {
    for cert in aws_acm_certificate.this : cert.domain_name => cert.arn
  }

  certificate_arn = each.value
  validation_record_fqdns = [
    for record in aws_route53_record.this : record.fqdn
  ]
}


# Store web content in an S3 bucket.
resource "aws_s3_bucket" "this" {
  bucket = "${var.STACK_NAME}-content"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = local.with_s3_sse_kms ? "aws:kms" : "AES256"
      kms_master_key_id = var.S3_ENCRYPTION_KEY_ARN
    }
  }
}


# Give CloudFront permission to access S3.
resource "aws_cloudfront_origin_access_identity" "this" {}

data "aws_iam_policy_document" "allow_access_from_cloudfront" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.this.iam_arn]
    }

    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.this.arn}/*"]
  }
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.allow_access_from_cloudfront.json
}


# Serve the web content using CloudFront.
resource "aws_cloudfront_distribution" "this" {
  for_each = var.CERTIFICATE_ARN == "" ? {
    for cert in aws_acm_certificate_validation.this : local.fqdn => cert.certificate_arn
    } : {
    local.fqdn = var.CERTIFICATE_ARN
  }

  comment = "${each.key} (${var.STACK_NAME})"
  aliases = [each.key]

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = var.CLOUDFRONT_PRICE_CLASS

  viewer_certificate {
    acm_certificate_arn = each.value
    ssl_support_method  = "sni-only"

    # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/secure-connections-supported-viewer-protocols-ciphers.html
    minimum_protocol_version = "TLSv1.2_2021"
  }

  # TODO: logging

  origin {
    origin_id   = local.s3_origin_id
    domain_name = aws_s3_bucket.this.bucket_regional_domain_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.this.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    # CachingOptimized managed cache policy
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"

    # UserAgentRefererHeaders managed origin request policy
    origin_request_policy_id = "acba4595-bd28-49b8-b9fe-13317c0390fa"

    # SecurityHeadersPolicy managed response header policy
    response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }
}


# Publish the CloudFront distribution in DNS.
resource "aws_route53_record" "cdn" {
  for_each = var.HOSTED_ZONE_ID != "" ? {
    for dist in aws_cloudfront_distribution.this : local.fqdn => {
      domain_name    = dist.domain_name
      hosted_zone_id = dist.hosted_zone_id
    }
  } : {}

  allow_overwrite = true
  name            = each.key
  type            = "A"
  zone_id         = var.HOSTED_ZONE_ID

  alias {
    name    = each.value.domain_name
    zone_id = each.value.hosted_zone_id

    evaluate_target_health = true
  }
}


# Store build artifacts in S3 for one day.
resource "aws_s3_bucket" "pipeline" {
  bucket = "${var.STACK_NAME}-temp"
}

resource "aws_s3_bucket_lifecycle_configuration" "pipeline" {
  bucket = aws_s3_bucket.pipeline.id

  rule {
    id     = "daily_cleaning"
    status = "Enabled"

    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }

    expiration {
      days = 1
    }
  }
}

resource "aws_s3_bucket_public_access_block" "pipeline" {
  bucket = aws_s3_bucket.pipeline.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "pipeline" {
  bucket = aws_s3_bucket.pipeline.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = local.with_s3_sse_kms ? "aws:kms" : "AES256"
      kms_master_key_id = var.S3_ENCRYPTION_KEY_ARN
    }
  }
}


# Connect to GitHub.
resource "aws_codestarconnections_connection" "github" {
  name          = "${var.STACK_NAME}-github"
  provider_type = "GitHub"
}


# Pre-create the log group for the following Lambda function.  This
# uses the AWS naming convention for the log group name following the
# principle of least astonishment.  As this log only really exists for
# diagnostic purposes, limit log retention to 3 days.
resource "aws_cloudwatch_log_group" "invalidate_distribution" {
  name              = "/aws/lambda/${var.STACK_NAME}-invalidate-distribution"
  retention_in_days = 3
}


# Deploy a helper function in Lambda that invalidates the CloudFront
# distribution's cache after CodePipeline updates the web site
# storage.
data "aws_iam_policy_document" "lambda_trust" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.${data.aws_partition.current.dns_suffix}"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "invalidate_distribution" {
  name               = "${var.STACK_NAME}-invalidate-distribution"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

resource "aws_lambda_function" "invalidate_distribution" {
  function_name    = "${var.STACK_NAME}-invalidate-distribution"
  role             = aws_iam_role.invalidate_distribution.arn
  filename         = "lambda-functions.zip"
  source_code_hash = filebase64sha256("lambda-functions.zip")
  handler          = "nossis_docs.pipeline.invalidate_distribution"
  runtime          = "python3.12"
  architectures    = [var.LAMBDA_ARCH]

  logging_config {
    log_group  = aws_cloudwatch_log_group.invalidate_distribution.name
    log_format = "JSON"
  }
}


# Allow the helper function permission to invalidate cached content in
# the CloudFront distribution and then report back to its caller.
data "aws_iam_policy_document" "invalidate_distribution" {
  # https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazoncloudwatchlogs.html
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["${aws_cloudwatch_log_group.invalidate_distribution.arn}:log-stream:*"]
  }

  # https://docs.aws.amazon.com/service-authorization/latest/reference/list_awscodepipeline.html
  statement {
    effect = "Allow"
    actions = [
      "codepipeline:PutJobFailureResult",
      "codepipeline:PutJobSuccessResult",
    ]
    resources = ["*"]
  }

  # https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazoncloudfront.html
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:CreateInvalidation"]
    resources = [for dist in aws_cloudfront_distribution.this : dist.arn]
  }
}

resource "aws_iam_policy" "invalidate_distribution" {
  name   = "${var.STACK_NAME}-invalidate-distribution"
  policy = data.aws_iam_policy_document.invalidate_distribution.json
}

resource "aws_iam_role_policy_attachment" "invalidate_distribution" {
  role       = aws_iam_role.invalidate_distribution.name
  policy_arn = aws_iam_policy.invalidate_distribution.arn
}


# Give pipelines access to artifact storage, web site storage, code
# repository connections, and helper functions.
data "aws_iam_policy_document" "codepipeline_trust" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["codepipeline.${data.aws_partition.current.dns_suffix}"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "this" {
  name               = "${var.STACK_NAME}-codepipeline"
  assume_role_policy = data.aws_iam_policy_document.codepipeline_trust.json
}

data "aws_iam_policy_document" "this" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:GetBucketVersioning",
      "s3:PutObjectAcl",
      "s3:PutObject",
    ]
    resources = [
      "${aws_s3_bucket.pipeline.arn}/*",
      aws_s3_bucket.pipeline.arn,
      "${aws_s3_bucket.this.arn}/*",
      aws_s3_bucket.this.arn,
    ]
  }

  dynamic "statement" {
    for_each = local.with_s3_sse_kms ? [1] : []
    content {
      effect = "Allow"
      actions = [
        "kms:Decrypt",
        "kms:Encrypt",
      ]
      resources = [var.S3_ENCRYPTION_KEY_ARN]
    }
  }

  # The pipeline must be allowed to use _both_ actions for the Source
  # action to work properly; cf. https://stackoverflow.com/a/64308047,
  # specifically Corin's comment.
  statement {
    effect = "Allow"
    actions = [
      "codeconnections:UseConnection",
      "codestar-connections:UseConnection",
    ]
    resources = [aws_codestarconnections_connection.github.arn]
  }

  statement {
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.invalidate_distribution.arn]
  }
}

resource "aws_iam_policy" "this" {
  name   = "${var.STACK_NAME}-codepipeline"
  policy = data.aws_iam_policy_document.this.json
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

# Create a content publishing pipeline for each configured Git
# repository.
resource "aws_codepipeline" "this" {
  for_each = {
    for repo in local.git_repos : repo => {
      repo_id      = regex(".*/([^/]+)$", repo)[0]
      full_repo_id = regex(".*/([^/]+/[^/]+)$", repo)[0]
      dist_id      = [for dist in aws_cloudfront_distribution.this : dist.id][0]
    }
  }

  name     = "${var.STACK_NAME}-${each.value.repo_id}"
  role_arn = aws_iam_role.this.arn

  artifact_store {
    type     = "S3"
    location = aws_s3_bucket.pipeline.bucket

    dynamic "encryption_key" {
      for_each = local.with_s3_sse_kms ? [1] : []
      content {
        type = "KMS"
        id   = var.S3_ENCRYPTION_KEY_ARN
      }
    }
  }

  stage {
    name = "Source"

    # https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html
    action {
      name     = "Source"
      category = "Source"
      owner    = "AWS"
      provider = "CodeStarSourceConnection"
      version  = "1"

      configuration = {
        ConnectionArn    = aws_codestarconnections_connection.github.arn
        FullRepositoryId = each.value.full_repo_id
        BranchName       = var.GH_PAGES_BRANCH
      }

      output_artifacts = ["pages"]
    }
  }

  stage {
    name = "Deploy"

    # https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-S3Deploy.html
    action {
      name     = "Deploy"
      category = "Deploy"
      owner    = "AWS"
      provider = "S3"
      version  = "1"

      input_artifacts = ["pages"]

      configuration = {
        BucketName          = aws_s3_bucket.this.bucket
        Extract             = true
        ObjectKey           = each.value.repo_id
        KMSEncryptionKeyARN = local.with_s3_sse_kms ? var.S3_ENCRYPTION_KEY_ARN : null
      }
    }
  }

  stage {
    name = "Invalidate"

    # https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-Lambda.html
    action {
      name     = "Invalidate"
      category = "Invoke"
      owner    = "AWS"
      provider = "Lambda"
      version  = "1"

      configuration = {
        FunctionName = aws_lambda_function.invalidate_distribution.function_name
        UserParameters = jsonencode({
          "distribution_id" = each.value.dist_id
          "object_paths"    = ["/${each.value.repo_id}/*"]
        })
      }
    }
  }
}
