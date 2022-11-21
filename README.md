# Onedata Acceptance Tests

This is the code repository containing acceptance tests for Onedata. \
It uses one-env for creating environment running on kubernetes

# Important notes

- Currently, for testing, only Google Chrome is used and well tested. 
You can use other browsers, but notice, this is not supported.    
- It is recommended to use Ubuntu 20.04+, Ubuntu 18.04. Setting up environment 
and running tests in macOS is not officially supported.

# Running acceptance tests
Acceptance tests can be run in few ways:
1. Using `Makefile`.
2. Using `./test_run.py`:
   1. Running tests on automatic Onedata deployment using a dockerized testing toolkit
   2. Running tests on a preexisting Onedata deployment:
      1. Using a dockerized testing toolkit.
      2. Using a locally installed testing toolkit.

For use in CI (Bamboo) see Bamboo Specs files placed in [bamboo-specs](bamboo-specs) directory in root of this repository. These specs use `Makefile` targets directly.

The exact procedure of running tests is described in:
* [tests/gui/README.md](./tests/gui/README.md) for **GUI** tests
* [tests/mixed/README.md](./tests/mixed/README.md) for **Mixed** tests
* [tests/oneclient/README.md](./tests/oneclient/README.md) for **Oneclient** tests


## Testing toolkit
All tools that are needed to run tests:
* Python 3.8
* required Python packages: [requirements.txt](requirements.txt)
* Google Chrome
* xclip
* chromedriver


# Starting Onedata deployment
The manual start of the environment is described in the following
document: [one-env guide](https://git.onedata.org/projects/VFS/repos/onedev/browse/guides/one-env.md)

Example command which starts deployment:

 ```
./onenv up -f test_env_config.yaml 
 ```

**Note:** setting up environment and running tests in macOS is not officially
supported and can be tricky. If you still want to run tests on macOS, see 
[macOS environment setup](macOS_enviroment_setup.md) for tips.

### Useful test_run parameters

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
* `--no-clean` - prevents deleting environment after tests (useful when using existing Onedata instalation)
* `--env-file=1oz_1op_not_deployed_embedded_ceph` - specifies `env_file` that will be used to start deployment if there is no active deployment 
* `--local` - starts tests on host instead of starting them in docker
* `--no-pull` - prevents from downloading docker images (by default all tests scenarios force pulling docker
                        images even if they are already present on host
                        machine.)

**Parameters:** (for advanced usage)

* `--no-mosaic-filter` - optional, if set videos of tests using multiple browsers will
be recorded as different video for each browser (mosaic video created by default) 
* `--sources` - optional, if set starts Onedata deployment using sources. Sources have
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