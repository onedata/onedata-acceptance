# Mixed acceptance tests

Mixed tests are tests that use GUI, REST and Oneclient.

**Note:** We recommend reading [tests/gui/README.md](../gui/README.md) to 
better understand mixed tests, which are basing on GUI tests.

# Running mixed tests using Makefile 

To run mixed test use:
```
make ENV_FILE=$ENV SUITE=$SUITE BROWSER=Chrome TIMEOUT=600 test_mixed_pkg
```
**Example:**
```
make SUITE=test_permission_posix_multi ENV_FILE=1oz_1op_2oc OPTS="--no-clean --no-pull" test_mixed_pkg
```
Commands for exact tests suites can be found in [bamboo-specs/mixed](../../bamboo-specs/mixed-acceptance-src.yml).

For more information about running tests using `make` see  [README](../../README.md#Running-acceptance-tests)

# Running mixed tests using test_run

Running Mixed tests must be preceded by `make build_swaggers` — this could be 
handled automatically on the Makefile level.

## Running tests on automatic Onedata deployment using a dockerized testing toolkit:

```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --xvfb --xvfb-recording=failed --env-file=$ENV
```
**Example:** running single test suite (from one specified file):
```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed/scenarios/test_permission_posix_multi.py --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --xvfb --xvfb-recording=failed --env-file=1oz_1op_2oc
```

## Running tests on a preexisting Onedata deployment:

**Note:** You can specify tests file and `env_file` in the same way as in above example.

### Using a dockerized testing toolkit:

for REST, web GUI and oneclient test
```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --no-clean --xvfb --xvfb-recording=failed
```

### Using a locally installed testing toolkit:

for REST and web GUI test (does not work with oneclient tests):
```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome --local --no-clean -v
```

more about starting tests with `--local` flag in [gui/README.md](../gui/README.md#Using-a-locally-installed-testing-toolkit) 

# Known issues

1. If you encounter `ImportError`, try to preceded running mixed tests by command: 
`make build_swaggers` (this could be handled automatically on the Makefile level).
2. [GUI known issues](../gui/README.md#known-issues)
3. [Oneclient known issues](../oneclient/README.md#known-issues)