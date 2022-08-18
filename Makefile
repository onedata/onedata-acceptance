ifdef IGNORE_XFAIL
TEST_RUN := ./test_run.py --ignore-xfail
else
TEST_RUN := ./test_run.py
endif

ifdef ENV_FILE
TEST_RUN := $(TEST_RUN) --env-file $(ENV_FILE)
endif

GIT_URL := $(shell git config --get remote.origin.url | sed -e 's/\(\/[^/]*\)$$//g')
GIT_URL := $(shell if [ "${GIT_URL}" = "file:/" ]; then echo 'ssh://git@git.plgrid.pl:7999/vfs'; else echo ${GIT_URL}; fi)
ONEDATA_GIT_URL := $(shell if [ "${ONEDATA_GIT_URL}" = "" ]; then echo ${GIT_URL}; else echo ${ONEDATA_GIT_URL}; fi)
export ONEDATA_GIT_URL

# FIXME: experimental images - change to production after code review
ACCEPTANCE_GUI_IMAGE := docker.onedata.org/acceptance_gui:chrome-104.1
ACCEPTANCE_MIXED_IMAGE := docker.onedata.org/acceptance_mixed:chrome-104.1

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
TIMEOUT			            ?= 300
REPEATS                     ?= 1
LOCAL_CHARTS_PATH           ?= ""
PULL_ONLY_MISSING_IMAGES    ?= ""
MIXED_TESTS_ROOT := $(shell pwd)/tests/mixed

ifdef bamboo_GUI_PKG_VERIFICATION
    GUI_PKG_VERIFICATION = --gui-pkg-verification
endif
ifdef PULL_ONLY_MISSING_IMAGES
    PULL_IMAGES_OPT = --pull-only-missing-images
endif

test_gui_pkg:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i ${ACCEPTANCE_GUI_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	-k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${PULL_IMAGES_OPT}

test_gui_src:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i ${ACCEPTANCE_GUI_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} --sources \
	 -k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${PULL_IMAGES_OPT}

test_mixed_pkg:
	PYTHONPATH=${MIXED_TESTS_ROOT} ${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i ${ACCEPTANCE_MIXED_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	 --env-file=${ENV_FILE} -k=${KEYWORDS} --repeats ${REPEATS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH}  --reruns 1 --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${PULL_IMAGES_OPT}

test_mixed_src:
	PYTHONPATH=${MIXED_TESTS_ROOT} ${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i ${ACCEPTANCE_MIXED_IMAGE} --xvfb --xvfb-recording=${RECORDING_OPTION} \
	--env-file=${ENV_FILE} --sources -k=${KEYWORDS} --repeats ${REPEATS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10 ${GUI_PKG_VERIFICATION} ${PULL_IMAGES_OPT}

test_oneclient_pkg:
	${TEST_RUN} --test-type oneclient -vvv --test-dir tests/oneclient/scenarios/${SUITE}.py -i ${ACCEPTANCE_MIXED_IMAGE} -k=${KEYWORDS} \
	 --repeats ${REPEATS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} ${PULL_IMAGES_OPT}

test_oneclient_src:
	${TEST_RUN} --test-type oneclient -vvv --test-dir tests/oneclient/scenarios/${SUITE}.py -i ${ACCEPTANCE_MIXED_IMAGE} -k=${KEYWORDS} \
	 --repeats ${REPEATS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --sources ${PULL_IMAGES_OPT}

test_onedata_fs:
	${TEST_RUN} --test-type onedata_fs -vvv --test-dir tests/onedata_fs/scenarios/test_unit_tests.py -i ${ACCEPTANCE_MIXED_IMAGE} -k=${KEYWORDS} \
     --repeats ${REPEATS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} ${PULL_IMAGES_OPT}

test_performance_pkg:
	${TEST_RUN} --test-type performance -vvv --test-dir tests/performance --image ${ACCEPTANCE_MIXED_IMAGE} -k=${KEYWORDS} --local-charts-path=${LOCAL_CHARTS_PATH} ${PULL_IMAGES_OPT}

test_performance_src:
	${TEST_RUN} --test-type performance -vvv --test-dir tests/performance --image ${ACCEPTANCE_MIXED_IMAGE} -k=${KEYWORDS} --local-charts-path=${LOCAL_CHARTS_PATH} --sources ${PULL_IMAGES_OPT}


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
	./bamboos/scripts/codetag-tracker.sh --branch=${BRANCH} --excluded-dirs=
