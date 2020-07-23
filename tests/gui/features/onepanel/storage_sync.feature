Feature: Onepanel features regarding storage sync (e.g. import/update)

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service

    And directory tree structure on local file system:
          browser2:
              - dir1: 5
              - dir2:
                  - dir21:
                      - dir211:
                          - dir2111: 4
                      - file2.txt: 11111
                  - dir22: 10
                  - file1.txt: 22222


  Scenario: User sees imported files after supporting space with import-enabled storage and sees difference after update configuration
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # configure import parameters
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    # confirm correct import configuration
    When user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Import strategy: Simple scan
          Max depth: 2

    And user of browser2 opens file browser for "space1" space

    # confirm import of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page
    Then user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21
                  - dir22
                  - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false

    # confirm update of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21:
                      - dir211
                      - file2.txt: 11111
                  - dir22: 10
                  - file1.txt


  Scenario: User sees that files are imported to depth defined by update configuration if it is larger than depth of import configuration
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true

    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2
          storage update:
                strategy: Simple scan
                max depth: 3
                scan interval [s]: 1

    # confirm import and update strategy
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser1 sees that Import strategy configuration for "space1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false

    # confirm import and update of files
    And user of browser2 opens file browser for "space1" space
    And user of browser2 is idle for 8 seconds

    And user of browser2 sees file browser in data tab in Oneprovider page
    Then user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21:
                      - dir211
                      - file2.txt: 11111
                  - dir22: 10
                  - file1.txt: 22222

    And user of browser1 revokes "space1" space support in "oneprovider-1" provider in Onepanel


  Scenario: User does not see files and directories that have been removed in storage mount point when delete option was enabled
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page

    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1
              delete enabled: true

    # confirm update of files
    And user of browser2 opens file browser for "space1" space

    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page
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

    And user of browser2 is idle for 8 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir22: 10


  Scenario: User sees file's update when update configuration is set
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel

    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # check content of imported file
    And user of browser2 opens file browser for "space1" space

    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21
                  - dir22
                  - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false

    # confirm update of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

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
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir2" in file browser
    And user of browser2 double clicks on item named "file1.txt" in file browser
    And user of browser2 sees that content of downloaded file "file1 (1).txt" is equal to: "2222234"


  Scenario: User does not see file's update when write once option is enabled
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # check content of imported file
    And user of browser2 opens file browser for "space1" space

    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21
                  - dir22
                  - file1.txt: 22222

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1
              write once: true

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: false

    # confirm update of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

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
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir2" in file browser
    And user of browser2 double clicks on item named "file1.txt" in file browser
    And user of browser2 sees that content of downloaded file "file1 (1).txt" is equal to: "22222"


  Scenario: User sees that files are deleted after synchronization when delete and write once options are enabled
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    # support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1
              delete enabled: true
              write once: true

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: true

    And user of browser2 opens file browser for "space1" space

    # confirm update of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

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

    And user of browser2 is idle for 8 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page

    Then user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir22: 10


  Scenario: User sees that directory is not synchronized after files update disable
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When user of browser2 creates "space1" space in Onezone
    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser2 copies dir2 to provider's storage mount point

    #support space
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 2

    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel

    # configure update parameters
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false

    And user of browser2 opens file browser for "space1" space

    # confirm update of files
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

    And user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21:
                      - dir211
                      - file2.txt: 11111
                  - dir22: 10
                  - file1.txt

    # disable files update
    And user of browser1 clicks on "Storage synchronization" navigation tab in space "space1"
    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 selects Disabled strategy from strategy selector in UPDATE CONFIGURATION in "space1" record in Spaces page in Onepanel
    And user of browser1 clicks on Save configuration button in "space1" record in Spaces page in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Cc]onfiguration.*space.*support.*changed.*

    # confirm correct update configuration
    And user of browser1 sees that Update strategy configuration for "space1" is as follow:
          Update strategy: Disabled

    # copy files to provider storage
     And user of browser2 copies dir1 to dir2 in provider's storage mount point

    # confirm that new files were not detected
    And user of browser2 is idle for 8 seconds
    And user of browser2 sees file browser in data tab in Oneprovider page

    Then user of browser2 sees that the file structure in file browser is as follow:
              - dir2:
                  - dir21:
                      - dir211
                      - file2.txt
                  - dir22: 10
                  - file1.txt
