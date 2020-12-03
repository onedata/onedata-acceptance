#Acceptance tests of upgrade procedure

Upgrade acceptance tests can be run using `test_run.py` with option `--test-type` set to `upgrade`.

Example invocation:
```bash
./test_run.py --test-type upgrade -vvv --test-dir tests/upgrade/upgrade_meta_test.py -i onedata/acceptance_mixed:v8 --timeout 420 --env-file=tests/upgrade/configs/test_config.yaml
```

Important parameter is `env-file` which contains path to `.yaml` file with environments description.

## Environments description file
This file consists of 3 sections:
  - scenarios
  - initialVersions
  - targetVersions
  
#### Initial versions
This part contains information about what version of each component is to be started. 
```yaml
initialVersions:
  onezone: 20.02.1
  oneprovider: 20.02.1
  oneclient: 20.02.1
```

NOTE: each provided version must be a valid tag to the `docker.onedata.org/{component}-dev` image.

#### Target versions
This part contains information about what version each component is to be upgraded to. 
It is similar to initial versions, but additionally `sources` can be specified for `onezone` or `oneprovider`.
```yaml
targetVersions: 
  onezone: develop
  oneprovider: 
    sources:
      baseImage: develop
      components:
        - worker
        - panel
        - cluster-manager
  oneclient: 20.02.3
```

Also `default` can be provided as a target version. In that case version is read from file in 
`./artifacts_dir/` which is created there by running `onenv pull_artifacts` before tests.
  
#### Scenarios
This is a list of names of files in `environments/scenarios` directory without `.yaml` suffix.

```yaml
scenarios: 
  - 1op
  - 2op
```
Tests are run in a following sequence: 
```
  - start environment specified in **first** scenario in version provided in initialVersions
  - run tests setup functions
  - upgrade environment to targetVersions
  - run tests verify functions
  - clean environment

  - start environment specified in **second** scenario in version provided in initialVersions
  - ...
```
