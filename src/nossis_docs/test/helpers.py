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

"""Test utilities, including helper classes and functions."""

from dataclasses import dataclass


@dataclass
class _LambdaContext:
    """A minimal (fake) Lambda execution context."""

    aws_request_id: str
    """Identify the invocation request."""

    function_name: str
    """Name the Lambda function."""

    invoked_function_arn: str
    """Provide the Amazon Resource Name (ARN) used to invoke the
    function."""

    memory_limit_in_mb: int = 128
    """Report the amount of memory allocated for the function."""
