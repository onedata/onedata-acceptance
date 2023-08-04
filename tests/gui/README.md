# GUI acceptance tests

Acceptance tests using a web browser and Selenium - automated software that
simulates user actions performed on a website.


# Development

Please read this document before you start writing or modifying any tests.


# Running tests using Makefile

```
make ENV_FILE=$ENV SUITE=$SUITE test_gui
```

Commands for exact tests suites can be found in
[bamboo-specs/gui](../../bamboo-specs/gui-acceptance-src.yml).

For more information about running tests using `make`, see 
**Running acceptance tests** section in the main [README](../../README.md).

**Example:**
QoS basic tests on automatic Onedata deployment using a dockerized testing toolkit
```
make ENV_FILE=1oz_2op_deployed SUITE=test_qos_basic OPTS="--no-clean --no-pull" test_gui
```
**Note:** Onedata deployment does not have to be started in order to run
tests using `make` (it will start automatically).

**Known issue**: flag `--local` won't work, because `make` by default is using 
`--xvfb` flag, and they need to be mutually exclusive.
<!--- TODO VFS-9881 delete the above note after making --local and --xvfb flags mutually exclusive in Makefile -->


# Running tests using test_run (advanced)

The test_run.py command is essentially invoked by Makefile, but using it directly
allows better parameterization and overcoming of some known issues.

**Note:** all examples use the `--no-clean` option, make sure to remove it if you
require a fresh deployment every run.

## Running tests using a dockerized testing toolkit

```
./test_run.py -t tests/gui -i onedata/acceptance_gui:latest --test-type gui \
    --driver=Chrome --xvfb --no-clean
```

The Onedata deployment will be set up automatically with a Onezone and Oneprovider
(for details see `environments` dir with configurations). Setting up the deployment
can take some time.

We recommend using `onedata/acceptance_gui:latest` testing docker image 
when working on branches based on the `develop` branch. To run older versions, 
use the image defined as default in `Makefile`.

For some tests you should specify `--env-file` - see 
[bamboo-specs/gui](../../bamboo-specs/gui-acceptance-src.yml).
Otherwise, the default one will be used.

Example that starts a deployment using `1oz_1op_not_deployed_2_nodes.yaml`
and then runs tests on it:
```
./test_run.py -t tests/gui/scenarios/test_onepanel_deployment_with_2_hosts.py \
    -i onedata/acceptance_gui:latest --test-type gui --driver=Chrome --xvfb \
    --env-file=1oz_1op_not_deployed_2_nodes --no-clean
```

## Running tests using a locally installed testing toolkit

Acceptance tests using Selenium (GUI, Mixed) can be run with `--local` flag to
use the locally installed testing toolkit.

Running test this way greatly helps with debug because you can observe the test 
happening "live" in your browser. 
<!--- TODO VFS-10023 write about automatic setup on local machine -->

### Prerequisites

* **Python 3.8:**
  we recommend using Python 3.8. Python 3.7 and Python 3.6 are also supported.

* **required Python packages:** [tests/gui/requirements.txt](requirements.txt).
  To install Python dependencies run (invoke from repo root):
   ```
   pip3 install -r tests/gui/requirements.txt
   ```
  On Ubuntu 22.04 this won't work on default Python 3.10, a version 3.8
  must be installed on the side.

* **Google Chrome:**
  currently, only Google Chrome is used and well tested.
  You can use other browsers on your own risk.

* **xclip**

* **chromedriver:**
  you can install the Google Chrome `chromedriver` in suitable
  version for it from: https://chromedriver.chromium.org/downloads.

  **Note:** `chromedriver` have to be located in $PATH and named `chromedriver`.

### Known issues

There is a problem with automatic Onedata deployment setup for tests which
are using local machine. With `--local` flag, `pytest` is run differently than
on docker (have different options). Until this is fixed, *a Onedata deployment 
has to be ready in order to run tests locally*.

The manual start of Onedata deployment is described in the following
document: [one-env guide](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md).

**Note:** the one-env environment that is set up should be accessible via hostnames
(eg. https://dev-onezone.default.svc.cluster.local). Make sure that you can open address
of Onezone in your browser before starting tests.
Command `./onenv hosts` (invoke from repo `one-env` root) add entries
in `/etc/hosts`. For more information see **Starting Onedata deployment** section in
[one-env](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md).

### Examples

The `--local` flag indicates that the tests should be started using locally 
installed testing toolkit.

```bash
./test_run.py -t tests/gui --test-type gui --driver=Chrome --local --no-clean
```

To run a single test case:

```bash
./test_run.py -t tests/gui/scenarios/test_onezone_basic.py --test-type gui -vvv \ 
    --timeout 5 --reruns 0 --reruns-delay 0 --local --no-clean --driver=Chrome \ 
    -k test_onezone_login_page_renders_with_proper_title
```

**Note:** the `--update-etc-hosts` flag will add entries in `/etc/hosts` when the 
deployment is ready.


# Test reports

The test report in HTML format with embedded screenshots of browser in failed test will be saved to:
`<onedata_repo_root>/tests/gui/logs/report.<time_stamp>/report.html`

# Taking screenshots

For some purposes, taking screenshots can be required at the time of test run.

In steps of scenarios simply use:
```python
driver.get_screenshot_as_file('/tmp/some-screenshot.png')
```
where driver is instance of Selenium WebDriver

## Fixtures and pytest plugins overrides

* The default configuration of `pytest-selenium-multi` for sensitive URLs is inverted:
all tests are considered *non-destructive by default*.
You can add a ```@pytest.mark.destructive``` mark to test scenario to mark test as destructive.

* The `sensitive_url` fixture has module scope, because we start new environment for each module
(so it could have different `base_url's`)
