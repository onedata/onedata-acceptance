# Name of the scenario to run
scenario: "scenario-1oz-1op"

# Determines if onedata components should be started from pre-compiled sources
# or pre-installed packages inside dockers. When enabled, sources are expected
# to be found in CWD (from where the 'up' script was run) or one dir above.
sources: false

createSpaces: false

# Onezone image to use. Note that if 'sources' option is enabled, it must
# be based off onedata/worker image (it contains all the machinery to run the
# application from sources).
onezoneImage: "docker.onedata.org/onezone-dev:develop"

# Oneprovider image to use. Note that if 'sources' option is enabled, it must
# be based off onedata/worker image.
oneproviderImage: "docker.onedata.org/oneprovider-dev:develop"

# When enabled, onezoneImage and oneproviderImage will be pulled before every
# deployment. If disabled, they will only be pulled if not existent.
forceImagePull: true

onezone:
  onezone_ready_check:
    enabled: false
  batchConfig: false
  workerOverlayConfig: |-
    [
      {oz_worker, [
        {disable_gui_package_verification, true},
        {gui_debug_mode, true}
      ]}
    ].
  panelOverlayConfig: |-
    [
      {onepanel, [
        {gui_debug_mode, true}
      ]}
    ].

oneprovider-1:
  oneprovider_ready_check:
    enabled: false
  batchConfig: false
  clusterConfig:
    managers: [node-1]
    workers: [node-2]
    databases: [node-1]
  addTestDomain: true