Feature: Storage management using onepanel


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [oneprovider-1 provider panel, onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onepanel, Onezone] service
    And directory tree structure on local file system:
          browser2:
              - dir1: 70


  Scenario: User uploads files on freshly supported space on newly created storage
    # create new_storage POSIX storage
    When user of browser1 clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Add storage button in storages page in Onepanel
    And user of browser1 selects POSIX from storage selector in storages page in Onepanel
    And user of browser1 types "new_storage" to Storage name field in POSIX form in storages page in Onepanel
    And user of browser1 types "/volumes/storage" to Mount point field in POSIX form in storages page in Onepanel
    And user of browser1 clicks on Add button in add storage form in storages page in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser1 expands "new_storage" record on storages list in storages page in Onepanel
    And user of browser1 sees that "new_storage" Storage type is posix in storages page in Onepanel
    And user of browser1 sees that "new_storage" Mount point is /volumes/storage in storages page in Onepanel

    # create space
    And user of browser2 clicks create new space on spaces on left sidebar menu
    And user of browser2 types "hello_world2" on input on create new space page
    And user of browser2 clicks on create new space button
    And user of browser2 sees "hello_world2" has appeared on spaces

    # receive support token
    And user of browser2 clicks Providers of "hello_world2" on left sidebar menu
    And user of browser2 clicks Get support button on providers page
    And user of browser2 clicks Copy button on Get support page
    And user of browser2 sends copied token to user of browser1

    # support space
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of browser1 selects "new_storage" from storage selector in support space form in onepanel
    And user of browser1 types received token to Support token field in support space form in Onepanel
    And user of browser1 types "1" to Size input field in support space form in Onepanel
    And user of browser1 selects GiB radio button in support space form in Onepanel
    And user of browser1 clicks on Support space button in support space form in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "hello_world2" has appeared in Spaces page in Onepanel

    # go to provider
    And user of browser2 is idle for 2 seconds
    And user of browser2 refreshes site
    And user of browser2 clicks Providers of "hello_world2" on left sidebar menu
    And user of browser2 opened oneprovider-1 Oneprovider view in web GUI    

    # create tmp dir and upload there 70 files
    And user of browser2 uses spaces select to change data space to "hello_world2"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees that current working directory displayed in breadcrumbs is hello_world2
    And user of browser2 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser2 sees that "New directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "dir100" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared
    And user of browser2 sees that item named "dir100" has appeared in file browser
    And user of browser2 double clicks on item named "dir100" in file browser
    And user of browser2 sees that current working directory displayed in breadcrumbs is hello_world2/dir100
    And user of browser2 uses upload button in toolbar to upload files from local directory "dir1" to remote current dir
    And user of browser2 waits for file upload to finish

    Then user of browser2 sees that there are 70 items in file browser

