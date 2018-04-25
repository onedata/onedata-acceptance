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

##
## Submodules
##

branch = $(shell git rev-parse --abbrev-ref HEAD)
submodules:
	./onedata_submodules.sh init ${submodule}
	./onedata_submodules.sh update ${submodule}

checkout_getting_started:
	./onedata_submodules.sh init getting_started
	./onedata_submodules.sh update --remote getting_started

##
## Test
##

RECORDING_OPTION   ?= failed
BROWSER            ?= Chrome
ENV_FILE           ?= tests/gui/environments/1oz_1op_deployed.yaml


test_gui_packages_one_env:
	${TEST_RUN} -t tests/gui/scenarios/${SUITE}.py --test-type gui -vvv --driver=${BROWSER} -i onedata/acceptance_gui:latest --xvfb --xvfb-recording=${RECORDING_OPTION} --env-file=${ENV_FILE} -k=${KEYWORDS}

##
## Build python REST clients generated from swaggers. (used in mixed tests)
##

build_swaggers:
	cd onezone_swagger && make python-client && cd generated/python && mv onezone_client ../../../tests/mixed_swaggers
	cd onepanel_swagger && make python-client && cd generated/python && mv onepanel_client ../../../tests/mixed_swaggers
	cd oneprovider_swagger && make python-client && cd generated/python && mv onepprovider_client ../../../tests/mixed_swaggers
	cd cdmi_swagger && make python-client  && cd generated/python && mv cdmi_client ../../../tests/mixed_swaggers
