Feature: Storage management using onepanel


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-1 in Onepanel

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [admin, admin] to [Onezone, emergency interface of Onepanel] service
    And directory tree structure on local file system:
          browser_unified:
              dir1: 70
              dir2: 5

  Scenario Outline: User uploads files on freshly supported space on newly created storage
    Given admin user does not have access to any space

    # create new_storage POSIX storage
    When user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of <browser> clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <browser> clicks on Add storage button in storages page in Onepanel
    And user of <browser> selects POSIX from storage selector in storages page in Onepanel
    And user of <browser> types "<storage_name>" to Storage name field in POSIX form in storages page in Onepanel
    And user of <browser> types "/volumes/persistence/storage" to Mount point field in POSIX form in storages page in Onepanel
    And user of <browser> clicks on Add button in add storage form in storages page in Onepanel
    And user of <browser> sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of <browser> expands "<storage_name>" record on storages list in storages page in Onepanel
    And user of <browser> sees that "<storage_name>" Storage type is posix in storages page in Onepanel
    And user of <browser> sees that "<storage_name>" Mount point is /volumes/persistence/storage in storages page in Onepanel

    And user of browser_unified creates "space1" space in Onezone
    And user of browser_unified is idle for 5 seconds
    And user of browser_unified sends support token for "space1" to user of <browser>

    # support space
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of <browser> clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <browser> clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of <browser> selects "<storage_name>" from storage selector in support space form in Onepanel
    And user of <browser> types received token to Support token field in support space form in Onepanel
    And user of <browser> types "1" to Size input field in support space form in Onepanel
    And user of <browser> selects GiB radio button in support space form in Onepanel
    And user of <browser> clicks on Support space button in support space form in Onepanel
    And user of <browser> sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of <browser> sees that space support record for "space1" has appeared in Spaces page in Onepanel

    # go to provider
    And user of browser_unified is idle for 4 seconds

    # create tmp dir and upload there 10 files
    And user of browser_unified opens file browser for "space1" space
    And user of browser_unified creates directory "new_dir"
    And user of browser_unified sees that item named "new_dir" has appeared in file browser
    And user of browser_unified double clicks on item named "new_dir" in file browser
    And user of browser_unified sees that current working directory displayed in breadcrumbs is /new_dir
    And user of browser_unified uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    And user of browser_unified waits for file upload to finish
    Then user of browser_unified sees that there are 5 items in file browser


    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage1 |
    | browser_emergency | new_storage2 |


  Scenario Outline: User modifies newly created storage
    When user of <browser> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
    And using docker, admin renames /volumes/persistence/storage path to /volumes/persistence/storage2
    And user of <browser> is idle for 5 seconds
    And user of <browser> expands toolbar for "<storage_name>" storage record in Storages page in Onepanel
    And user of <browser> clicks on Modify storage details option in storage's toolbar in Onepanel
    And user of <browser> types "/volumes/persistence/storage2" to Mount point field in POSIX edit form for "<storage_name>" storage in Onepanel
    And user of <browser> clicks on Save button in edit form for "<storage_name>" storage in Onepanel
    And user of <browser> clicks on "Proceed" button in modal "Modify Storage"
    And user of <browser> is idle for 2 seconds
    And user of <browser> expands "<storage_name>" record on storages list in storages page in Onepanel
    Then user of <browser> sees that "<storage_name>" Mount point is /volumes/persistence/storage2 in storages page in Onepanel

    And using docker, admin renames /volumes/persistence/storage2 path to /volumes/persistence/storage

    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage3 |
    | browser_emergency | new_storage4 |


  Scenario Outline: User removes newly created storage
    When user of <browser> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
    And user of <browser> is idle for 5 seconds
    Then user of <browser> expands toolbar for "<storage_name>" storage record in Storages page in Onepanel
    And user of <browser> clicks on Remove storage option in storage's toolbar in Onepanel
    And user of <browser> clicks on "Remove" button in modal "Remove storage"
    And user of <browser> is idle for 2 seconds
    And user of <browser> sees that "<storage_name>" has disappeared from the storages list

    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage5 |
    | browser_emergency | new_storage6 |


  Scenario: User sees that synchronization auto-update still works after changing mount point for storage
    When user of browser_unified creates "space3" space in Onezone
    And user of browser_unified copies dir1 to /volumes/persistence/storage/dir directory on docker
    And user of browser_unified adds "new_storage7" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage/dir
          imported storage: true
    And user of browser_unified sends support token for "space3" to user of browser_unified

    # support space
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage7 (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2
          storage update:
                strategy: Simple scan

    And user of browser_unified sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser_unified sees that space support record for "space3" has appeared in Spaces page in Onepanel

    And user of browser_unified opens file browser for "space3" space

    # confirm import of files
    And user of browser_unified is idle for 8 seconds
    And user of browser_unified sees file browser in data tab in Oneprovider page

    And user of browser_unified sees only items named "dir1" in file browser

    And using docker, admin renames /volumes/persistence/storage/dir path to /volumes/persistence/storage/renamed_dir05
    And user of browser_unified copies dir2 to /volumes/persistence/storage/renamed_dir05 directory on docker

    And user of browser_unified is idle for 8 seconds
    And user of browser_unified sees file browser in data tab in Oneprovider page

    And user of browser_unified sees that there is 1 item in file browser

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified is idle for 8 seconds
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser_unified expands toolbar for "new_storage7" storage record in Storages page in Onepanel
    And user of browser_unified clicks on Modify storage details option in storage's toolbar in Onepanel
    And user of browser_unified types "/volumes/persistence/storage/renamed_dir05" to Mount point field in POSIX edit form for "new_storage7" storage in Onepanel
    And user of browser_unified clicks on Save button in edit form for "new_storage7" storage in Onepanel
    And user of browser_unified clicks on "Proceed" button in modal "Modify storage"

    And user of browser_unified opens file browser for "space3" space
    And user of browser_unified is idle for 8 seconds
    And user of browser_unified sees file browser in data tab in Oneprovider page

    Then user of browser_unified sees that there are 2 items in file browser
    And user of browser_unified sees item(s) named "dir2" in file browser


  Scenario: User fails to configure import in storage that is not import-enabled
    When user of browser_unified creates "space5" space in Onezone
    And user of browser_unified copies dir1 to /volumes/persistence/storage/dir directory on docker
    And user of browser_unified adds "new_storage8" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage/dir
    And user of browser_unified sends support token for "space5" to user of browser_unified

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_unified clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of browser_unified selects "new_storage8" from storage selector in support space form in Onepanel
    And user of browser_unified types received token to Support token field in support space form in Onepanel
    Then user of browser_unified cannot enable storage data import option


  Scenario: User fails to create 2 storages with the same name
    When user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    # user adds new storage with name
    And user of browser_unified clicks on Add storage button in storages page in Onepanel
    And user of browser_unified selects POSIX from storage selector in storages page in Onepanel
    And user of browser_unified types "storage" to Storage name field in POSIX form in storages page in Onepanel
    And user of browser_unified types "/" to Mount point field in POSIX form in storages page in Onepanel
    And user of browser_unified clicks on Add button in add storage form in storages page in Onepanel

    # user adds second storage with the same name
    And user of browser_unified selects POSIX from storage selector in storages page in Onepanel
    And user of browser_unified types "storage" to Storage name field in POSIX form in storages page in Onepanel
    And user of browser_unified types "/tmp" to Mount point field in POSIX form in storages page in Onepanel
    And user of browser_unified clicks on Add button in add storage form in storages page in Onepanel
    And user of browser_unified sees that error popup has appeared
    And user of browser_unified sees that error modal with text "The resource already exists." appeared
