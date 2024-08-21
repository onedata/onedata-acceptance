Feature: Onepanel features regarding storage sync (e.g. import/update)

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-1 in Onepanel
    And "new_storage" storage backend in "oneprovider-1" Oneprovider panel service used by admin with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
          imported storage: true

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service

    And directory tree structure on local file system:
          browser2:
            dir1: 5
            dir2:
              dir21:
                dir211:
                  dir2111: 4
                file2.txt:
                  content: 11111
              dir22: 10
              file1.txt:
                content: 22222


  Scenario: User sees imported files after supporting space and sees difference when max depth has changed
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # configure import parameters
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 2
            detect modifications: false
            detect deletions: false
            continuous scan: true

    # confirm correct import configuration
    When user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Max depth: 2
          Detect modifications: false
          Detect deletions: false
          Continuous scan: true

    And user of browser2 opens file browser for "space1" space

    # confirm import of files
    And user of browser2 sees file browser in files tab in Oneprovider page
    Then user of browser2 sees that the file structure in file browser is as follow:
           - dir2:
               - dir21
               - dir22
               - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page
    And user of browser1 sets import configuration in Storage import tab as following:
          max depth: 3
          scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Max depth: 3
          Scan interval [s]: 1

    # confirm update of files
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt


  Scenario: User does not see files and directories that have been removed in storage mount point when detect deletions option was enabled
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            detect modifications: false
            detect deletions: true
            max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # configure update parameters
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page

    And user of browser1 sets import configuration in Storage import tab as following:
          max depth: 3
          scan interval [s]: 1

    # confirm update of files
    And user of browser2 opens file browser for "space1" space

    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt

    # confirm detection of deleted files
    And user of browser2 removes dir2/dir21 from provider's storage mount point
    And user of browser2 removes dir2/file1.txt from provider's storage mount point

    And user of browser2 refreshes site
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir22: 10


  Scenario: User sees file's update when detect modifications is set
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            detect deletions: false
            detect modifications: false
            max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel

    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # check content of imported file
    And user of browser2 opens file browser for "space1" space

    And user of browser2 sees file browser in files tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page
    And user of browser1 sets import configuration in Storage import tab as following:
          max depth: 3
          detect modifications: true
          scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Max depth: 3
          Scan interval [s]: 1
          Detect modifications: true
          Detect deletions: false

    # confirm update of files
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt

    # confirm change of file content
    And user of browser2 appends "34" to dir2/file1.txt file in provider's storage mount point

    And user of browser2 is idle for 10 seconds
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 clicks and presses enter on item named "dir2" in file browser
    And user of browser2 clicks and presses enter on item named "file1.txt" in file browser
    And user of browser2 sees that content of downloaded file "file1 (1).txt" is equal to: "2222234"


  Scenario: User does not see file's update when detect modifications is disabled
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # check content of imported file
    And user of browser2 opens file browser for "space1" space

    And user of browser2 sees file browser in files tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page
    And user of browser1 sets import configuration in Storage import tab as following:
          max depth: 3
          detect modifications: false
          scan interval [s]: 1

    # confirm correct update
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Max depth: 3
          Detect modifications: false
          Detect deletions: true
          Continuous scan: true
          Scan interval [s]: 1

    # confirm update of files
    And user of browser2 sees file browser in files tab in Oneprovider page

    Then user of browser2 sees that the file structure in file browser is as follow:
           - dir2:
               - dir21:
                   - dir211
                   - file2.txt: 11111
               - dir22: 10
               - file1.txt

    # files in gui are not updated after local changes
    And user of browser2 appends "34" to dir2/file1.txt file in provider's storage mount point
    And user of browser2 is idle for 10 seconds
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 clicks and presses enter on item named "dir2" in file browser
    And user of browser2 clicks and presses enter on item named "file1.txt" in file browser
    And user of browser2 sees that content of downloaded file "file1 (1).txt" is equal to: "22222"


  Scenario: User sees that files are deleted after synchronization when detect deletions is enabled and detect modifications is disabled
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # configure update parameters
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page
    And user of browser1 sets import configuration in Storage import tab as following:
          max depth: 3
          detect deletions: true
          detect modifications: false
          scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Max depth: 3
          Detect deletions: true
          Detect modifications: false
          Continuous scan: true
          Scan interval [s]: 1

    And user of browser2 opens file browser for "space1" space

    # confirm update of files
    And user of browser2 sees file browser in files tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt

    # confirm detection of deleted files
    And user of browser2 removes dir2/dir21 from provider's storage mount point
    And user of browser2 removes dir2/file1.txt from provider's storage mount point

    And user of browser2 refreshes site
    And user of browser2 sees file browser in files tab in Oneprovider page

    Then user of browser2 sees that the file structure in file browser is as follow:
           - dir2:
               - dir22: 10


  Scenario: User sees that directory is not synchronized automatically when continuous scan is disabled
    Given there is no "dir2/dir1" in provider's storage mount point
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    #support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 3
            detect modifications: true
            detect deletions: true
            continuous scan: true
            scan interval [s]: 1

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    And user of browser2 opens file browser for "space1" space

    # confirm update of files
    And user of browser2 sees file browser in files tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt
              - dir22: 10
              - file1.txt

    # disable continuous scan
    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage import in Spaces page
    And user of browser1 sets import configuration in Storage import tab as following:
          continuous scan: false

    # confirm that continuous scan was disabled
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Detect modifications: true
          Detect deletions: true
          Continuous scan: False

    And user of browser2 copies dir1 to dir2 in provider's storage mount point

    # confirm that new files were not detected
    And user of browser2 sees file browser in files tab in Oneprovider page
    Then user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt
              - dir22: 10
              - file1.txt


  Scenario: User synchronizes directory manually when continuous scan is disabled
    Given there is no "dir2/dir1" in provider's storage mount point
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 3
            detect modifications: true
            detect deletions: true
            continuous scan: false

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    And user of browser2 opens file browser for "space1" space

    And user of browser2 copies dir1 to dir2 in provider's storage mount point

    # confirm that new files were not detected
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt
              - dir22: 10
              - file1.txt

    And user of browser1 clicks on "Storage import" navigation tab in space "space1"
    And user of browser1 clicks on "Start scan" button in storage import tab in Onepanel
    And user of browser1 waits until scanning is finished in storage import tab in Onepanel

    And user of browser2 sees file browser in files tab in Oneprovider page
    Then user of browser2 sees that the file structure in file browser is as follow:
          - dir2:
              - dir1: 5
              - dir21:
                  - dir211
                  - file2.txt
              - dir22: 10
              - file1.txt
