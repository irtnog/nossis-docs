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

"""Bundle functional and integration tests in the distribution.

This facilitates the operational qualification of production
deployments.

The names of functional test modules corresponds to the module being
exercised, e.g., `test_widgets.py` exercises the code in `widgets.py`.
Integration test module names are more free-form.

Test function names for API routes follow the corresponding route's
component path names plus the action being tested, e.g.,
`test_widget_creation` checks the `POST /widget` route.

"""
