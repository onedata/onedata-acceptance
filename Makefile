TEST_RUN := ./test_run.py

ifdef ENV_FILE
TEST_RUN := $(TEST_RUN) --env-file $(ENV_FILE)
endif

GIT_URL := $(shell git config --get remote.origin.url | sed -e 's/\(\/[^/]*\)$$//g')
GIT_URL := $(shell if [ "${GIT_URL}" = "file:/" ]; then echo 'ssh://git@git.plgrid.pl:7999/vfs'; else echo ${GIT_URL}; fi)
ONEDATA_GIT_URL := $(shell if [ "${ONEDATA_GIT_URL}" = "" ]; then echo ${GIT_URL}; else echo ${ONEDATA_GIT_URL}; fi)
export ONEDATA_GIT_URL

# TODO: VFS-12424 Try latest Chrome (newer than 128.0.6613.86) with fix from this issue
ACCEPTANCE_TEST_IMAGE := onedata/acceptance_tests:v3.132

unpack = tar xzf $(1).tar.gz

##
## Artifacts
##

artifact: artifact_op_worker artifact_oz_worker artifact_cluster_manager artifact_onepanel artifact_onezone artifact_onedata

artifact_op_worker:
	$(call unpack, op_worker)

artifact_oz_worker:
	$(call unpack, oz_worker)

artifact_cluster_manager:
	$(call unpack, cluster_manager)

artifact_onepanel:
	$(call unpack, onepanel)

artifact_onezone:
	$(call unpack, onezone)

artifact_onedata:
	$(call unpack, onedata)

artifact_oneclient:
	$(call unpack, oneclient)

artifact_luma_docker_build:
	$(call unpack, luma_docker_build)

artifact_rest_cli_docker_build:
	$(call unpack, rest_cli_docker_build)

artifact_oneclient_docker_build:
	$(call unpack, oneclient_docker_build)

##
## Submodules
##

branch = $(shell git rev-parse --abbrev-ref HEAD)
submodules:
	git submodule init ${submodule}
	git submodule update --init --recursive ${submodule}

checkout_getting_started:
	git submodule init getting_started
	git submodule update --remote getting_started

##
## Test
##

RECORDING_OPTION            ?= failed
BROWSER                     ?= Chrome
TIMEOUT			            ?= 600
COUNT                       ?= 1
RERUNS                      ?= 1
LOCAL_CHARTS_PATH           ?= ""
PULL_ONLY_MISSING_IMAGES    ?= ""
FILE_MODE                   ?= regular
TESTS_ROOT := $(shell pwd)
GENERATED_CLIENTS_ROOT := ${TESTS_ROOT}/generated

ifdef bamboo_GUI_PKG_VERIFICATION
    GUI_PKG_VERIFICATION = --gui-pkg-verification
endif

# TODO VFS-9779 - reorganize test targets after introducing bamboo specs
.PHONY: test_gui test_gui_pkg test_gui_src
.PHONY: test_mixed test_mixed_pkg test_mixed_src
.PHONY: test_oneclient test_oneclient_pkg test_oneclient_src
.PHONY: test_performance test_performance_pkg test_performance_src
.PHONY: test_upgrade_pkg test_upgrade_src
.PHONY: format format-check static-analysis type-check
.PHONY: submodules
.PHONY: test_demo_mode

test_gui:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i ${ACCEPTANCE_TEST_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	-k=${KEYWORDS} --timeout ${TIMEOUT} --reruns ${RERUNS} --count ${COUNT} --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${SOURCES} ${OPTS}

test_gui_pkg: test_gui
test_gui_src: SOURCES = --sources
test_gui_src: test_gui

test_mixed:
	PYTHONPATH=${GENERATED_CLIENTS_ROOT} ${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i ${ACCEPTANCE_TEST_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	 -k=${KEYWORDS} --count ${COUNT} --timeout ${TIMEOUT} --reruns ${RERUNS} --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${SOURCES} ${OPTS}

test_mixed_pkg: test_mixed
test_mixed_src: SOURCES = --sources
test_mixed_src: test_mixed

test_oneclient:
	${TEST_RUN} --test-type oneclient -vvv --test-dir tests/oneclient/scenarios/${SUITE}.py -i ${ACCEPTANCE_TEST_IMAGE} -k=${KEYWORDS} \
	 --count ${COUNT} --timeout ${TIMEOUT} --file-mode ${FILE_MODE} ${SOURCES} ${OPTS}

test_oneclient_pkg: test_oneclient
test_oneclient_src: SOURCES = --sources
test_oneclient_src: test_oneclient

test_performance:
	${TEST_RUN} --test-type performance -vvv --test-dir tests/performance --image ${ACCEPTANCE_TEST_IMAGE} -k=${KEYWORDS} ${SOURCES} ${OPTS}

test_performance_pkg: test_performance
test_performance_src: SOURCES = --sources
test_performance_src: test_performance

test_upgrade_pkg:
	${TEST_RUN} --ignore-xfail --test-type upgrade -vvv --test-dir tests/upgrade --image ${ACCEPTANCE_TEST_IMAGE} --timeout ${TIMEOUT} --local-charts-path="" --pull-only-missing-images --env-file=tests/upgrade/configs/pkg/"${CONFIG_FILE}".yaml
test_upgrade_src:
	${TEST_RUN} --ignore-xfail --test-type upgrade -vvv --test-dir tests/upgrade --image ${ACCEPTANCE_TEST_IMAGE} --timeout ${TIMEOUT} --local-charts-path="" --pull-only-missing-images --env-file=tests/upgrade/configs/src/"${CONFIG_FILE}".yaml

DEMO_MODE_SCENARIOS_ROOT := tests/demo_mode/scenarios
DEMO_MODE_TESTS := \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_run_in_foreground.py \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_distributed_environment.py \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_run_in_background.py \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_comprehensive_example.py \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_python_access.py \
	$(DEMO_MODE_SCENARIOS_ROOT)/test_persistence.py
DEMO_MODE_TEST_REPORTS_DIR := $(CURDIR)/test-reports
DEMO_MODE_LOGS_DIR := $(CURDIR)/tests/demo_mode/logs
DEMO_MODE_DOCKER_CONFIG_DIR := $(if $(DOCKER_CONFIG),$(DOCKER_CONFIG),$(HOME)/.docker)
ifdef SCENARIO
DEMO_MODE_TEST_PATH := ${DEMO_MODE_SCENARIOS_ROOT}/${SCENARIO}.py
else
DEMO_MODE_TEST_PATH := $(DEMO_MODE_TESTS)
endif
ifdef RUNNER_NAME
DEMO_MODE_RUNNER_NAME_OPTION := --name="${RUNNER_NAME}"
endif
ifdef DOCKER_API_VERSION
DEMO_MODE_DOCKER_API_VERSION_OPTION := -e DOCKER_API_VERSION="${DOCKER_API_VERSION}"
endif

# ONEZONE_IMAGE and ONEPROVIDER_IMAGE can be used to override the defaults, 
# which are resolved based on branchConfig
ifdef ONEZONE_IMAGE
DEMO_MODE_ONEZONE_IMAGE_OPTION := --onezone-image="${ONEZONE_IMAGE}"
endif
ifdef ONEPROVIDER_IMAGE
DEMO_MODE_ONEPROVIDER_IMAGE_OPTION := --oneprovider-image="${ONEPROVIDER_IMAGE}"
endif

test_demo_mode:
	@test -z "${SCENARIO}" || test -f "${DEMO_MODE_TEST_PATH}" || (echo "Unknown demo-mode scenario: ${SCENARIO}"; exit 2)
	@mkdir -p "${DEMO_MODE_TEST_REPORTS_DIR}" "${DEMO_MODE_LOGS_DIR}"
	@rm -f "${DEMO_MODE_TEST_REPORTS_DIR}/results-demo-mode.xml"
	docker run ${DEMO_MODE_RUNNER_NAME_OPTION} ${DEMO_MODE_DOCKER_API_VERSION_OPTION} --rm -i --network=host \
	 -e PYTHONDONTWRITEBYTECODE=1 \
	 -e DEMO_MODE_HOST_TMP=/demo-mode-host-tmp \
	 -e DEMO_MODE_HOST_UID="$$(id -u)" \
	 -e DEMO_MODE_HOST_GID="$$(id -g)" \
	 -e DOCKER_CONFIG=/demo-mode-docker-config \
	 -e bamboo_planRepository_branchName \
	 -v $(CURDIR):$(CURDIR):ro \
	 -v ${DEMO_MODE_TEST_REPORTS_DIR}:${DEMO_MODE_TEST_REPORTS_DIR} \
	 -v ${DEMO_MODE_LOGS_DIR}:${DEMO_MODE_LOGS_DIR} \
	 -v ${DEMO_MODE_DOCKER_CONFIG_DIR}:/demo-mode-docker-config:ro \
	 -v /tmp:/demo-mode-host-tmp \
	 -v /var/run/docker.sock:/var/run/docker.sock \
	 -w $(CURDIR) ${ACCEPTANCE_TEST_IMAGE} \
	 python3 -m tests.demo_mode.utils.test_runner \
	 --color=yes -p no:cacheprovider -rs -s -v \
	 --confcutdir=tests/demo_mode \
	 --junitxml=${DEMO_MODE_TEST_REPORTS_DIR}/results-demo-mode.xml \
	 ${DEMO_MODE_TEST_PATH} ${DEMO_MODE_ONEZONE_IMAGE_OPTION} ${DEMO_MODE_ONEPROVIDER_IMAGE_OPTION}


##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	mkdir -p ${GENERATED_CLIENTS_ROOT}
	cd submodules/onezone_swagger && make python-client && cd generated/python && mv onezone_client ${GENERATED_CLIENTS_ROOT}
	cd submodules/onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ${GENERATED_CLIENTS_ROOT}
	cd submodules/oneprovider_swagger && make python-client && cd generated/python && mv oneprovider_client ${GENERATED_CLIENTS_ROOT}
	cd submodules/cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ${GENERATED_CLIENTS_ROOT}

##
## Clean
##

clean: clean_swaggers

clean_swaggers:
	cd submodules/onezone_swagger && make clean
	cd submodules/onepanel_swagger && make clean
	cd submodules/oneprovider_swagger && make clean
	cd submodules/cdmi_swagger && make clean
	rm -rf ${GENERATED_CLIENTS_ROOT}/onezone_client
	rm -rf ${GENERATED_CLIENTS_ROOT}/onepanel_client
	rm -rf ${GENERATED_CLIENTS_ROOT}/oneprovider_client
	rm -rf ${GENERATED_CLIENTS_ROOT}/cdmi_client

codetag-tracker:
	./bamboos/scripts/codetag-tracker.sh --branch=${BRANCH} --excluded-dirs=generated --excluded-files=.pylintrc


##
## Formatting
##

STATIC_ANALYSER_IMAGE := docker.onedata.org/python_static_analyser:v14
PYTHON_CONFIG := pyproject.toml
UID := $(shell id -u)
GID := $(shell id -g)

define docker_run
	docker run --rm -i -v $(CURDIR):$(CURDIR) -w $(CURDIR) -u $(UID):$(GID) $(STATIC_ANALYSER_IMAGE) $1
endef


ALL_FILES := tests/gui/steps tests/gui/meta_steps tests/gui/utils tests/gui/constants.py tests/gui/__init__.py tests/__init__.py \
 tests/mixed/steps tests/mixed/utils tests/mixed/__init__.py \
 tests/performance/__init__.py tests/performance/type_definitions.py tests/performance/test_*.py \
 tests/oneclient/steps tests/oneclient/meta_steps tests/oneclient/__init__.py tests/utils tests/upgrade \
 tests/demo_mode/utils tests/demo_mode/scenarios tests/demo_mode/environment.py \
 tests/demo_mode/persistence.py tests/demo_mode/comprehensive_example.py \
 tests/demo_mode/python_access.py tests/demo_mode/data.py tests/demo_mode/constants.py \
 tests/demo_mode/__init__.py
ALL_CONFTEST_FILES := tests/conftest.py tests/gui/conftest.py tests/mixed/conftest.py \
 tests/oneclient/conftest.py tests/performance/conftest.py tests/demo_mode/conftest.py
ALL_SCENARIO_FILES := tests/gui/scenarios tests/mixed/scenarios tests/oneclient/scenarios


format:
	# Select Ruff's "I" (isort) rules to sort imports before formatting.
	$(docker_run) ruff check --config $(PYTHON_CONFIG) --no-cache --select I --fix $(ALL_FILES) $(ALL_CONFTEST_FILES) $(ALL_SCENARIO_FILES)
	$(docker_run) ruff format --config $(PYTHON_CONFIG) --no-cache $(ALL_FILES) $(ALL_CONFTEST_FILES) $(ALL_SCENARIO_FILES)


format-check:
	# Check import sorting using Ruff's "I" (isort) rules.
	$(docker_run) ruff check --config $(PYTHON_CONFIG) --no-cache --select I $(ALL_FILES) $(ALL_CONFTEST_FILES) $(ALL_SCENARIO_FILES)
	$(docker_run) ruff format --config $(PYTHON_CONFIG) --no-cache --check $(ALL_FILES) $(ALL_CONFTEST_FILES) $(ALL_SCENARIO_FILES) || \
	 (echo "Code failed Ruff format checking. Please run 'make format' before committing your changes. "; exit 1)


##
## Static analysis
##

static-analysis:
	$(docker_run) ruff check --config $(PYTHON_CONFIG) --no-cache $(ALL_FILES)
	$(docker_run) ruff check --config $(PYTHON_CONFIG) --no-cache \
	--ignore=ARG,PLC0415,SLF001 $(ALL_CONFTEST_FILES)

# Rules ignored for conftest files:
# - ARG (unused arguments): pytest and pytest-bdd require fixed fixture and hook
#   signatures even when some injected arguments are unused.
# - PLC0415 (import outside top level): GUI fixtures defer imports to avoid
#   circular dependencies and keep platform-specific setup local.
# - SLF001 (private member access): WebDriver instances are deliberately stored
#   in pytest's private node state under `_driver` for sharing between fixtures
#   and hooks.

type-check:
	$(docker_run) mypy $(ALL_FILES) $(ALL_CONFTEST_FILES) --config-file=$(PYTHON_CONFIG)
