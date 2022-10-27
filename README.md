Onedata Acceptance Tests
========================

This is the code repository containing acceptance tests for Onedata. It uses 
one_env for creating environment running on kubernetes. 

Starting Onedata deployment
========================
To start Onedata 
deployment navigate to one_env directory and run:

 ```
 ./onenv up -f <env_file>
 ```
 
Where:
* ``env_file`` is yaml file describing the environment
* ``-f`` is option forcing new deployment, deleting an old one if present

Important notes:
1. To deploy environment using one_env you need to have access to kubernetes 
cluster (either local cluster started with minikube/kubeadm or remote cluster).
2. If you are using local kubernetes cluster started with minikube and driver 
option different than `none` you should check correctness of config generated 
by one_env in `${HOME}/.one_env/config`. Some drivers will mount your home 
directory in a different path in the VM, so you have to modify 
`kubeHostHomeDir` attribute. You can check mapping of host home directory to
VM directory on the official minikube website.
3. If you want to deploy environment with nfs storage make sure that:
- you have installed ``/sbin/mount.nfs`` helper program on node
- node's resolv.conf have to be able to resolve nfs domain name
4. To specify images for services use options:
- ``-zi`` for onezone service
- ``-ci`` for oneclient service
- ``-pi`` for oneprovider service

For example 2-provider environment with specified images:
```bash
./onenv up -f -pi docker.onedata.org/oneprovider-dev:develop -zi docker.onedata.org/onezone-dev:develop ../tests/gui/environments/1oz_2op_deployed.yaml
```
After deployment is ready (you can check it by using `./onenv status` _ready: True_), 
you need to add entries in `/etc/hosts` for this use: `./onenv hosts`.

### Environment setup for tests using local machines

Currently, only **Python 3.6.x** is supported and well tested.

These tests will be run using `py.test` runner on local machine.
Required Python packages to install (e.g. using `pip install`) are listed
in requirement file: `tests/gui/requirements.txt`

A handy oneliner to install Python dependencies (invoke from repo root):

```bash
pip install -r tests/gui/requirements.txt
```

Additional applications required in system:

* `xclip` (Linux) or `pbcopy` (macOS)

A browser selected for tests (with `--driver`) should be also installed with test driver
executable. For example, you can install Google Chrome and a `chromedriver` in suitable
version for it from: https://chromedriver.chromium.org/downloads.

GUI tests
===========
The whole procedure for running gui tests is described in details in the
[tests/gui/README.md](./tests/gui/README.md) file.


Mixed tests
===========
**Note:** Reading [tests/gui/README.md](./tests/gui/README.md) can help 
with understanding what is going on here. 
####
To run mixed tests: 

You can use ``./test_run.py`` script:

1. **Non-headless tests using existing Onedata installation** (more about non-headless test in [tests/gui/README.md](./tests/gui/README.md)): 
   - for REST and web GUI test:
       ```
     PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome --local --no-clean -v
       ```
     ``--local``: starts tests on host instead of starting them in pod (does not work with oneclient tests)
  

2. **Headless tests using existing Onedata installation**:
   - for REST, web GUI and oneclient test
     ```
     PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --no-clean --xvfb --xvfb-recording=failed
     ```
3. **Headless tests inside Pod on new Onedata environment** (automatic setup: use `--env-file` flag):
    ```
    PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --xvfb --xvfb-recording=failed --env-file=1oz_1op_2oc
    ```

Aforementioned commands can be used to run tests from one specified file:
```
  PYTHONPATH=tests/mixed ./test_run.py -t tests/mixed/scenarios/test_access_tokens_path_caveats.py --test-type mixed --driver=Chrome -i onedata/acceptance_mixed:latest --no-clean --xvfb --xvfb-recording=failed
```

##
The other way to run mixed tests is to use ``make`` command - see [bamboo-specs](../bamboo-specs).

  e.g.
  ```
  make SUITE=test_permission_posix_multi ENV_FILE=1oz_1op_2oc OPTS="--no-clean --no-pull" test_mixed_pkg
  ```

- ``SUITE`` - determines tests 
- ``ENV_FILE`` - optional, determines env-file (if not given default will be used)
- ``OPTS`` - optional, parameters - more about them you can find in _oneclient tests_ sector and [tests/gui/README.md](./tests/gui/README.md)


**Note:** When you specify `env-file` you don't need to start Onedata deployment by yourself - automatic setup (doesn't work on local machine) 
<!--- TODO VFS-10023 update after checking -->

Oneclient tests
=================
1. To run oneclient tests use ``./test_run.py`` script. Example invoke:
```
./test_run.py -t tests/oneclient/scenarios/test_luma_provider.py --test-type oneclient -i onedata/acceptance_mixed:latest --env-file=singleprovider_multistorage
```

Where:
* ``-t`` - standard ``./test_run.py`` parameter to set the test cases path to oneclient luma provider tests
* ``--test-type acceptance`` - set the test type use by core Onedata test helpers
* ``-i onedata/worker`` - use Docker image with dependencies for oneclient tests
* ``--env-file=singleprovider_multistorage`` - path to description of test environment in .yaml file


Some useful options:
* ``--no-clean`` - if present prevents cleaning onedata environment (don't use it if environment is not set up)
* ``-k="test_posix_storage_operations"`` - used to select specific test
* ``--oc-image=docker.onedata.org/oneclient-dev:develop`` - use to specify oneclient service


2. Like in _mixed test_ ``make`` command can be used to run oneclient tests - see [bamboo-specs](../bamboo-specs).

```
make SUITE=test_luma_provider ENV_FILE=singleprovider_multistorage TIMEOUT=720 IGNORE_XFAIL=1 OPTS="-k="test_posix_storage_operations"" test_oneclient_pkg
```