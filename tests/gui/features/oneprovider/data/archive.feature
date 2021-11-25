Feature: Basic archives operations

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - dir2:
                        - dir3:
                          - file1: 100
                    - dir4:
                      - file2: 100

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees archive with "Preserved" state after creating it and waiting
    When user of browser creates dataset for item "dir4" in "space1"

    # create archive with description
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 archives
    And user of browser clicks on menu for "dir4" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser writes "first archive" into description text field in create archive modal
    And user of browser clicks on "Create" button in modal "Create Archive"

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser sees that 1st archive in archive browser has description: "first archive"
    And user of browser sees that archive with description: "first archive" in archive browser has status: "preserved", number of files: "1 file", size: "3 B"
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 1 archive


  Scenario: User sees that dataset does not have archive after purging archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 1 archive
    And user of browser clicks on archives count link for "dir4" in dataset browser
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Purge archive" option in data row menu in archive browser
    And user of browser writes "I understand that data of the archive will be lost" into confirmation input in Purge Archive modal
    And user of browser clicks on "Purge archive" button in modal "Purge archive"
    Then user of browser sees that page with text "NO ARCHIVES" appeared in archive browser
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 archives


  Scenario: User sees directory tree in archive browser after creating plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100


  Scenario: User sees that newly created archive has new file and is different than archive created earlier after creating new plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser succeeds to upload "20B-0.txt" to "/dir1/dir2/dir3" in "space1"
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: second archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "second archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "second archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100
               - 20B-0.txt


  Scenario: User sees BagIt tag after creating BagIt archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: BagIt
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees BagIt tag for archive with description: "first archive" on archives list in archive browser


  Scenario: User sees symbolic links on child datasets after creating nested archive on parent
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser goes to "/dir1/dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        create nested archives: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser goes to "/dir1/dir2" in archive file browser
    And user of browser sees symlink status tag for "dir3" in archive file browser
    And user of browser double clicks on item named "dir3" in archive file browser
    And user of browser sees symlink status tag for "file1" in archive file browser


  Scenario: User sees that dataset has more archives than its parent after creating nested archive on child dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        layout: plain
        create nested archives: True
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 1 archive
    And user of browser double clicks on item named "dir1" in dataset browser
    And user of browser sees that item "dir2" has 1 archive
    And user of browser succeeds to create archive for item "dir2" in "space1" with following configuration:
        layout: plain
        create nested archives: True
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser double clicks on item named "dir2" in dataset browser
    Then user of browser sees that item "dir3" has 2 archives
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 1 archive


  Scenario: User sees real directory tree of downloaded tar generated for nested archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        create nested archives: True

    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Copy archive ID" option in data row menu in archive browser
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Download (tar)" option in data row menu in archive browser
    Then user of browser sees that contents of downloaded archive TAR file (with ID from clipboard) in download directory have following structure:
          - archive:
            - dir1:
              - dir2:
                - dir3:
                  - file1: 100


  Scenario: User sees that files that did not change since creating last archive have 2 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain

    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser succeeds to upload "20B-0.txt" to "dir4" in "space1"
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: second archive
        layout: plain
        incremental:
            enabled: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "second archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file2" in archive file browser
    And user of browser does not see hardlink status tag for "20B-0.txt" in archive file browser


  Scenario: User sees that files that did not change since creating last two base archives have 3 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
        incremental:
            enabled: True
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: third archive
        layout: plain
        incremental:
            enabled: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "third archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file2" in archive file browser


  Scenario: User sees name of base archive after creating incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser goes back to dataset browser from archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: second archive
        layout: plain
        incremental:
            enabled: True
    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser sees that base archive for archive with description: "second archive" is archive with description: "first archive" on archives list in archive browser


  Scenario: User sees that the base archive in create archive modal is the latest created archive after enabling incremental toggle
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on Create Archive button in archive browser
    And user of browser checks "Incremental" toggle in modal "Create Archive"
    Then user of browser sees that base archive name in Create Archive modal is the same as latest created archive name


  Scenario: User creates incremental archive that has chosen base archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain

    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser copies archive with description: "first archive" name in archive browser to clipboard

    # create archive
    And user of browser clicks on Create Archive button in archive browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on menu for archive that name was copied to clipboard
    And user of browser clicks "Create incremental archive" option in data row menu in archive browser
    And user of browser clicks on "Create" button in modal "Create Archive"
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees that base archive for latest created archive is archive with description: "first archive" on archives list in archive browser


  Scenario: User sees DIP tag after creating archive with "Include DIP" option
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: DIP archive
        layout: plain
        include DIP: True
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees DIP tag for archive with description: "DIP archive" on archives list in archive browser



  Scenario: User sees BagIt metadata files and directory tree in AIP tab and directory tree in DIP tab in archive browser after creating archive with "BagIt" layout and "Include DIP" option
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: BagIt
        include DIP: True
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on the archive browser background to ensure lack of pop ups
    And user of browser double clicks on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - bagit.txt
         - data:
           - dir1:
             - dir2:
               - dir3:
                 - file1: 100
         - manifest-md5.txt
         - manifest-sha1.txt
         - manifest-sha256.txt
         - manifest-sha512.txt
         - metadata.json
         - tagmanifest-md5.txt
         - tagmanifest-sha1.txt
         - tagmanifest-sha256.txt
         - tagmanifest-sha512.txt
    And user of browser double clicks on archive with description: "first archive" on archives list in archive browser
    And user of browser clicks on DIP view mode on archive file browser page
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100


