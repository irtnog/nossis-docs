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

"""The top-level test configuration file."""

import os
from typing import Any, Dict, List

import pytest

options: List[Dict[str, Any]] = []
"""Define additional pytest configuration items.

List entries are {py:method}`pytest.Parser.addini` kwargs.  For
example:

```
{
    "name": "db_driver",
    "help": "Use the named ODBC driver.",
}
```

"""


def pytest_addoption(parser: pytest.Parser, pluginmanager: pytest.PytestPluginManager):
    """Customize the pytest configuration file and CLI arguments.

    :::{note}
    Pytest only calls this hook when loading plugins or the top-level
    test configuration file (this file).
    :::

    `parser`
    : The pytest configuration file and command line argument parser.

    `pluginmanager`
    : Manages the registration of pytest plugins and related hooks.

    """
    for option in options:
        option: Dict[str, Any]

        # Add each new option to both the configuration file and the
        # CLI argument list, e.g, an option named `the_option_name`
        # has a corresponding CLI argument named `--the-option-name`.
        parser.addini(**option)
        parser.addoption(f"--{option['name'].replace('_', '-')}", help=option["help"])


def pytest_configure(config: pytest.Config):
    """Load the custom pytest configuration into the test session.

    Access the configuration via
    <inv:pytest:std:fixture#pytestconfig>, e.g.,
    `pytestconfig.option.the_option_name`.

    Allow overriding the configuration via the process environment.
    Environment variables must use option names converted to upper
    case, e.g,. `THE_OPTION_NAME`.

    :::{note}
    Environment variables override CLI arguments.  CLI arguments
    override the configuration file.  Configuration items default to
    `None` unless the configuration file option definition in
    {function}`pytest_addoption` specifies a different value.
    :::

    `config`
    : The pytest run-time configuration.

    """
    for option in options:
        option: Dict[str, Any]
        option_name: str = option["name"]

        # Pytest automatically converts CLI argument names back into
        # snake case, e.g., access the value of `--the-option-name`
        # using the key `the_option_name`.
        setattr(
            config.option,
            option_name,
            os.environ.get(
                option_name.upper(),
                config.getoption(option_name, config.getini(option_name)),
            ),
        )
