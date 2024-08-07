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
    And user of <browser> clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <browser> clicks on Add storage backend button in storages page in Onepanel
    And user of <browser> selects POSIX from storage selector in storages page in Onepanel
    And user of <browser> types "<storage_name>" to Storage name field in POSIX form in storages page in Onepanel
    And user of <browser> types "/volumes/posix" to Mount point field in POSIX form in storages page in Onepanel
    And user of <browser> clicks on Add button in add storage form in storages page in Onepanel
    And user of <browser> sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of <browser> expands "<storage_name>" record on storages list in storages page in Onepanel
    And user of <browser> sees that "<storage_name>" Storage type is posix in storages page in Onepanel
    And user of <browser> sees that "<storage_name>" Mount point is /volumes/posix in storages page in Onepanel

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
    And user of browser_unified clicks and presses enter on item named "new_dir" in file browser
    And user of browser_unified sees that current working directory displayed in breadcrumbs on file browser is "space1/new_dir"
    And user of browser_unified uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    Then user of browser_unified sees that there are 5 items in file browser


    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage1 |
    | browser_emergency | new_storage2 |


  Scenario Outline: User modifies newly created storage
    When user of <browser> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
    And using docker, admin renames /volumes/posix path to /volumes/posix2
    And user of <browser> is idle for 5 seconds
    And user of <browser> clicks on "Modify" button for "<storage_name>" storage record in Storages page in Onepanel
    And user of <browser> types "/volumes/posix2" to Mount point field in POSIX edit form for "<storage_name>" storage in Onepanel
    And user of <browser> clicks on Save button in edit form for "<storage_name>" storage in Onepanel
    And user of <browser> confirms committed changes in modal "Modify Storage"
    And user of <browser> is idle for 5 seconds
    And user of <browser> expands "<storage_name>" record on storages list in storages page in Onepanel
    Then user of <browser> sees that "<storage_name>" Mount point is /volumes/posix2 in storages page in Onepanel

    And using docker, admin renames /volumes/posix2 path to /volumes/posix

    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage3 |
    | browser_emergency | new_storage4 |


  Scenario Outline: User removes newly created storage
    When user of <browser> adds "<storage_name>" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
    And user of <browser> is idle for 5 seconds
    Then user of <browser> expands toolbar for "<storage_name>" storage record in Storages page in Onepanel
    And user of <browser> clicks on Remove storage backend option in storage's toolbar in Onepanel
    And user of <browser> clicks on "Remove" button in modal "Remove storage backend"
    And user of <browser> sees that "<storage_name>" has disappeared from the storages list

    Examples:
    | browser           | storage_name |
    | browser_unified   | new_storage5 |
    | browser_emergency | new_storage6 |


  Scenario: User sees that synchronization auto-update still works after changing mount point for storage
    When user of browser_unified creates "space3" space in Onezone
    And user of browser_unified copies dir1 to /volumes/posix/dir directory on docker
    And user of browser_unified adds "new_storage7" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/posix/dir
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
            max depth: 2
            continuous scan: true
            scan interval [s]: 1

    And user of browser_unified sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser_unified sees that space support record for "space3" has appeared in Spaces page in Onepanel

    And user of browser_unified opens file browser for "space3" space

    # confirm import of files
    And user of browser_unified sees file browser in files tab in Oneprovider page

    And user of browser_unified sees only items named "dir1" in file browser

    And using docker, admin renames /volumes/posix/dir path to /volumes/posix/renamed_dir05
    And user of browser_unified copies dir2 to /volumes/posix/renamed_dir05 directory on docker

    And user of browser_unified sees file browser in files tab in Oneprovider page

    And user of browser_unified sees that there is 1 item in file browser

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_unified is idle for 2 seconds

    And user of browser_unified clicks on "Modify" button for "new_storage7" storage record in Storages page in Onepanel
    And user of browser_unified types "/volumes/posix/renamed_dir05" to Mount point field in POSIX edit form for "new_storage7" storage in Onepanel
    And user of browser_unified clicks on Save button in edit form for "new_storage7" storage in Onepanel
    And user of browser_unified confirms committed changes in modal "Modify Storage"

    And user of browser_unified opens file browser for "space3" space
    And user of browser_unified sees file browser in files tab in Oneprovider page

    Then user of browser_unified sees that there are 2 items in file browser
    And user of browser_unified sees item(s) named "dir2" in file browser


  Scenario: User fails to update import in storage that is not import-enabled
    When user of browser_unified creates "space5" space in Onezone
    And user of browser_unified copies dir1 to /volumes/posix/dir directory on docker
    And user of browser_unified adds "new_storage8" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/posix/dir
    And user of browser_unified sends support token for "space5" to user of browser_unified

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_unified clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of browser_unified selects "new_storage8" from storage selector in support space form in Onepanel
    And user of browser_unified types received token to Support token field in support space form in Onepanel
    And user of browser_unified types "1" to Size input field in support space form in Onepanel
    And user of browser_unified selects GiB radio button in support space form in Onepanel
    And user of browser_unified clicks on Support space button in support space form in Onepanel
    And user of browser_unified opens "space5" record on spaces list in Spaces page in Onepanel
    Then user of browser_unified cannot click on Storage import navigation tab in space "space5"


  Scenario: User succeeds to create 2 storages with the same name
    Given there is no "storage" storage in "oneprovider-1" Oneprovider panel
    When user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    # user adds new storage with name
    And user of browser_unified clicks on Add storage backend button in storages page in Onepanel
    And user of browser_unified selects POSIX from storage selector in storages page in Onepanel
    And user of browser_unified types "storage" to Storage name field in POSIX form in storages page in Onepanel
    And user of browser_unified types "/" to Mount point field in POSIX form in storages page in Onepanel
    And user of browser_unified clicks on Add button in add storage form in storages page in Onepanel

    # user adds second storage with the same name
    And user of browser_unified clicks on Add storage backend button in storages page in Onepanel
    And user of browser_unified selects POSIX from storage selector in storages page in Onepanel
    And user of browser_unified types "storage" to Storage name field in POSIX form in storages page in Onepanel
    And user of browser_unified types "/tmp" to Mount point field in POSIX form in storages page in Onepanel
    And user of browser_unified clicks on Add button in add storage form in storages page in Onepanel
    Then user of browser_unified sees 2 storages named "storage" with different IDs on the storages list


  Scenario: User sees actual space content after copying it into another location and changing mount point for storage
    When user of browser_unified creates "space6" space in Onezone
    And using docker, browser_unified creates directory (mkdir) /volumes/dir3
    And user of browser_unified adds "new_storage9" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
    And user of browser_unified sends support token for "space6" to user of browser_unified

    # support space
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified supports "space6" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage9
          size: 1
          unit: GiB

    And user of browser_unified sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser_unified sees that space support record for "space6" has appeared in Spaces page in Onepanel

    And user of browser_unified opens file browser for "space6" space
    And user of browser_unified sees file browser in files tab in Oneprovider page
    And user of browser_unified uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir

    And user of browser_unified copies "space6" space to /volumes/dir3

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_unified is idle for 2 seconds

    And user of browser_unified clicks on "Modify" button for "new_storage9" storage record in Storages page in Onepanel
    And user of browser_unified types "/volumes/dir3" to Mount point field in POSIX edit form for "new_storage9" storage in Onepanel
    And user of browser_unified clicks on Save button in edit form for "new_storage9" storage in Onepanel
    And user of browser_unified confirms committed changes in modal "Modify Storage"

    And user of browser_unified opens file browser for "space6" space
    And user of browser_unified sees file browser in files tab in Oneprovider page

    And user of browser_unified clicks and presses enter on item named "20B-1.txt" in file browser
    Then user of browser_unified sees that content of downloaded file "20B-1.txt" is equal to: "11111111111111111111"


  Scenario: User sees actual space content after copying it into another location and changing s3 bucket for storage
    When user of browser_unified creates "space7" space in Onezone

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser_unified clicks on Add storage backend button in storages page in Onepanel
    And user of browser_unified selects s3 from storage selector in storages page in Onepanel
    And user of browser_unified types "new_storage10" to Storage name field in s3 form in storages page in Onepanel
    And user of browser_unified types "http://volume-s3.dev-volume-s3-krakow.default:9000" to hostname field in s3 form in storages page in Onepanel
    And user of browser_unified types "test" to bucket name field in s3 form in storages page in Onepanel
    And user of browser_unified types "accessKey" to admin access key field in s3 form in storages page in Onepanel
    And user of browser_unified types "verySecretKey" to admin secret key field in s3 form in storages page in Onepanel
    And user of browser_unified clicks on Add button in add storage form in storages page in Onepanel
    And user of browser_unified sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser_unified sends support token for "space7" to user of browser_unified

    # support space
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified supports "space7" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage10
          size: 1
          unit: GiB

    And user of browser_unified sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser_unified sees that space support record for "space7" has appeared in Spaces page in Onepanel

    And user of browser_unified opens file browser for "space7" space
    And user of browser_unified sees file browser in files tab in Oneprovider page
    And user of browser_unified uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir
    And user of browser_unified clicks on "Information" in context menu for "20B-1.txt"
    And user of browser_unified sees physical location path in file details and copies it into the clipboard

    And using REST, user creates s3 bucket "bucket2"
    And using REST, user of browser_unified copies item with recently copied path from "test" bucket into "bucket2" bucket

    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified clicks on "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_unified is idle for 2 seconds

    And user of browser_unified clicks on "Modify" button for "new_storage10" storage record in Storages page in Onepanel
    And user of browser_unified types "bucket2" to bucket name field in s3 edit form for "new_storage10" storage in Onepanel
    And user of browser_unified types "verySecretKey" to admin secret key field in s3 edit form for "new_storage10" storage in Onepanel
    And user of browser_unified clicks on Save button in edit form for "new_storage10" storage in Onepanel
    And user of browser_unified confirms committed changes in modal "Modify Storage"

    And user of browser_unified opens file browser for "space7" space
    And user of browser_unified sees file browser in files tab in Oneprovider page

    And user of browser_unified clicks and presses enter on item named "20B-1.txt" in file browser
    Then user of browser_unified sees that content of downloaded file "20B-1.txt" is equal to: "11111111111111111111"
