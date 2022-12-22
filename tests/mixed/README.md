# Mixed acceptance tests

Acceptance tests using the Web GUI, REST and Oneclient.


# Development

Please read this document before you start writing or modifying any tests.

**Note:** we recommend reading [tests/gui/README.md](../gui/README.md) first to 
better understand mixed tests, which are based on GUI tests.


# Running mixed tests using Makefile 

Running Mixed tests must be preceded by `make build_swaggers`. Then:

```
make ENV_FILE=$ENV SUITE=$SUITE test_mixed
```
**Example:**
```
make SUITE=test_permission_posix_multi ENV_FILE=1oz_1op_2oc OPTS="--no-clean --no-pull" test_mixed
```
Commands for exact tests suites can be found in 
[bamboo-specs/mixed](../../bamboo-specs/mixed-acceptance-src.yml).

For more information about running tests using `make`, see
**Running acceptance tests** section in the main [README](../../README.md).


# Running tests using test_run (advanced)

The test_run.py command is essentially invoked by Makefile, but using it directly
allows better parameterization and overcoming of some known issues.

**Note:** all examples use the `--no-clean` option, make sure to remove it if you
require a fresh deployment every run.

## Running tests using a dockerized testing toolkit

```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed \
    --driver=Chrome -i onedata/acceptance_mixed:latest --xvfb --xvfb-recording=failed \
    --env-file=$ENV --no-clean
```

To run a single test suite:

```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed/scenarios/test_permission_posix_multi.py \
    --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest \
    --xvfb --xvfb-recording=failed --env-file=1oz_1op_2oc --no-clean
```

## Running tests using a locally installed testing toolkit

**Only for REST and web GUI tests**, because `--local` mode currently does not support Oneclient tests:

```
PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed \
    --driver=Chrome --local --no-clean -v
```

More about starting tests with `--local` flag can be found in **Running tests using a locally
installed testing toolkit** section in [tests/gui/README.md](../gui/README.md).


# Known issues

1. If you encounter `ImportError`, try to precede running mixed tests by command: 
`make build_swaggers` (this could be handled automatically when running tests using Makefile). 
<!--- TODO VFS-10239 build swaggers, if needed, automatically when running tests using Makefile  -->
2. The `--local` flag does not work for suites using Oneclient.
3. **Known issues** section in [GUI README](../gui/README.md).
4. **Known issues** section in [Oneclient README](../oneclient/README.md).
