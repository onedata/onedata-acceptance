# Oneclient acceptance tests

## Running tests using Makefile

To run oneclient tests use:

```
make SUITE=$SUITE ENV_FILE=$ENV TIMEOUT=$TIMEOUT IGNORE_XFAIL=1 test_oneclient_pkg
```
Commands for exact tests suites can be found in [bamboo-specs/oneclient](../../bamboo-specs/oneclient-acceptance-pkg.yml).

For more information about running tests using `make` see  [gui/README](../gui/README.md#Running-tests-using-Makefile)

**Example:**
```
make SUITE=test_luma_provider ENV_FILE=singleprovider_multistorage TIMEOUT=720 IGNORE_XFAIL=1 OPTS="-k="test_posix_storage_operations"" test_oneclient_pkg
```
Some useful options for `OPTS`:
* `--no-clean` - if present prevents cleaning Onedata deployment
* `-k="test_posix_storage_operations"` - used to select specific test
* `--oc-image=docker.onedata.org/oneclient-dev:develop` - used to specify oneclient service docker image


## Running mixed tests using test_run

```
./test_run.py -t tests/oneclient --test-type oneclient -i onedata/acceptance_mixed:latest --env-file=$ENV
```
Where:
* `-t` - standard `./test_run.py` parameter to set the test cases path to oneclient luma provider tests
* `--test-type acceptance` - set the test type use by core Onedata test helpers
* `-i onedata/worker` - use Docker image with dependencies for oneclient tests
* `--env-file=singleprovider_multistorage` - path to description of test environment in .yaml file

**Example:**
```
./test_run.py -t tests/oneclient/scenarios/test_luma_provider.py --test-type oneclient -i onedata/acceptance_mixed:latest --env-file=singleprovider_multistorage
```

# Known issues

1. An example command to run Oneclient Acceptance test suite using sources:
   ```
    ./test_run.py -t tests/oneclient/scenarios/test_multi_reg_file_CRUD.py 
   --test-type oneclient -i onedata/acceptance_mixed:latest 
   --env-file multiprovider_proxy --sources
   ```

2. If you encounter problems with tests using oneclient and the logs contain
   errors such as "connection refused" or some rpyc connection errors, it is
   probable that you did not provide a `docker.onedata.org/oneclient-dev:*` 
   image. A `dev` image **is required**, the `docker.onedata.org/oneclient:*` 
   image won't work.

3. If there are problems with setting up an environment for tests that use 
   oneclient, it is possible that some remnants of previous deployments are
   the cause. Try running `onenv clean`, and if it does not help,
   `helm delete dev; helm delete patch-dev`.

4.  `--local` flag is not working in tests that use Oneclient. There is a 
     problem with client mounting (connecting to rpyc).
