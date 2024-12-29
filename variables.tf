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

variable "cert_dcv_method" {
  description = <<-EOT
    (Optional) When requesting a new service certificate, use DNS
    record- or confirmation email-based domain control validation
    (DCV).  If using DNS DCV (the default) and if hosted_zone_id is
    set, the stack will handle this automatically.  Otherwise,
    validation will require manual action by one of the domain's
    contacts.  For more information, refer to
    https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html
    (DNS) or
    https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html
    (EMAIL).
    EOT
  type        = string
  default     = "DNS"

  validation {
    condition     = contains(["DNS", "EMAIL"], var.cert_dcv_method)
    error_message = "Unsupported domain control validation method"
  }
}

variable "certificate_arn" {
  description = <<-EOT
    (Optional) The stack will use this certificate in AWS Certificate
    Manager (ACM).  If left blank, the stack will request a new ACM
    certificate.
    EOT
  type        = string
  default     = ""
}

variable "cloudfront_price_class" {
  description = <<-EOT
    Select a CloudFront price class that matches the audience's
    location.
    EOT
  type        = string
  default     = "PriceClass_All"

  validation {
    condition = contains(
      ["PriceClass_100", "PriceClass_200", "PriceClass_All"],
      var.cloudfront_price_class,
    )
    error_message = "Unsupported CloudFront price class"
  }
}

variable "domain_name" {
  description = <<-EOT
    The domain name of the service, e.g., for \"docs.example.com\",
    the domain name would be \"example.com\".
    EOT
  type        = string
}

variable "gh_pages_branch" {
  description = <<-EOT
    Publish web content from this branch of the specified Git
    repositories.
    EOT
  type        = string
  default     = "gh-pages"
}

variable "git_repos" {
  description = <<-EOT
    Publish the web content branches of these Git repositories (JSON
    list of repository URLs).
    EOT
  type        = string
}

variable "hosted_zone_id" {
  description = <<-EOF
    (Optional) If specified, the stack will create resource records
    for the service in this Route 53 hosted zone.  Note that the Route
    53 hosted zone MUST exist in the same partition/account as this
    stack.
    EOF
  type        = string
  default     = ""
}

variable "hostname" {
  description = <<-EOT
    The short name of the service, e.g., for \"docs.example.com\", the
    hostname would be \"docs\".
    EOT
  type        = string
}

variable "lambda_arch" {
  type        = string
  default     = "arm64"
  description = "Deploy Lambda functions on the selected hardware architecture."

  validation {
    condition     = contains(["arm64", "x86_64"], var.lambda_arch)
    error_message = "Unsupported hardware architecture specified."
  }
}

variable "s3_encryption_key_arn" {
  description = <<-EOT
    (Optional; SSE-KMS only) The stack will use this symmetric KMS
    master key to encrypt S3 storage instead of the default.
    EOT
  type        = string
  # FIXME arn:${AWS::Partition}:kms:${AWS::Region}:${AWS::AccountId}:alias/aws/s3
  default = null
}

variable "s3_server_side_encryption" {
  description = <<-EOT
    (Optional) The stack will encrypt S3-backed storage with a key of
    this type.  SSE-KMS costs more but enables key usage auditing and
    offers better control over key management.
    EOT
  type        = string
  default     = "SSE-S3"

  validation {
    condition     = contains(["SSE-KMS", "SSE-S3"], var.s3_server_side_encryption)
    error_message = "Unsupported S3 storage encryption method"
  }
}

variable "stack_name" {
  description = "Give this service a unique name."
  type        = string
  nullable    = false
}

variable "tags_all" {
  description = <<-EOT
    Apply these AWS metadata tags to all resources (JSON mapping tag
    names to values).
    EOT
  type        = string
  default     = "{}"
}
