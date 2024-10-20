TEST_RUN := ./test_run.py

ifdef ENV_FILE
TEST_RUN := $(TEST_RUN) --env-file $(ENV_FILE)
endif

GIT_URL := $(shell git config --get remote.origin.url | sed -e 's/\(\/[^/]*\)$$//g')
GIT_URL := $(shell if [ "${GIT_URL}" = "file:/" ]; then echo 'ssh://git@git.plgrid.pl:7999/vfs'; else echo ${GIT_URL}; fi)
ONEDATA_GIT_URL := $(shell if [ "${ONEDATA_GIT_URL}" = "" ]; then echo ${GIT_URL}; else echo ${ONEDATA_GIT_URL}; fi)
export ONEDATA_GIT_URL

ACCEPTANCE_TEST_IMAGE := onedata/acceptance_tests:v1.115

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
REPEATS                     ?= 1
RERUNS                      ?= 1
LOCAL_CHARTS_PATH           ?= ""
PULL_ONLY_MISSING_IMAGES    ?= ""
FILE_MODE                   ?= regular
MIXED_TESTS_ROOT := $(shell pwd)/tests/mixed

ifdef bamboo_GUI_PKG_VERIFICATION
    GUI_PKG_VERIFICATION = --gui-pkg-verification
endif

# TODO VFS-9779 - reorganize test targets after introducing bamboo specs
.PHONY: test_gui, test_gui_pkg, test_gui_src
.PHONY: test_mixed, test_mixed_pkg, test_mixed_src
.PHONY: test_oneclient, test_oneclient_pkg, test_oneclient_src
.PHONY: test_performance, test_performance_pkg, test_performance_src
.PHONY: test_upgrade
.PHONY: format

test_gui:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i ${ACCEPTANCE_TEST_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	-k=${KEYWORDS} --timeout ${TIMEOUT} --reruns ${RERUNS} --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${SOURCES} ${OPTS}

test_gui_pkg: test_gui
test_gui_src: SOURCES = --sources
test_gui_src: test_gui

test_mixed:
	PYTHONPATH=${MIXED_TESTS_ROOT} ${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i ${ACCEPTANCE_TEST_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	 --env-file=${ENV_FILE} -k=${KEYWORDS} --repeats ${REPEATS} --timeout ${TIMEOUT} --reruns ${RERUNS} --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${SOURCES} ${OPTS}

test_mixed_pkg: test_mixed
test_mixed_src: SOURCES = --sources
test_mixed_src: test_mixed

test_oneclient:
	${TEST_RUN} --test-type oneclient -vvv --test-dir tests/oneclient/scenarios/${SUITE}.py -i ${ACCEPTANCE_TEST_IMAGE} -k=${KEYWORDS} \
	 --repeats ${REPEATS} --timeout ${TIMEOUT} --file-mode ${FILE_MODE} ${SOURCES} ${OPTS}

test_oneclient_pkg: test_oneclient
test_oneclient_src: SOURCES = --sources
test_oneclient_src: test_oneclient

test_performance:
	${TEST_RUN} --test-type performance -vvv --test-dir tests/performance --image ${ACCEPTANCE_TEST_IMAGE} -k=${KEYWORDS} ${SOURCES} ${OPTS}

test_performance_pkg: test_performance
test_performance_src: SOURCES = --sources
test_performance_src: test_performance

test_upgrade:
	${TEST_RUN} --ignore-xfail --test-type upgrade -vvv --test-dir tests/upgrade --image ${ACCEPTANCE_TEST_IMAGE} --timeout ${TIMEOUT} --local-charts-path="" --pull-only-missing-images --env-file=tests/upgrade/configs/"${CONFIG_FILE}".yaml


##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	cd onezone_swagger && make python-client && cd generated/python && mv onezone_client ${MIXED_TESTS_ROOT}
	cd onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ${MIXED_TESTS_ROOT}
	cd oneprovider_swagger && make python-client && cd generated/python && mv oneprovider_client ${MIXED_TESTS_ROOT}
	cd cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ${MIXED_TESTS_ROOT}

##
## Clean
##

clean: clean_swaggers

clean_swaggers:
	cd onezone_swagger && make clean
	cd onepanel_swagger && make clean
	cd oneprovider_swagger && make clean
	cd cdmi_swagger && make clean
	rm -rf ${MIXED_TESTS_ROOT}/onezone_client
	rm -rf ${MIXED_TESTS_ROOT}/onepanel_client
	rm -rf ${MIXED_TESTS_ROOT}/oneprovider_client
	rm -rf ${MIXED_TESTS_ROOT}/cdmi_client

codetag-tracker:
	./bamboos/scripts/codetag-tracker.sh --branch=${BRANCH} --excluded-files=.pylintrc


##
## Formatting
##

STATIC_ANALYSER_IMAGE := "docker.onedata.org/python_static_analyser:v8"
ALL_FILES := tests/gui/steps tests/gui/meta_steps tests/gui/utils tests/gui/__init__.py tests/__init__.py \
 tests/mixed/steps tests/mixed/utils tests/mixed/__init__.py \
 tests/oneclient/steps tests/oneclient/__init__.py
ALL_CONFTEST_FILES := tests/conftest.py tests/gui/conftest.py tests/mixed/conftest.py tests/oneclient/conftest.py
ALL_SCENARIO_FILES := tests/gui/scenarios tests/mixed/scenarios tests/oneclient/scenarios
FILES_TO_FORMAT := $(ALL_FILES) $(ALL_CONFTEST_FILES) $(ALL_SCENARIO_FILES)
LINTER_DOCKER_RUN := docker run --rm -i -v `pwd`:`pwd` -w `pwd` $(STATIC_ANALYSER_IMAGE)


format:
	$(LINTER_DOCKER_RUN) isort $(FILES_TO_FORMAT) --settings-file tests/configs/.pyproject.toml
	$(LINTER_DOCKER_RUN) black $(FILES_TO_FORMAT) --config tests/configs/.pyproject.toml


black-check:
	$(LINTER_DOCKER_RUN) black $(FILES_TO_FORMAT) --check --config tests/configs/.pyproject.toml || \
	 (echo "Code failed Black format checking. Please run 'make format' before commiting your changes. "; exit 1)


##
## Static analysis
##

static-analysis:
	$(LINTER_DOCKER_RUN) pylint $(ALL_FILES) --output-format=colorized --recursive=y --rcfile=tests/configs/.pylintrc
	$(LINTER_DOCKER_RUN) pylint $(ALL_CONFTEST_FILES) --output-format=colorized --recursive=y \
	--disable=redefined-outer-name,import-outside-toplevel,protected-access,unused-argument --rcfile=tests/configs/.pylintrc
