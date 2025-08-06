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

# Avoid problems on systems where the SHELL variable might be
# inherited from the environment.
SHELL = /bin/sh


# Explicitly clear and then set the suffixes used in implicit rules.
.SUFFIXES:
# .SUFFIXES: .c .o


# Search a colon-separated list of directories for one of the given
# programs, returning the first match.
pathsearch = \
$(or \
	$(firstword \
		$(foreach a, $(2), \
			$(wildcard $(addsuffix /$(a), $(subst :, , $(1)))))), \
	$(3))


# Search the Python virtual environment and the executable search path
# for the programs in the listed order, returning the first match.
venvsearch = \
$(if $(call pathsearch,.venv/bin,$(1)), \
	. .venv/bin/activate; $(1), \
	$(call pathsearch,$(PATH),$(1),exit 1; echo $(1)))


# Develop using the latest available supported version of Python.
PYTHON = \
$(call pathsearch,$(PATH),python3.13 python3.12 python3.11,exit 1; echo python3)
PYTHON_VERSION = \
$(shell $(PYTHON) -c "import sys;print('{}.{}'.format(*sys.version_info[:2]))")


# Use these tools from the development environment, if available.
PRE_COMMIT  = $(call venvsearch,pre-commit)
PYTEST      = $(call venvsearch,pytest)
SPHINXBUILD = $(call venvsearch,sphinx-build)
SPHINXINTL  = $(call venvsearch,sphinx-intl)
SPHINXMULTI = $(call venvsearch,sphinx-multiversion)
TOMLQ       = $(call venvsearch,tomlq)
YQ          = $(call venvsearch,yq)


# On Debian/Ubuntu, install these build dependencies via APT.
DEBIAN_BUILD_DEPS = \
	build-essential \
	devscripts \
	equivs \
	python3.13-full \
	xmlsec1 \


# On Debian/Ubuntu, install these Python packages' build dependencies.
APT_GET_INSTALL = \
apt-get -o Debug::pkgProblemResolver=yes -y --no-install-recommends install
DEBIAN_SOURCE_DEPS = \
	python3-cairosvg \


# On macOS, install these build dependencies (formulas) via Homebrew.
HOMEBREW_FORMULA_BUILD_DEPS = \
	checkov \
	tofu \


# On macOS, install these build dependencies (casks) via Homebrew.
HOMEBREW_CASK_BUILD_DEPS = \
	docker \


# On macOS, install these build dependencies via MacPorts.
MACPORTS_BUILD_DEPS = \
	act \
	actionlint \
	cairo \
	jq \
	libffi \
	py313-cairosvg \
	shellcheck \
	tflint \


# Determine the canonical path to the project's working directory.
PROJECT_ROOT = $(dir $(realpath $(lastword $(MAKEFILE_LIST))))


# Get the package name.
PYPACKAGE_NAME = \
$(shell $(TOMLQ) -r '.tool.setuptools."package-dir"|keys[0]' pyproject.toml)


# Recursively list code, content, and test articles (as well as
# related work in progress).
SOURCEISH ?= $(or $(shell git ls-tree --full-tree --name-only -r HEAD src))
UNTRACKED ?= $(or $(shell git ls-files --others --exclude-standard src))


# Prepare these translations.
TRANSLATIONS=


# Enumerate translation targets.
LOCALES = $(foreach l,$(TRANSLATIONS),docs/_locales/$(l))


# List in-use pre-commit hooks.
PRE_COMMIT_HOOKS = \
$(addprefix .git/hooks/, \
	$(shell \
		$(YQ) -r ".repos[].hooks[].stages[]" .pre-commit-config.yaml \
			2>/dev/null \
		| sort -u \
	) \
	pre-commit \
)


# When adding an alias for a build artifact, add it to this list; cf.
# https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html.
# Sort the list alphabetically.
.PHONY: \
	all \
	build-deps \
	clean \
	clean-deps \
	coverage \
	debug \
	dist \
	distclean \
	docs \
	gettext \
	hash-source-code \
	html \
	lint \
	locale \
	locales \
	pre-commit \
	setup \
	smoke \
	test \
	tests \
	venv \


# Set the default target when running `make`.
all: .coverage


# Install build dependencies for local development.
build-deps:
	$(eval uname = $(or $(shell uname)))
	$(if $(filter Darwin, $(uname)), \
		sudo port -N install $(MACPORTS_BUILD_DEPS); \
		brew install $(HOMEBREW_FORMULA_BUILD_DEPS); \
		brew install --cask $(HOMEBREW_CASK_BUILD_DEPS))
	$(if $(filter Linux, $(uname)), \
		$(eval distro = $(or $(shell lsb_release -is))))
	$(if $(filter Debian Ubuntu, $(distro)), \
		sudo sed -i '/deb-src/s/^# //' /etc/apt/sources.list; \
		sudo apt-get update; \
		sudo DEBIAN_FRONTEND=noninteractive \
			apt-get install -y --no-install-recommends \
				software-properties-common \
		; \
		sudo add-apt-repository -y ppa:deadsnakes/ppa; \
		sudo DEBIAN_FRONTEND=noninteractive \
			apt-get install -y --no-install-recommends \
				$(DEBIAN_BUILD_DEPS) \
		; \
		curl https://bootstrap.pypa.io/get-pip.py | python3.13 -; \
		sudo DEBIAN_FRONTEND=noninteractive \
			mk-build-deps -i -r -t "$(APT_GET_INSTALL)" \
				$(DEBIAN_SOURCE_DEPS); \
		rm -f *.buildinfo *.changes)


# Create the development environment.
venv .venv:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate; python -m pip install -U pip-with-requires-python
	. .venv/bin/activate; python -m pip install -U pip setuptools


# Set up the development environment.
setup $(PYPACKAGE_NAME).egg-info: pyproject.toml .venv
	. .venv/bin/activate; python -m pip install -e .[dev,test]


# Install the pre-commit hooks.
pre-commit: $(PRE_COMMIT_HOOKS)
.git/hooks/%: .pre-commit-config.yaml $(PYPACKAGE_NAME).egg-info
	$(PRE_COMMIT) validate-config
	$(PRE_COMMIT) validate-manifest
	$(PRE_COMMIT) install --install-hooks --hook-type $*


# Run the linter (including unstaged changes).
lint: $(PRE_COMMIT_HOOKS)
	$(PRE_COMMIT) run --show-diff-on-failure --all-files


# Run the test suite.
test tests coverage .coverage: $(PYPACKAGE_NAME).egg-info $(SOURCEISH) $(UNTRACKED)
	$(PYTEST) --cov=$(PYPACKAGE_NAME) $(PYTEST_ARGS)

smoke: $(PYPACKAGE_NAME).egg-info
	$(PYTEST) -m "smoke and not slow" $(PYTEST_ARGS)


# Generate the documentation.
docs: $(LOCALES) | $(PYPACKAGE_NAME).egg-info
	$(foreach l,en $(TRANSLATIONS), \
		$(SPHINXMULTI) -D language="$(l)" docs build/html/$(l))
	env LATEST_VERSION=`git describe --tag --abbrev=0` \
		envsubst < docs/.index.html > build/html/index.html

locale locales: $(LOCALES)
docs/_locales/%: build/gettext | $(PYPACKAGE_NAME).egg-info
	mkdir -p $@
	$(SPHINXINTL) -c docs/conf.py update -p build -l $*
	touch $@

gettext build/gettext: | $(PYPACKAGE_NAME).egg-info
	$(SPHINXBUILD) -b gettext -n docs build $(SPHINXOPTS)
	touch build/gettext


# Build the distribution.
dist: .coverage
	. .venv/bin/activate; [ -f requirements.txt ] || ( \
		pip-compile -o requirements.txt pyproject.toml; \
		python -m build; \
		twine check dist/*; \
		echo "file://localhost$(PROJECT_ROOT)$(wildcard dist/*.whl)" \
			>> requirements.txt \
	)
	. .venv/bin/activate; pip install --no-compile --target dist-lambda -r requirements.txt
	find dist-lambda -exec touch -t 198001010000.00 '{}' \;

distclean:
	rm -rf dist* requirements.txt


# Remove build artifacts and reset the development environment.
clean: distclean
	rm -rf build* .coverage .pytest_cache .venv* docs/apidocs \
		docs/_locales/en $(PRE_COMMIT_HOOKS)
	find . -type d -name __pycache__ -print | xargs rm -rf
	find . -type d -name .external_modules -print | xargs rm -rf
	find . -type d -name \*.egg-info -print | xargs rm -rf


# This could remove packages other that the ones listed, so keep any
# confirmation prompts (requires local administrator rights).
clean-deps:
	$(eval uname = $(or $(shell uname)))
	$(if $(filter Darwin, $(uname)), \
		sudo port uninstall $(MACPORTS_BUILD_DEPS); \
		brew uninstall $(HOMEBREW_FORMULA_BUILD_DEPS); \
		brew uninstall --cask $(HOMEBREW_CASK_BUILD_DEPS))
	$(if $(filter Linux, $(uname)), \
		$(eval distro = $(or $(shell lsb_release -is))))
	$(if $(filter Debian Ubuntu, $(distro)), \
		sudo apt-mark auto \
			$(DEBIAN_BUILD_DEPS) \
			$(addsuffix -build-deps, $(DEBIAN_SOURCE_DEPS)) \
		; \
		sudo apt-get autoremove)


# Fingerprint the source code.  Run this in a fresh clone of the
# repository.  Refer to the Continuous Integration workflow
# (.github/workflows/ci.yml) for more information.
hash-source-code:
	@find pyproject.toml *.tf modules src -type f -exec cat '{}' \; \
		| sha512sum \
		| awk '{print "hash=" $$1}'
