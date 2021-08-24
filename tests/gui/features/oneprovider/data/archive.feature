Feature: Archive basic operation

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
    And user of browser sees that item "dir4" has 0 Archives
    And user of browser clicks on menu for "dir4" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser writes "first archive" into description text field in create archive modal
    And user of browser clicks on "Create" button in modal "Create Archive"

    Then user of browser sees that item "dir4" has 1 Archives
    And user of browser clicks on 1 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees "Preserved Archived: 1 files, 3 B" on first archive state in archive file browser


  Scenario: User sees that dataset does not have archive after purging archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
    And user of browser sees that item "dir4" has 1 Archives
    And user of browser clicks on 1 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks on menu for 1 archive in archive file browser
    And user of browser clicks "Purge archive" option in data row menu in archive file browser
    And user of browser writes "I understand that data of the archive will be lost" into confirmation box in Purge Archive modal
    And user of browser clicks on "Purge archive" button in modal "Purge archive"
    Then user of browser sees that page with text "NO ARCHIVES" appeared
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 Archives



  Scenario: User sees directory tree in archive browser after creating plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    Then user of browser sees that the file structure in archive file browser is as follow:
           - dir1:
               - dir2:
                 - dir3:
                   - file1: 100


  Scenario: User sees that newly created archive has new file and is different than archive created earlier after creating new plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    And user of browser sees that the file structure in archive file browser is as follow:
           - dir1:
               - dir2:
                 - dir3:
                   - file1: 100
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser

    # upload file
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    Then user of browser sees that the file structure in archive file browser is as follow:
         - dir1:
             - dir2:
               - dir3:
                 - file1: 100
                 - 20B-0.txt


Scenario: User sees BagIt tag after creating BagIt archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: BagIt
    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees BagIt tag for latest created archive


Scenario: User sees BagIt metadata files and directory tree in „data” directory in archive browser after creating BagIt archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
              layout: BagIt
    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    Then user of browser sees that the file structure in archive file browser is as follow:
         - bagit.txt
         - data:
             - dir1:
               - dir2:
                 - dir3:
                    - file1
         - manifest-md5.txt
         - manifest-sha1.txt
         - manifest-sha256.txt
         - manifest-sha512.txt
         - metadata.json
         - tagmanifest-md5.txt
         - tagmanifest-sha1.txt
         - tagmanifest-sha256.txt
         - tagmanifest-sha512.txt


  Scenario: User sees symbolic links on child datasets after creating nested archive on parent
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
          create nested archives: True

    Then user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    And user of browser double clicks on item named "dir1" in archive file browser
    And user of browser double clicks on item named "dir2" in archive file browser
    And user of browser sees symlink status tag for "dir3" in archive file browser
    And user of browser double clicks on item named "dir3" in archive file browser
    And user of browser sees symlink status tag for "file1" in archive file browser


  Scenario: User sees that dataset has more archives than its parent after creating nested archive on child dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"

    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
          create nested archives: True
    And user of browser sees that item "dir1" has 1 Archives
    And user of browser double clicks on item named "dir1" in dataset browser
    And user of browser sees that item "dir2" has 1 Archives
    And user of browser creates archive for item "dir2" in "space1" with following configuration:
          layout: plain
          create nested archives: True

    And user of browser double clicks on item named "dir2" in dataset browser
    Then user of browser sees that item "dir3" has 2 Archives
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 1 Archives


  Scenario: User sees directory tree after downloading tar with symlinks
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"

    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
          create nested archives: True

    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks on menu for 1 archive in archive file browser
    And user of browser clicks "Copy archive ID" option in data row menu in archive file browser
    And user of browser clicks on menu for 1 archive in archive file browser
    And user of browser clicks "Download (tar)" option in data row menu in archive file browser
    Then user of browser sees contents of downloaded "archive" TAR file in download directory has following structure:
                  - archive:
                      - dir1:
                        - dir2:
                          - dir3:
                             - file1


  Scenario: User sees that files that did not change since creating last archive have 2 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain

    # upload file
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
          incremental: True

    Then user of browser clicks on 2 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    And user of browser double clicks on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file2" in archive file browser
    And user of browser does not see hardlink status tag for "20B-0.txt" in archive file browser


  Scenario: User sees that files that did not change since creating last two archive (at least one incremental) have 3 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
          incremental: True
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
          incremental: True
    Then user of browser clicks on 2 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    And user of browser double clicks on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file2" in archive file browser


  Scenario: User sees name of base archive after creating incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
          incremental: True
    Then user of browser clicks on 2 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that base archive for latest created archive is 2 archive


  Scenario: User sees that base archive, in create archive modal, is latest created archive, after checking incremental toggle
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          layout: plain
    And user of browser clicks on 1 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks on Create Archive button in archive file browser
    And user of browser checks "Incremental" toggle in modal "Create Archive"
    Then user of browser sees that base archive name in Create Archive modal is the same as latest created archive name


  Scenario: User creates incremental archive that has chosen base archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser creates archive for item "dir4" in "space1" with following configuration:
          description: first_archive
          layout: plain

    And user of browser clicks on 1 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser copies 1 archive name in archive file browser to clipboard

    # create archive
    And user of browser clicks on Create Archive button in archive file browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on menu for archive that name was copied to clipboard
    And user of browser clicks "Create incremental archive" option in data row menu in archive file browser
    And user of browser clicks on "Create" button in modal "Create Archive"
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that base archive for latest created archive is 3 archive


  Scenario: User sees tag DIP after creating Include DIP archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
          include DIP: True
    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees DIP tag for latest created archive


  Scenario: User sees directory tree in DIP tab in archive browser after creating Include DIP archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain
          include DIP: True
    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    And user of browser clicks on DIP view mode on archive file browser page
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure in archive file browser is as follow:
           - dir1:
               - dir2:
                 - dir3:
                   - file1


  Scenario: User sees BagIt metadata files and directory tree in AIP tab and directory tree in DIP tab in archive browser after creating BagIt and Include DIP archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser creates archive for item "dir1" in "space1" with following configuration:
              layout: BagIt
              include DIP: True
    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on 1 archive
    Then user of browser sees that the file structure in archive file browser is as follow:
         - bagit.txt
         - data:
             - dir1:
               - dir2:
                 - dir3:
                    - file1
         - manifest-md5.txt
         - manifest-sha1.txt
         - manifest-sha256.txt
         - manifest-sha512.txt
         - metadata.json
         - tagmanifest-md5.txt
         - tagmanifest-sha1.txt
         - tagmanifest-sha256.txt
         - tagmanifest-sha512.txt
    And user of browser double clicks on 1 archive
    And user of browser clicks on DIP view mode on archive file browser page
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that the file structure in archive file browser is as follow:
             - dir1:
                 - dir2:
                   - dir3:
                     - file1

