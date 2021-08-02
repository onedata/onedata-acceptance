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
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 Archives
    And user of browser clicks on menu for "dir4" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser writes "first archive" into description text field
    And user of browser clicks on "Create" button in modal "Create Archive"
    Then user of browser sees that item "dir4" has 1 Archives
    And user of browser clicks on 1 in "dir4" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees "Preserved Archived: 1 files, 3 B" on first archive state in archive file browser


  Scenario: User sees directory tree in archive browser after creating plain archive
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # create archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on latest created archive
    Then user of browser sees that the file structure in archive file browser is as follow:
           - dir1:
               - dir2:
                 - dir3:
                   - file1: 100


  Scenario: User sees that newly created archive has new file and is different than archive created earlier after creating new plain archive
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # create archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 1 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on latest created archive
    Then user of browser sees that the file structure in archive file browser is as follow:
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

     #create archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on latest created archive
    Then user of browser sees that the file structure in archive file browser is as follow:
         - dir1:
             - dir2:
               - dir3:
                 - file1: 100
                 - 20B-0.txt

Scenario: User sees BagIt tag after creating BagIt archive
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    #create BagIt archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "BagIt" button in modal "Create Archive"
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees BagIt tag for latest created archive



Scenario: User sees BagIt metadata files and directory tree in „data” directory in archive browser after creating BagIt archive
      # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    #create BagIt archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "BagIt" button in modal "Create Archive"
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 2 in "dir1" Archives
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser double clicks on latest created archive
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
