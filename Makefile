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

RECORDING_OPTION   ?= failed
BROWSER            ?= Chrome
OZ_IMAGE           ?= ""
OP_IMAGE           ?= ""
OC_IMAGE           ?= ""
REST_CLI_IMAGE     ?= ""
LUMA_IMAGE         ?= ""
TIMEOUT			   ?= 300
LOCAL_CHARTS_PATH  ?= ""

test_gui_pkg:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v6 --xvfb --xvfb-recording=${RECORDING_OPTION} \
	-k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10

test_gui_src:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v6 --xvfb --xvfb-recording=${RECORDING_OPTION} --sources \
	 -k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10

test_mixed_pkg:
	${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v6 --xvfb --xvfb-recording=${RECORDING_OPTION} \
	 --env-file=${ENV_FILE} -k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 0 --reruns-delay 10

test_mixed_src:
	${TEST_RUN} -t tests/mixed/scenarios/${SUITE}.py --test-type mixed -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v6 --xvfb --xvfb-recording=${RECORDING_OPTION} \
	--env-file=${ENV_FILE} --sources -k=${KEYWORDS} --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH} --reruns 1 --reruns-delay 10

test_oneclient_pkg:
	${TEST_RUN} --test-type oneclient -vvv --test-dir tests/oneclient/scenarios/${SUITE}.py -i onedata/acceptance_mixed:v6 -k=${KEYWORDS} \
	 --timeout ${TIMEOUT} --local-charts-path=${LOCAL_CHARTS_PATH}

##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	cd onezone_swagger && make python-client && cd generated/python && mv onezone_client ../../../tests/mixed
	cd onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ../../../tests/mixed
	cd oneprovider_swagger && make python-client && cd generated/python && mv oneprovider_client ../../../tests/mixed
	cd cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ../../../tests/mixed


##
## Clean
##

clean: clean_swaggers

clean_swaggers:
	rm -rf tests/mixed/onezone_client
	rm -rf tests/mixed/onepanel_client
	rm -rf tests/mixed/oneprovider_client
	rm -rf tests/mixed/cdmi_client
