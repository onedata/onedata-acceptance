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

artifact: artifact_op_worker artifact_oz_worker artifact_cluster_manager artifact_onepanel

artifact_op_worker:
	$(call unpack, op_worker)

artifact_oz_worker:
	$(call unpack, oz_worker)

artifact_cluster_manager:
	$(call unpack, cluster_manager)

artifact_onepanel:
	$(call unpack, onepanel)


##
## Submodules
##

branch = $(shell git rev-parse --abbrev-ref HEAD)
submodules:
	git submodule init ${submodule}
	git submodule update ${submodule}

checkout_getting_started:
	git submodule init getting_started
	git submodule update --remote getting_started

##
## Test
##

RECORDING_OPTION   ?= failed
BROWSER            ?= Chrome
ENV_FILE           ?= tests/gui/environments/1oz_1op_deployed.yaml
OZ_IMAGE           ?= ""
OP_IMAGE           ?= ""

test_gui_packages_one_env:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v2 --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE}  --reruns 1 --reruns-delay 10

test_gui_sources_one_env:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v2 --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} --sources -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE}  --reruns 1 --reruns-delay 10

test_mixed_packages_swaggers:
	${TEST_RUN} -t tests/mixed_swaggers/scenarios/${SUITE}.py --test-type mixed_swaggers -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v2 --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE} --reruns 1 --reruns-delay 10

test_mixed_sources_swaggers:
	${TEST_RUN} -t tests/mixed_swaggers/scenarios/${SUITE}.py --test-type mixed_swaggers -vvv --driver=${BROWSER} -i onedata/acceptance_gui:v2 --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} --sources -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE} --reruns 1 --reruns-delay 10


##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	cd onezone_swagger && make python-client && cd generated/python && mv onezone_client ../../../tests/mixed_swaggers
	cd onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ../../../tests/mixed_swaggers
	cd oneprovider_swagger && make python-client && cd generated/python && mv oneprovider_client ../../../tests/mixed_swaggers
	cd cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ../../../tests/mixed_swaggers
