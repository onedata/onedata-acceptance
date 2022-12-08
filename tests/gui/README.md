# GUI acceptance tests

# Running tests using Makefile

To run GUI test use:
```
make ENV_FILE=$ENV SUITE=$SUITE BROWSER=Chrome TIMEOUT=600 test_gui
```

Commands for exact tests suites can be found in [bamboo-specs/gui](../../bamboo-specs/gui-acceptance-src.yml).

For more information about running tests using `make` see  [README](../../README.md#running-acceptance-tests)

**Example:**
QoS basic tests on automatic Onedata deployment using a dockerized testing toolkit
```
make ENV_FILE=1oz_2op_deployed SUITE=test_qos_basic BROWSER=Chrome TIMEOUT=600 OPTS="--no-clean --no-pull" test_gui
```
**Note:** Onedata deployment does not have to be started in order to run
tests using `make` (it will start automatically).

**Note:** flag `--local` won't work, because `make` by default is using 
`--xvfb` flag, and they need to be mutually exclusive.
<!--- TODO VFS-9881 delete the above note after making --local and --xvfb flags mutually exclusive in Makefile -->


# Running GUI tests using test_run

## Running tests on automatic Onedata deployment using a dockerized testing toolkit

Using this method, the Onedata deployment will be set up automatically with OZ and OP
(for details see `environments` dir with configurations). Setting up deployment can take
some time.

```
./test_run.py -t tests/gui -i onedata/acceptance_gui:latest --test-type gui --driver=Chrome --xvfb
```

**Note:** we recommend using `onedata/acceptance_gui:latest` testing docker image for
current version of tests. For legacy versions of tests, use image defined in `Makefile`.

**Note:** for some tests you should specify `--env-file` - 
see [bamboo-specs/gui](../../bamboo-specs/gui-acceptance-src.yml)

Example that starts deployment using `1oz_1op_not_deployed_embedded_ceph.yaml`:
```
./test_run.py -t tests/gui/scenarios/test_onepanel_deployment_ceph.py -i onedata/acceptance_gui:latest --test-type gui --driver=Chrome --xvfb --env-file=1oz_1op_not_deployed_embedded_ceph
```

## Running tests on a preexisting Onedata deployment:

Using this method, existing Onedata deployment installation will be used
if available.

### Using a dockerized testing toolkit

```
./test_run.py -t tests/gui --test-type gui --driver=Chrome -i onedata/acceptance_gui:latest --no-clean --xvfb --xvfb-recording=failed
```

**Note:**  If Onedata deployment is not running, it will start 
during the first call of above command 

### Using a locally installed testing toolkit

Running test this way greatly helps with debug because you see test "live". 
<!--- TODO VFS-10023 write about automatic setup on local machine -->

Acceptance tests using selenium (GUI, Mixed) can be run with `--local` flag. 
To make it work you must install some tools. 
List of tools: [Testing toolkit](../../README.md#testing-toolkit)

**Starting tests:**

We recommend  reading
[Some-useful-information-about-starting-Onedata-deployment-to-run-tests](../../README.md#some-useful-information-about-starting-onedata-deployment-to-run-tests)
before starting tests locally.

**Note:** the one-env environment that is set up should be accessible via hostnames
(eg. https://dev-onezone.default.svc.cluster.local). Make sure that you can open address
of Onezone in your browser before starting tests. 
Command `./onenv hosts` (invoke from repo `one-env` root) add entries 
in `/etc/hosts`. For more information: 
[one-env/Starting-Onedata-deployment](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md#Starting-Onedata-deployment)

**Example** (invoke from onedata-acceptance repo root dir):

```bash
./test_run.py -t tests/gui --test-type gui --driver=Chrome --local --no-clean
```

You can also use this command to run the simplest single test:

```bash
./test_run.py -t tests/gui/scenarios/test_onezone_basic.py --test-type gui -vvv --timeout 5 --reruns 0 --reruns-delay 0 --local --no-clean --driver=Chrome -k test_onezone_login_page_renders_with_proper_title
```

**New parameters:**

* `--local` - uses locally installed testing toolkit instead of dockerized one.

**Note:** Onedata deployment have to be ready in order to run tests locally.

**Note:** `--update-etc-hosts` flag add entries in `/etc/hosts` when deployment is ready.

# Known issues

1. There is a problem with automatic Onedata deployment setup for tests which 
are using local machine. With `--local` flag, `pytest` is run differently than 
on docker (have different options).

# Test reports

The test report in HTML format with embedded screenshots of browser in failed test will be saved to:
`<onedata_repo_root>/tests/gui/logs/report.<time_stamp>/report.html`

# Taking screenshots

For some purposes, taking screenshots can be required in time of test run.

In steps of scenarios simply use:
```python
driver.get_screenshot_as_file('/tmp/some-screenshot.png')
```
where driver is instance of Selenium WebDriver

# Development

Please read these section before you start writing or modifying GUI tests.

## Fixtures and pytest plugins overrides

* The default configuration of `pytest-selenium-multi` for sensitive URLs is inverted:
all tests are considered *non-destructive by default*.
You can add a ```@pytest.mark.destructive``` mark to test scenario to mark test as destructive.

* The `sensitive_url` fixture has module scope, because we start new environment for each module
(so it could have different `base_url's`)
