Feature: Basic dataset operations

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
                        - file1: 100
                    - dir2:
                        - dir3:
                          - dir4:
                            - dir5
                        - file2: 150
                    - file3: 160

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees Editor disabled label after marking dataset and metadata write protection
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser sees data protected status tag for "dir1" in file browser
    And user of browser sees metadata protected status tag for "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees Editor disabled label in Metadata modal
    And user of browser clicks on "Close" button in metadata modal


  Scenario: User sees that file has dataset tag with arrow after marking its parent directory as dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser double clicks on item named "dir1" in file browser
    And user of browser sees Dataset status tag with arrow for "file1" in file browser


  Scenario: User does not see dataset tag after removing dataset in dataset browser
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Remove dataset" option in data row menu in desktop browser
    And user of browser clicks Remove button on Remove Selected Dataset modal
    Then user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees only directories marked as dataset in dataset browser
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees "dir2" in dataset browser
    And user of browser double clicks on item named "dir2" in dataset browser
    And user of browser does not see "dir3" in dataset browser
    And user of browser sees "dir4" in dataset browser
    And user of browser double clicks on item named "dir4" in dataset browser
    And user of browser sees "dir5" in dataset browser


  Scenario: User sees labels and tag about features in directory dataset modal after giving its parent directories some features
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser sees that metadata write protection toggle is checked in Ancestor Dataset menu in Datasets modal
    And user of browser sees that data write protection toggle is checked in Ancestor Dataset menu in Datasets modal
    And user of browser clicks on Ancestor datasets option in Datasets modal
    And user of browser sees that data write protection toggle is checked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is unchecked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is checked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser sees that data write protection toggle is unchecked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser clicks Close button in Datasets modal


  Scenario: User sees data protection tag in dataset modal of file's hardlink
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks file browser hardlink button

    # mark file as dataset and set data protection
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal

    # check file's data protection
    And user of browser clicks file browser refresh button
    And user of browser clicks on menu for "file3(1)" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    Then user of browser sees "File's data is write protected" label in Datasets modal


  Scenario: User sees data and metadata protection tags on created file's hardlink
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks file browser hardlink button

    # mark file as dataset and set data protection
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal

    # mark hardlink as dataset and set data protection
    And user of browser clicks file browser refresh button
    And user of browser clicks on menu for "file3(1)" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal

    # check hardlink's data protection tags
    Then user of browser sees data protected status tag for "file3(1)" in file browser
    And user of browser sees metadata protected status tag for "file3(1)" in file browser


  Scenario:  User sees metadata and data protection tags on file and hardlink in different directories
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser changes current working directory to home using breadcrumbs

    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks file browser hardlink button
    And user of browser changes current working directory to home using breadcrumbs

    # mark directories as dataset and set data protection
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal

    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal

    # check file's and hardlink's protection status tagss
    And user of browser double clicks on item named "dir1" in file browser
    Then user of browser sees data protected status tag for "file1" in file browser
    And user of browser sees metadata protected status tag for "file1" in file browser
    And user of browser changes current working directory to home using breadcrumbs

    And user of browser double clicks on item named "dir2" in file browser
    And user of browser sees data protected status tag for "file1" in file browser
    And user of browser sees metadata protected status tag for "file1" in file browser





