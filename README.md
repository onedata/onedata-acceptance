# Onedata Acceptance Tests

This is the code repository containing acceptance tests for Onedata. \
It uses one-env for creating Onedata deployment running on kubernetes

# Important notes

- Currently, for testing, only Google Chrome is used and well tested. 
You can use other browsers, but notice, this is not supported.    
- It is recommended to use Ubuntu 20.04+. Ubuntu 18.04+ is a slightly worse
choice, but surely working one. Setting up deployment 
and running tests in macOS is not officially supported. If you still want to run tests on macOS, see 
[macOS deployment setup](macos_deployment_setup.md) for tips.

# Running acceptance tests

Acceptance tests can be run in few ways (which are described in our READMEs):

## 1. Using `Makefile`.

Generic `make` command to run tests:
```
make ENV_FILE=$ENV SUITE=$SUITE BROWSER=Chrome OPTS=$OPTS TIMEOUT=$TIMEOUT $test_type
```

- `SUITE` - determines tests. For example, for GUI tests, file name 
from [scenarios](tests/gui/scenarios), without extension. 
- `ENV_FILE` - determines env-file (description of Onedata deployment). For
example, for GUI tests, path to file from [environments](tests/gui/environments), 
without extension (if not specified, default 
[1oz_1op_deployed.yaml](tests/gui/environments/1oz_1op_deployed.yaml) 
will be used).
- `OPTS` - optional, any of `./test_run.py` parameters
(see [useful parameters](README.md#Useful-test_run-parameters))
- `TIMEOUT` - wait timeout
- `test_type` - type of tests e.g. `test_gui_pkg`

## 2. Using `./test_run.py`:

Makefile is using `./test_run.py` with specified, default parameters. You can use and 
parameterize `./test_run.py` on your own.  

1. ### Running tests on automatic Onedata deployment using a dockerized testing toolkit
   Using this method, the Onedata deployment will be set up automatically.
2. ### Running tests on a preexisting Onedata deployment:
   1. **Using a dockerized testing toolkit** \
      Existing Onedata deployment installation will be used if available.
   2. **Using a locally installed testing toolkit.**\
      Running test this way greatly helps with debug because you see test "live".

For use in CI (Bamboo) see Bamboo Specs files placed in [bamboo-specs](bamboo-specs) directory in root of this repository. These specs use `Makefile` targets directly.

The exact procedure of running tests is described in:
* [tests/gui/README.md](./tests/gui/README.md) for **GUI** tests
* [tests/mixed/README.md](./tests/mixed/README.md) for **Mixed** tests 
(these are tests that use GUI, REST and Oneclient)
* [tests/oneclient/README.md](./tests/oneclient/README.md) for **Oneclient** tests


## Testing toolkit

All tools that are needed to run GUI and Mixed tests:
* Python 3.8
* required Python packages: [gui/requirements.txt](tests/gui/requirements.txt) 
* Google Chrome
* xclip
* chromedriver

Tools that are needed to run Oneclient test:
* Python 3.8
* required Python packages: pytest, pytest-bdd


# Starting Onedata deployment

The manual start of Onedata deployment is described in the following
document: [one-env guide](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md)

To start Onedata deployment navigate to `one-env` directory in 
[one-env](https://git.onedata.org/projects/VFS/repos/onedev/browse) repository
or to [one_env](one_env) submodule in this repository and run:

 ```
./onenv up -f test_env_config.yaml 
 ```

Example of 2-provider deployment with specified onezone and oneprovider images:
```bash
./onenv up -f -pi docker.onedata.org/oneprovider-dev:develop -zi docker.onedata.org/onezone-dev:develop ../tests/gui/environments/1oz_2op_deployed.yaml
```


## Some useful information about Starting Onedata deployment to run tests

### Onedata deployment setup for tests using local machines

We recommend using **Python 3.8**. Python 3.7 and Python 3.6 are also supported.

These tests will be run using `py.test` runner on local machine.
Required Python packages to install (e.g. using `pip install`) are listed
in requirement file: 
[tests/gui/requirements.txt](https://git.onedata.org/projects/VFS/repos/onedata-acceptance/browse/tests/gui/requirements.txt)

A handy oneliner to install Python dependencies (invoke from repo root):

```bash
pip install -r tests/gui/requirements.txt
```

Additional applications required in system (for GUI and mixed tests):

* `xclip` (Linux) or `pbcopy` (macOS)

A browser selected for tests (with `--driver`) should be also installed with test driver
executable. For example, you can install Google Chrome `chromedriver` in suitable
version for it from: https://chromedriver.chromium.org/downloads. 

**Note:** `chromedriver` have to be located in $PATH and named `chromedriver`.  

**Note:** Currently, only Google Chrome is used and well tested. 
You can use other browsers, but notice, this is not supported.

# Useful test_run parameters

* `--test-type gui` - set the test type use by core Onedata test helpers to differ from
"cucumber" tests etc.
* `-t tests/gui` - set the test cases path to gui
tests. For example, you can filter out tests to single suite using scenario file:
`-t tests/gui/scenarios/test_onezone_basic.py`.
* `--driver=Chrome` - set the browser to test in
* `-i onedata/gui_builder:latest` - use Docker image with dependencied for GUI tests
(i.a. Python, Selenium, Xvfb, Chrome)
* `--xvfb` - starts Xvfb, a virtual display server, that makes tests headless (without opening local browser window)
* `--xvfb-recording=<all|none|failed>` - optional, record all or none or failed tests
as movies and save them to `<logdir>/movies`
* `--no-clean` - prevents deleting Onedata deployment after tests (useful when using existing Onedata instalation)
* `--env-file=1oz_1op_not_deployed_embedded_ceph` - specifies `env_file` that will be used to start deployment if there is no active deployment 
* `--local` - uses locally installed testing toolkit instead of dockerized one
* `--no-pull` - prevents from downloading docker images (by default all tests scenarios force pulling docker
                        images even if they are already present on host
                        machine.)
* `-k="test_posix_storage_operations"` - used to select specific test
* `--oc-image=docker.onedata.org/oneclient-dev:develop` - used to specify oneclient service docker image


**Parameters:** (for advanced usage)

* `--no-mosaic-filter` - optional, if set, videos of tests using multiple browsers will
be recorded as different video for each browser (mosaic video created by default) 
* `--sources` - optional, if used, Onedata deployment starts using sources. Sources have
to be located in appropriate directories.
* `--update-etc-hosts` <!--- TODO VFS-10023 make description more specific after investigating this flag -->- adds entries to `/etc/hosts` for all pods in deployment.
When using this option script has to be run with root privileges.   
* `--add-test-domain` <!--- TODO VFS-10025 make description more specific after investigating this flag -->- when running tests on local machine option for adding entries to
`/etc/hosts` is turned off by default. This may cause that some test will fail.
You can enable adding entries to `/etc/hosts` using `--add-test-domain` option or add
entries manually.

**Note:** using `--add-test-domain`, `--update-etc-hosts` flags can be problematic due to permissions of `/etc/hosts` file.
The experimental and **not safe** method is to do `sudo chmod go+w /etc/hosts` locally and
share `/etc` directory in docker.
Please contact our support if you have issues with updating `/etc/hosts` for testing.

# Tests debugging
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

# Known issues

1. Some of the `test_run.py` flags are outdated and not used. They should be 
checked and eventually removed. <!--- VFS-10177  remove outdated test-run flags -->
2. [GUI known issues](tests/gui/README.md#known-issues)
3. [Mixed known issues](tests/mixed/README.md#known-issues)
4. [Oneclient known issues](tests/oneclient/README.md#known-issues)
