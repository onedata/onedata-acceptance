Feature: Storage modification


  Background:
    Given user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario Outline: User changes storage parameters into incorrect ones and sees that they remain unchanged in Onepanel
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser expands "<storage_name>" record on storages list in storages page in Onepanel
    And user of browser clicks on "Modify" button for "<storage_name>" storage record in Storages page in Onepanel
    And user of browser types "<param_val>" to <param_name> field in <storage_name> edit form for "<storage_name>" storage in Onepanel
    And user of browser clicks on Save button in edit form for "<storage_name>" storage in Onepanel
    And user of browser confirms committed changes in modal "Modify Storage"

    And user of browser sees that error modal with text "File read/write test has failed" appeared
    And user of browser closes "error" modal

    And user of browser expands "<storage_name>" record on storages list in storages page in Onepanel
    Then user of browser sees that "<storage_name>" <param_name> is <prev_param_val> in storages page in Onepanel

    Examples:
    | storage_name | param_name  | param_val   | prev_param_val |
    | posix        | Mount point | /wrong/path | /volumes/posix |
    | s3           | Bucket name | wrong_name  | test           |
    | ceph         | Pool name   | wrong_name  | test           |


  Scenario Outline: User fails to create <storage_name> storage with incorrect parameters using add storage form in Onepanel
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser clicks on Add storage backend button in storages page in Onepanel
    And user of browser selects <storage_name> from storage selector in storages page in Onepanel
    And user of browser types "test_storage" to Storage name field in <storage_name> form in storages page in Onepanel
    And user of browser types "<param_val>" to <param_name> field in <storage_name> form in storages page in Onepanel
    And user of browser clicks on Add button in add storage form in storages page in Onepanel

    Then user of browser sees that error modal with text "Adding \"test_storage\" storage backend failed!" appeared
    And user of browser closes "error" modal
    And user of browser does not see "test_storage" on the storages list


    Examples:
    | storage_name | param_name  | param_val   |
    | posix        | Mount point | /wrong/path |
    | s3           | Bucket name | wrong_name  |


  Scenario: User fails to create Ceph storage with incorrect parameters using add storage form in Onepanel
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser clicks on Add storage backend button in storages page in Onepanel
    And user of browser selects Ceph Rados from storage selector in storages page in Onepanel
    And user of browser types "test_storage" to Storage name field in ceph form in storages page in Onepanel
    And user of browser types "client.k8s" to Username field in ceph form in storages page in Onepanel
    And user of browser types "AQC1oSZZZfucFxAA34MekwoWBm7qpGd0A8u+fg==" to Key field in ceph form in storages page in Onepanel
    And user of browser types "dev-volume-ceph-krakow.default" to Monitor hostname field in ceph form in storages page in Onepanel
    And user of browser types "test_cluster" to Cluster name field in ceph form in storages page in Onepanel
    And user of browser types "wrong_name" to Pool name field in ceph form in storages page in Onepanel
    And user of browser types "4194304" to Block size field in ceph form in storages page in Onepanel
    And user of browser clicks on Add button in add storage form in storages page in Onepanel

    Then user of browser sees that error modal with text "Adding \"test_storage\" storage backend failed!" appeared
    And user of browser closes "error" modal
    And user of browser does not see "test_storage" on the storages list


  Scenario: User sees file's content after modifying storage backend to copied mountpoint directory
    Given "test_storage1" storage backend in "oneprovider-1" Oneprovider panel service used by admin with following configuration:
          storage type: POSIX
          mount point: /volumes/posix

    And initial spaces configuration in "onezone" Onezone service:
          space2:
              owner: admin
              providers:
                  - oneprovider-1:
                      storage: test_storage1
                      size: 1000000

    When user creates directory (mkdir) /volumes/dir3 on oneprovider-1 docker

    And user of browser opens file browser for "space2" space
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir

    And user of browser copies "space2" space directory to /volumes/dir3

    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser clicks on "Modify" button for "test_storage1" storage record in Storages page in Onepanel
    And user of browser types "/volumes/dir3" to Mount point field in POSIX edit form for "test_storage1" storage in Onepanel
    And user of browser clicks on Save button in edit form for "test_storage1" storage in Onepanel
    And user of browser confirms committed changes in modal "Modify Storage"
    And user of browser sees that "test_storage1" is visible on the storages list

    And user of browser opens file browser for "space2" space
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "20B-1.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-1.txt" is equal to: "11111111111111111111"
