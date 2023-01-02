# Onedata Acceptance Tests

Repository with all acceptance tests of the Onedata system.

Tests are run on a Onedata deployment set up using one-env on a Kubernetes cluster.
As the testing framework, `pytest` with `pytest-bdd` extension is used.


# Important notes

* Currently, all selenium-based tests that use a web browser run on Google Chrome.
  Other browsers are only *theoretically* supported.

* It is recommended to use Ubuntu 20.04+. Ubuntu 18.04+ is a slightly worse
  choice, but surely a working one. Setting up a deployment and running tests in 
  macOS is possible, but problematic; see
  [macOS deployment setup](macos_deployment_setup.md) for tips.


# Prerequisites

* python 3.6+ (3.8+ is recommended)
* docker
* kubernetes cluster (e.g. minikube)

By default, the tests are run using a dockerized testing toolkit. All the 
required libraries are preinstalled in the docker image. However, it is possible
to run some tests using a locally installed testing toolkit, as described in
[tests/gui/README.md](./tests/gui/README.md).


# Running acceptance tests

In general, there are two ways of running acceptance tests:

1. **Using `Makefile`** (recommended):

   ```
   make ENV_FILE=$ENV SUITE=$SUITE OPTS=$OPTS $test_type_identifier
   ```
   - `$SUITE` - file name from `tests/*/scenarios` without extension; determines 
     the test suite to run. 
   - `$ENV_FILE` - file name from `tests/*/environments` without extension; determines 
     the env-file (description of Onedata deployment). If not specified, default 
     [1oz_1op_deployed.yaml](tests/gui/environments/1oz_1op_deployed.yaml) will be used.
   - `$OPTS` - optional, any of `./test_run.py` parameters
     (see **Useful test_run parameters** section).
   - `$test_type_identifier` - determines the type of tests; one of: `test_gui`,   
     `test_mixed`, `test_oneclient`.

2. **Using `./test_run.py`** (when advanced customization is required):

    Makefile essentially uses `./test_run.py` with default parameters. If needed,
    you can use the command directly with desired parameters.

The exact procedure of running tests is described in:
* [tests/gui/README.md](./tests/gui/README.md) for **GUI** tests,
* [tests/mixed/README.md](./tests/mixed/README.md) for **Mixed** tests
  (these tests use GUI, REST and Oneclient at the same time)
* [tests/oneclient/README.md](./tests/oneclient/README.md) for **Oneclient** tests.

For use in CI (Bamboo), see Bamboo Specs files placed in [bamboo-specs](bamboo-specs)
directory in root of this repository. These specs use the `Makefile` targets directly.


# Reusing an existing deployment

If there is a pre-existing deployment, it will be automatically detected and
used for the test. The deployment may be started manually (see the section that follows)
before running the test command. **Note**, however, that by default, the deployment 
**will be cleaned** after the test. To prevent that, use the `--no-clean` option.

Running tests with `--no-clean` option is the optimal way to do consecutive
runs - the environment is set up once and then reused.


# Starting a Onedata deployment

In typical scenarios, the deployment is started automatically as a part of the
test procedure. If needed, it can be set up manually in order to run the tests 
on a preexisting deployment.

The manual start of Onedata deployment is described in the following
document: [one-env guide](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md).

To start Onedata deployment, navigate to the `one-env` directory in 
[one-env](https://git.onedata.org/projects/VFS/repos/one-env/browse) repository
or to [one_env](one_env) submodule in the onedata-acceptance repository and run:

 ```
./onenv up -f test_env_config.yaml 
 ```


**Note:** For above command to work, you need to build submodules using 
`make submodules` command (invoke from repo root).

Example of a 2 provider deployment with specified onezone and oneprovider images:
```bash
./onenv up -f -pi docker.onedata.org/oneprovider-dev:develop -zi docker.onedata.org/onezone-dev:develop ../tests/gui/environments/1oz_2op_deployed.yaml
```


# Useful test_run parameters

* `--no-clean` - prevents deleting Onedata deployment after tests - makes consecutive runs much faster
  (a preexisting deployment is detected and reused) 
* `--test-type gui` - determines the test type.
* `-t tests/gui` - set the path with test cases to gui tests. For example, 
  you can filter out tests to single suite using scenario file:
  `-t tests/gui/scenarios/test_onezone_basic.py`.
* `--driver=Chrome` - set the browser to test in
* `-i onedata/gui_builder:latest` - use Docker image with dependencies for GUI tests
  (i.e. Python, Selenium, Xvfb, Chrome)
* `--xvfb` - starts Xvfb, a virtual display server, that makes tests headless (without opening local browser window)
* `--xvfb-recording=<all|none|failed>` - optional, record all or none or failed tests
  as movies and save them to `<logdir>/movies`
* `--env-file=1oz_1op_not_deployed_embedded_ceph` - specifies `env_file` that will be used to start deployment if there is no active deployment 
* `--local` - uses locally installed testing toolkit instead of dockerized one
* `--no-pull` - prevents from downloading docker images (by default all tests scenarios force pulling docker
   images even if they are already present on host machine.)
* `-k="test_posix_storage_operations"` - used to select specific test, runs tests 
  which contain names that match given string expression (case-insensitive). For more
  information see: [pytest documentation](https://docs.pytest.org/en/6.2.x/usage.html#specifying-tests-selecting-tests).
* `--oc-image=docker.onedata.org/oneclient-dev:develop` - used to specify oneclient service docker image
* `--sources` - optional, if used, Onedata deployment starts using sources. Sources have
  to be located in appropriate directories.

**Parameters:** (for advanced usage)

* `--no-mosaic-filter` - optional, if set, videos of tests using multiple browsers will
  be recorded as different video for each browser (mosaic video created by default)
* `--update-etc-hosts` <!--- TODO VFS-10023 make description more specific after investigating this flag -->-
  adds entries to `/etc/hosts` for all pods in deployment.
  When using this option script has to be run with root privileges.   
* `--add-test-domain` <!--- TODO VFS-10025 make description more specific after investigating this flag -->-
  when running tests on local machine, option for adding entries to
  `/etc/hosts` is turned off by default. This may cause that some test will fail.
  You can enable adding entries to `/etc/hosts` using `--add-test-domain` option, or add
  entries manually.

**Note:** using `--add-test-domain`, `--update-etc-hosts` flags can be problematic due to permissions of `/etc/hosts` file.
  The experimental and **not safe** method is to do `sudo chmod go+w /etc/hosts` locally and
  share `/etc` directory in docker.
  Please contact our support if you have issues with updating `/etc/hosts` for testing.


# Test debugging

Python debugger `pdb` is a very handy tool when it comes to test debugging. 

The typical usage is to insert:
```
import pdb
pdb.set_trace()
```
at the location you want to break into the debugger, and then run test. 
When the program stops, you can step through the code and then continue test
using `c`(continue) command.

Some useful debugger commands:
* `c(ont(inue))` - continue execution, only stop when a breakpoint is encountered.
* `q(uit)` - quit from the debugger. The program being executed is aborted.
* `n(ext)`- continue execution until the next line in the current function is reached or it returns.

For more information about Python debugger see : [pdb documentation](https://docs.python.org/3/library/pdb.html)

In test scenario you can add `(Given-When-Then) trace`
step, which works exactly the same, and stops test between steps.


# Known issues

1. Some of the `test_run.py` flags are outdated and not used. They should be 
checked and eventually removed. <!--- VFS-10177  remove outdated test-run flags -->
2. **Known issues** section in [GUI README](tests/gui/README.md).
3. **Known issues** section in [Mixed README](tests/mixed/README.md).
4. **Known issues** section in [Oneclient README](tests/oneclient/README.md).
