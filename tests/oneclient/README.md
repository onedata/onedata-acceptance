# Oneclient acceptance tests

Acceptance tests using the Oneclient: a fuse-based Onedata client with POSIX
interface.


# Development

Please read this document before you start writing or modifying any tests.


# Running tests using Makefile

```
make SUITE=$SUITE ENV_FILE=$ENV IGNORE_XFAIL=1 test_oneclient
```
Commands for exact tests suites can be found in 
[bamboo-specs/oneclient](../../bamboo-specs/oneclient-acceptance-pkg.yml).

For more information about running tests using `make`, see
**Running acceptance tests** section in the main [README](../../README.md).

**Example:**
```
make SUITE=test_luma_provider ENV_FILE=singleprovider_multistorage TIMEOUT=720 \
    IGNORE_XFAIL=1 OPTS="-k="test_posix_storage_operations"" test_oneclient --no-clean
```
In `OPTS`, any of `./test_run.py` parameters can be passed (see **Useful test_run 
parameters** section in the main [README](../../README.md).

Some useful options used mostly in `oneclient` tests:
* `-k="test_posix_storage_operations"` - selects a specific test
* `--oc-image=docker.onedata.org/oneclient-dev:develop` - specifies Oneclient docker image


# Running tests using test_run (advanced)

The test_run.py command is essentially invoked by Makefile, but using it directly
allows better parameterization and overcoming of some known issues.

**Note:** all examples use the `--no-clean` option, make sure to remove it if you
require a fresh deployment every run.

```
./test_run.py -t tests/oneclient --test-type oneclient \ 
    -i onedata/acceptance_mixed:latest --env-file=$ENV --no-clean
```
Where:
* `-t` - standard `./test_run.py` parameter to set the test cases path to Oneclient luma provider tests
* `--test-type oneclient` - set the test type use by core Onedata test helpers
* `-i onedata/acceptance_mixed:latest` - use Docker image with dependencies for Oneclient tests
* `--env-file=$ENV` - path to file from [environments](environments), without extension.

**Example:**
```
./test_run.py -t tests/oneclient/scenarios/test_luma_provider.py \
   --test-type oneclient -i onedata/acceptance_mixed:latest \
   --env-file=singleprovider_multistorage --no-clean
```

## Running Oneclient test using sources

To run tests using sources, you need to place sources for `oneclient`, 
`onepanel`, `oz_worker`, `op-worker`, `cluster-manager` in one of these 
directories: 
* [one_env](../../one_env) directory,
* onedata-acceptance repo root dir,
* your home directory.

To download sources, you can go to
[bamboo.onedata.org/allPlans](https://bamboo.onedata.org/allPlans.action) and find 
certain plan (e.g. [op-worker](https://bamboo.onedata.org/browse/BAM-PROV)). 
Then from artifacts, in the latest build, you can download compressed file 
(which you must unzip).

An example command to run Oneclient acceptance test suite using sources:
```
./test_run.py -t tests/oneclient/scenarios/test_multi_reg_file_CRUD.py \
   --test-type oneclient -i onedata/acceptance_mixed:latest \
   --env-file=multiprovider_proxy --sources --no-clean
```
# Known issues

1. If you encounter problems with tests using Oneclient and the logs contain
   errors such as "connection refused" or some rpyc connection errors, it is
   probable that you did not provide a `docker.onedata.org/oneclient-dev:*` 
   image. A `dev` image **is required**, the `docker.onedata.org/oneclient:*` 
   image won't work.

2. If there are problems with setting up Onedata deployment for tests that use
   Oneclient, it is possible that some remnants of previous deployments are
   the cause. Try running `onenv clean`, and if it does not help,
   `helm delete dev; helm delete patch-dev`.

3.  `--local` flag is not working in tests that use Oneclient. There is a 
     problem with client mounting (connecting to rpyc).
