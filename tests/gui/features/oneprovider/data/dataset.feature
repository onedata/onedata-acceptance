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
    And user of browser clicks on "Close" button in modal "Datasets"
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
    And user of browser clicks on "Close" button in modal "Datasets"
    Then user of browser double clicks on item named "dir1" in file browser
    And user of browser sees Dataset status tag with arrow for "file1" in file browser


  Scenario: User does not see dataset tag after removing dataset in dataset browser
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
    And user of browser clicks Remove button on Remove Selected Dataset modal
    Then user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in dataset browser after marking directories as dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    Then user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees "dir2" in dataset browser
    And user of browser double clicks on item named "dir2" in dataset browser
    And user of browser does not see "dir3" in dataset browser
    And user of browser sees "dir4" in dataset browser
    And user of browser double clicks on item named "dir4" in dataset browser
    And user of browser sees "dir5" in dataset browser


  Scenario: User sees metadata, data write protection toggles checked in directory dataset modal after marking its parent directories
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
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
    And user of browser clicks on "Close" button in modal "Datasets"


  Scenario: User does not see dataset tag in file browser and see directory in Detached tab after detaching dataset
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
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"
    And user of browser clicks on detached button on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees "dir1" in dataset browser
    Then user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in Detached tab after detaching directories
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks on menu for "dir3" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser double clicks on item named "dir2" in dataset browser
    And user of browser clicks on menu for "dir3" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"
    And user of browser double clicks on item named "dir4" in dataset browser
    And user of browser clicks on menu for "dir5" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"
    And user of browser clicks on detached button on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees "dir3" in dataset browser
    And user of browser double clicks on item named "dir3" in dataset browser
    And user of browser sees "dir5" in dataset browser
    And user of browser double clicks on item named "dir5" in dataset browser
    And user of browser sees that current working directory displayed in breadcrumbs on dataset browser is /dir3/dir5
    And user of browser clicks on attached button on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees "dir2" in dataset browser
    And user of browser double clicks on item named "dir2" in dataset browser
    And user of browser sees "dir4" in dataset browser
    And user of browser double clicks on item named "dir4" in dataset browser
    And user of browser sees that current working directory displayed in breadcrumbs on dataset browser is /dir2/dir4


