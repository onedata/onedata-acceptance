Feature: Storage management using onepanel


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser1, browser2] logged as [admin, admin] to [Onezone, emergency interface of Onepanel] service
    And directory tree structure on local file system:
          browser1:
              - dir1: 70
              - dir2: 10


  Scenario Outline: User uploads files on freshly supported space on newly created storage
    Given there are no spaces supported in Onepanel used by user of browser1
    And there is no "hello_world1" space in Onezone used by user of browser1

    # create new_storage POSIX storage
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of <client> clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <client> clicks on Add storage button in storages page in Onepanel
    And user of <client> selects POSIX from storage selector in storages page in Onepanel
    And user of <client> types "<storage_name>" to Storage name field in POSIX form in storages page in Onepanel
    And user of <client> types "/volumes/persistence/storage" to Mount point field in POSIX form in storages page in Onepanel
    And user of <client> clicks on Add button in add storage form in storages page in Onepanel
    And user of <client> sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of <client> expands "<storage_name>" record on storages list in storages page in Onepanel
    And user of <client> sees that "<storage_name>" Storage type is posix in storages page in Onepanel
    And user of <client> sees that "<storage_name>" Mount point is /volumes/persistence/storage in storages page in Onepanel

    And user of browser1 creates "hello_world1" space in Onezone
    And user of browser1 is idle for 5 seconds
    And user of browser1 sends support token for "hello_world1" to user of <client>

    # support space
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of <client> clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <client> clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of <client> selects "<storage_name>" from storage selector in support space form in Onepanel
    And user of <client> types received token to Support token field in support space form in Onepanel
    And user of <client> types "1" to Size input field in support space form in Onepanel
    And user of <client> selects GiB radio button in support space form in Onepanel
    And user of <client> clicks on Support space button in support space form in Onepanel
    And user of <client> sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of <client> sees that space support record for "hello_world1" has appeared in Spaces page in Onepanel

    # go to provider
    And user of browser1 is idle for 2 seconds
    And user of browser1 refreshes site
    And user of browser1 opens oneprovider-1 Oneprovider view in web GUI

    # create tmp dir and upload there 70 files
    And user of browser1 uses spaces select to change data space to "hello_world1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 sees that current working directory displayed in breadcrumbs is hello_world1
    And user of browser1 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser1 sees that "New directory" modal has appeared
    And user of browser1 clicks on input box in active modal
    And user of browser1 types "dir100" on keyboard
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared
    And user of browser1 sees that item named "dir100" has appeared in file browser
    And user of browser1 double clicks on item named "dir100" in file browser
    And user of browser1 sees that current working directory displayed in breadcrumbs is hello_world1/dir100
    And user of browser1 uses upload button in toolbar to upload files from local directory "dir1" to remote current dir
    And user of browser1 waits for file upload to finish

    Then user of browser1 sees that there are 70 items in file browser

    And user of browser1 clicks on the "spaces" tab in main menu sidebar
    And user of browser1 leaves "hello_world1" space in Onezone page

    Examples:
    | client   | storage_name |
    | browser1 | new_storage1 |
    | browser2 | new_storage2 |


  Scenario Outline: User modifies newly created storage
    When user of <client> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
    And using docker, admin renames /volumes/persistence/storage path to /volumes/persistence/storage2
    And user of <client> expands toolbar for "<storage_name>" storage record in Storages page in Onepanel
    And user of <client> clicks on Modify storage details option in storage's toolbar in Onepanel
    And user of <client> types "/volumes/persistence/storage2" to Mount point field in POSIX edit form for "<storage_name>" storage in Onepanel
    And user of <client> clicks on Save button in edit form for "<storage_name>" storage in Onepanel
    And user of <client> clicks on "Proceed" button in modal "MODIFY STORAGE"
    Then user of <client> sees that "<storage_name>" Mount point is /volumes/persistence/storage2 in storages page in Onepanel

    And using docker, admin renames /volumes/persistence/storage2 path to /volumes/persistence/storage

    Examples:
    | client   | storage_name |
    | browser1 | new_storage3 |
    | browser2 | new_storage4 |


  Scenario Outline: User removes newly created storage
    When user of <client> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
    Then user of <client> expands toolbar for "<storage_name>" storage record in Storages page in Onepanel
    And user of <client> clicks on Remove storage option in storage's toolbar in Onepanel
    And user of <client> clicks on "Remove" button in modal "REMOVE STORAGE"
    And user of <client> sees that "<storage_name>" has disappeared from the storages list

    Examples:
    | client   | storage_name |
    | browser1 | new_storage5 |
    | browser2 | new_storage6 |


  Scenario: User changes the name of a directory which is the mount point for storage
    When user of browser1 creates "space3" space in Onezone
    And user of browser1 copies dir1 to /volumes/persistence/storage/dir directory
    And user of browser1 adds "new_storage7" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage/dir
    And user of browser1 sends support token for "space3" to user of browser1

    # support space
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage7
          size: 1
          unit: GiB
          mount in root: True
          storage import:
                strategy: Simple scan
                max depth: 2
          storage update:
                strategy: Simple scan

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space3" has appeared in Spaces page in Onepanel

    And user of browser1 opens oneprovider-1 Oneprovider view in web GUI
    And user of browser1 sees that Oneprovider session has started
    And user of browser1 uses spaces select to change data space to "space3"

    # confirm import of files
    And user of browser1 is idle for 8 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 sees that there is 1 item in file browser
    And user of browser1 sees item(s) named "dir1" in file browser

    And using docker, admin renames /volumes/persistence/storage/dir path to /volumes/persistence/storage/renamed_dir05
    And user of browser1 copies dir2 to /volumes/persistence/storage/renamed_dir05 directory

    And user of browser1 is idle for 8 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 sees that there is 1 item in file browser

    And user of browser1 clicks on the "clusters" tab in main menu sidebar
    And user of browser1 is idle for 8 seconds
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 expands toolbar for "new_storage7" storage record in Storages page in Onepanel
    And user of browser1 clicks on Modify storage details option in storage's toolbar in Onepanel
    And user of browser1 types "/volumes/persistence/storage/renamed_dir05" to Mount point field in POSIX edit form for "new_storage7" storage in Onepanel
    And user of browser1 clicks on Save button in edit form for "new_storage7" storage in Onepanel
    And user of browser1 clicks on "Proceed" button in modal "MODIFY STORAGE"

    And user of browser1 opens oneprovider-1 Oneprovider view in web GUI
    And user of browser1 sees that Oneprovider session has started
    And user of browser1 uses spaces select to change data space to "space3"

    Then user of browser1 is idle for 8 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 sees that there are 2 items in file browser
    And user of browser1 sees item(s) named "dir2" in file browser
