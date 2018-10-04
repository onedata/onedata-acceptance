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
TIMEOUT			   ?= 300

# TODO: image
test_gui_packages_one_env:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i docker.onedata.org/acceptance_gui:one_env_test --xvfb --xvfb-recording=${RECORDING_OPTION} -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE}  --reruns 1 --reruns-delay 10

# TODO: image
test_gui_sources_one_env:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i docker.onedata.org/acceptance_gui:one_env_test --xvfb --xvfb-recording=${RECORDING_OPTION} --sources -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE}  --reruns 1 --reruns-delay 10

test_mixed_packages_swaggers:
	${TEST_RUN} -t tests/mixed_swaggers/scenarios/${SUITE}.py --test-type mixed_swaggers -vvv --driver=${BROWSER} -i docker.onedata.org/acceptance_gui:one_env_test --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE} --reruns 0 --reruns-delay 10

test_mixed_sources_swaggers:
	${TEST_RUN} -t tests/mixed_swaggers/scenarios/${SUITE}.py --test-type mixed_swaggers -vvv --driver=${BROWSER} -i docker.onedata.org/acceptance_gui:one_env_test --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} --sources -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE} --reruns 1 --reruns-delay 10

test_mixed_oneclient:
	${TEST_RUN} -t tests/mixed_oneclient/scenarios/${SUITE}.py --test-type mixed_oneclient -vvv --driver=${BROWSER} -i docker.onedata.org/acceptance_gui:one_env_test --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE} --timeout ${TIMEOUT} --reruns 1 --reruns-delay 10

# TODO: IMAGE
test_oneclient_pkg:
	${TEST_RUN} --test-type acceptance -vvv --test-dir tests/acceptance/scenarios/${SUITE}.py -i docker.onedata.org/worker:one_env_test -k=${KEYWORDS} --oz-image=${OZ_IMAGE} --op-image=${OP_IMAGE}

##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	cd onezone_swagger && make python-client && cd generated/python && mv onezone_client ../../../tests/mixed_swaggers
	cd onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ../../../tests/mixed_swaggers
	cd oneprovider_swagger && make python-client && cd generated/python && mv oneprovider_client ../../../tests/mixed_swaggers
	cd cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ../../../tests/mixed_swaggers


##
## Clean
##

clean: clean_swaggers

clean_swaggers:
	rm -rf tests/mixed_swaggers/onezone_client
	rm -rf tests/mixed_swaggers/onepanel_client
	rm -rf tests/mixed_swaggers/oneprovider_client
	rm -rf tests/mixed_swaggers/cdmi_client
