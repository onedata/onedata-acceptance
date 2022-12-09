# Mixed acceptance tests

Mixed tests are tests that use GUI, REST and Oneclient.

**Note:** We recommend reading [tests/gui/README.md](../gui/README.md) to 
better understand mixed tests, which are basing on GUI tests.

# Running mixed tests using Makefile 

Running Mixed tests must be preceded by `make build_swaggers`.

To run mixed test use:

```
make ENV_FILE=$ENV SUITE=$SUITE BROWSER=Chrome TIMEOUT=600 test_mixed
```
**Example:**
```
make SUITE=test_permission_posix_multi ENV_FILE=1oz_1op_2oc OPTS="--no-clean --no-pull" test_mixed
```
Commands for exact tests suites can be found in 
[bamboo-specs/mixed](../../bamboo-specs/mixed-acceptance-src.yml).

For more information about running tests using `make` see 
**Running acceptance tests** section in [README](../../README.md)

# Running mixed tests using test_run

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

more about starting tests with `--local` flag in **Using a locally installed
testing toolkit** section in [gui/README.md](../gui/README.md) 

# Known issues

1. If you encounter `ImportError`, try to precede running mixed tests by command: 
`make build_swaggers` (this could be handled automatically when running tests using Makefile). 
<!--- TODO VFS-10239 build swaggers, if needed, automatically when running tests using Makefile  -->
2. **Known issues** section in [GUI README](../gui/README.md)
3. **Known issues** section in [Oneclient README](../oneclient/README.md)