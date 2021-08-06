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
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal

    And user of browser click data write protection toggle in Datasets modal
    And user of browser click metadata write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    Then user of browser sees data protected status tag for "dir1" in file browser
    And user of browser sees metadata protected status tag for "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees "Editor disabled" label in Metadata modal
    And user of browser clicks on "Close" button in metadata modal


  Scenario: User sees inherited dataset status tag after marking its parent directory as dataset
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser double clicks on item named "dir1" in file browser
    Then user of browser sees inherited dataset status tag for "file1" in file browser
    And user of browser sees Dataset status tag for "file1" in file browser


  Scenario: User does not see dataset tag after removing dataset in dataset browser
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Remove dataset" option in data row menu in dataset browser
    And user of browser clicks on "Remove" button in modal "Remove Selected Dataset"
    And user of browser clicks Files of "space1" in the sidebar
    Then user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in dataset browser after marking directories as dataset
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser double clicks on item named "dir2" in file browser

    # create dataset
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # create dataset
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    Then user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that the file structure in dataset browser is as follow:
          - dir2:
              - dir4:
                  - dir5



  Scenario: User sees metadata, data write protection toggles checked in directory dataset modal after marking its parent directories
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal

    And user of browser click data write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser

    # create dataset
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal

    And user of browser click metadata write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    Then user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser sees that metadata write protection toggle is checked in Ancestor Datasets row in Datasets modal
    And user of browser sees that data write protection toggle is checked in Ancestor Datasets row in Datasets modal
    And user of browser expands Ancestor datasets row in Datasets modal
    And user of browser sees that data write protection toggle is checked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is unchecked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is checked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser sees that data write protection toggle is unchecked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser clicks on "Close" button in modal "Datasets"


  Scenario: User does not see dataset tag in file browser and see directory in Detached tab after detaching dataset
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    # detach dataset
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees item(s) named "dir1" in dataset browser
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in Detached tab after detaching directories
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser double clicks on item named "dir2" in file browser

    # create dataset
    And user of browser clicks on menu for "dir3" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser double clicks on item named "dir3" in file browser

    # create dataset
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser double clicks on item named "dir4" in file browser

    # create dataset
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser double clicks on item named "dir2" in dataset browser

    # detach dataset
    And user of browser clicks on menu for "dir3" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"


    # detach dataset
    And user of browser double clicks on item named "dir4" in dataset browser
    And user of browser clicks on menu for "dir5" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees that the file structure in dataset browser is as follow:
          - dir3:
              - dir5
    And user of browser clicks on attached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that the file structure in dataset browser is as follow:
          - dir2:
              - dir4


 Scenario: User sees data protection tag in dataset modal for hardlink of data protected file
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    # mark file as dataset and set data protection
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click data write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # check hardlink's data protection
    And user of browser clicks on menu for "file3(1)" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    Then user of browser sees "File's data is write protected" label in Datasets modal


  Scenario: User sees both data and metadata protection tags on hardlinks if hardlinked files have these flags separately set
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    # mark file as dataset and set data write protection
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click data write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # mark hardlink as dataset and set metadata write protection
    And user of browser clicks on menu for "file3(1)" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click metadata write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # check hardlink's data protection tags
    Then user of browser sees data protected status tag for "file3(1)" in file browser
    And user of browser sees metadata protected status tag for "file3(1)" in file browser


  Scenario: User sees both data and metadata protection tags on hardlinks if hardlinked files inherit these flags from their parents separately
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser changes current working directory to home using breadcrumbs

    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar
    And user of browser changes current working directory to home using breadcrumbs

    # mark directory as dataset and set data write protection
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this directory as dataset toggle in Datasets modal
    And user of browser click data write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # mark directory as dataset and set metadata write protection
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this directory as dataset toggle in Datasets modal
    And user of browser click metadata write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    # check file's and hardlink's protection status tagss
    And user of browser double clicks on item named "dir1" in file browser
    Then user of browser sees data protected status tag for "file1" in file browser
    And user of browser sees metadata protected status tag for "file1" in file browser
    And user of browser changes current working directory to home using breadcrumbs

    And user of browser double clicks on item named "dir2" in file browser
    And user of browser sees data protected status tag for "file1" in file browser
    And user of browser sees metadata protected status tag for "file1" in file browser
