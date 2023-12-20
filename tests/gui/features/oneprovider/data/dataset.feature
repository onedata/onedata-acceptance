Feature: Basic datasets operations

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
                        - dir2
                        - dir22
                    - dir2:
                        - dir3:
                          - dir4:
                            - dir5
                        - file2: 150
                    - file3: 160

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that file has dataset tag set after marking it as dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on "Establish dataset" button in modal "Datasets"
    And user of browser clicks on "X" button in modal "Datasets"
    Then user of browser sees Dataset status tag for "dir1" in file browser


  Scenario: User sees Editor disabled label after marking dataset and metadata write protection
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser checks metadata write protection toggle in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"

    Then user of browser sees data protected status tag for "dir1" in file browser
    And user of browser sees metadata protected status tag for "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees "Editor disabled" label in metadata panel


  Scenario: User sees inherited dataset status tag after marking its parent directory as dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    Then user of browser sees inherited status tag for "file1" in file browser
    And user of browser clicks on inherited status tag for "file1" in file browser
    And user of browser sees Dataset status tag for "file1" in file browser


  Scenario: User does not see dataset tag after removing dataset in dataset browser
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Remove" option in data row menu in dataset browser
    And user of browser clicks on "Remove" button in modal "Remove Selected Dataset"
    And user of browser clicks "Files" of "space1" space in the sidebar
    Then user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in dataset browser after marking directories as dataset
    When user of browser creates dataset for item "dir2" in "space1"
    And user of browser goes to "/dir2/dir3" in file browser
    And user of browser creates dataset for item "dir4" in "space1"
    And user of browser clicks and presses enter on item named "dir4" in file browser
    And user of browser creates dataset for item "dir5" in "space1"

    Then user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that the item structure in dataset browser is as follow:
          - dir2:
              - dir4:
                  - dir5


  Scenario: User sees metadata, data write protection toggles checked on ancestors list in directory dataset modal after marking its parent directories
    When user of browser creates dataset for item "dir2" in "space1"
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"

    And user of browser goes to "/dir2/dir3" in file browser
    And user of browser creates dataset for item "dir4" in "space1"
    And user of browser clicks on menu for "dir4" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser checks metadata write protection toggle in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"

    Then user of browser clicks and presses enter on item named "dir4" in file browser
    And user of browser clicks on menu for "dir5" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser sees that metadata write protection toggle is checked in Ancestor Datasets row in Datasets modal
    And user of browser sees that data write protection toggle is checked in Ancestor Datasets row in Datasets modal
    And user of browser sees that data write protection toggle is checked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is unchecked on "/space1/dir2" in ancestors list
    And user of browser sees that metadata write protection toggle is checked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser sees that data write protection toggle is checked on "/space1/dir2/dir3/dir4" in ancestors list
    And user of browser clicks on "X" button in modal "Datasets"


  Scenario: User does not see dataset tag in file browser and see directory in Detached tab after detaching dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    # detach dataset
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees item(s) named "dir1" in dataset browser
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser does not see Dataset status tag for "dir1" in file browser


  Scenario: User sees directory tree in Detached tab after detaching directories
    When user of browser creates dataset for item "dir2" in "space1"
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser clicks and presses enter on item named "dir3" in file browser
    And user of browser creates dataset for item "dir4" in "space1"
    And user of browser clicks and presses enter on item named "dir4" in file browser
    And user of browser creates dataset for item "dir5" in "space1"

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir2" in dataset browser

    # detach dataset
    And user of browser clicks on menu for "dir3" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    # detach dataset
    And user of browser clicks and presses enter on item named "dir4" in dataset browser
    And user of browser clicks on menu for "dir5" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees that the item structure in dataset browser is as follow:
          - dir3:
              - dir5
    And user of browser clicks on attached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that the item structure in dataset browser is as follow:
          - dir2:
              - dir4


  Scenario: User sees dataset in attached tab after reattaching detached dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    # detach dataset
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Reattach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Reattach Dataset"
    Then user of browser clicks on attached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees item(s) named "dir1" in dataset browser


  Scenario: User fails to reattach dataset after deleting directory
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    # detach dataset
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    # delete directory
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    Then user of browser sees that "Reattach" option is disabled in opened item menu in dataset browser


  Scenario: User sees dataset in detached tab after deleting directory
    When user of browser creates dataset for item "dir1" in "space1"

    # delete directory
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees item(s) named "dir1" in dataset browser


  Scenario: User fails to delete child directory after marking parent directory dataset data write protection
    When user of browser creates dataset for item "dir2" in "space1"
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"
    And user of browser clicks and presses enter on item named "dir2" in file browser

    And user of browser clicks on menu for "dir3" directory in file browser
    Then user of browser sees that "Delete" option is disabled in opened item menu in file browser


  Scenario: User sees data protection tag in dataset modal for hardlink of data protected file
    # create hardlink
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    # mark file as dataset and set data protection
    And user of browser clicks on menu for "file3" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on "Establish dataset" button in modal "Datasets"
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"

    # check hardlink's data protection
    And user of browser clicks on menu for "file3(1)" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    Then user of browser sees "File's data is write protected" label in Datasets modal


  # TODO VFS-10555 check hardlink inherited protection flags behavior


  # checks bugfix from VFS-8739
  Scenario: User sees proper list of datasets when their names have common prefix and end with digit
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser creates dataset for item "dir22" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in files tab in Oneprovider page
    Then user of browser sees that the item structure in dataset browser is as follow:
          - dir1:
              - dir2
              - dir22
    And user of browser clicks and presses enter on item named "dir1" in dataset browser
    And user of browser sees that there are 2 items in dataset browser


  Scenario: User sees path to dataset root file after creating datasets and entering them
    When user of browser creates dataset for item "dir2" in "space1"
    And user of browser goes to "/dir2/dir3/dir4" in file browser
    And user of browser creates dataset for item "dir5" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in files tab in Oneprovider page
    Then user of browser sees path to root file: "/space1/dir2" for "dir2" dataset in dataset browser
    And user of browser clicks and presses enter on item named "dir2" in dataset browser
    And user of browser sees path to root file: "/space1/dir2/dir3/dir4/dir5" for "dir5" dataset in dataset browser


  Scenario: User sees same paths to detached datasets root files after deleting dataset root file and recreating file marked as dataset with the same name
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to remove "dir1" in "space1"
    And user of browser creates directory "dir1"
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Detach" option in data row menu in dataset browser
    And user of browser clicks on "Proceed" button in modal "Detach Dataset"
    And user of browser clicks on detached view mode on dataset browser page
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    Then user of browser sees that one of two listed datasets "dir1" has got root file deleted
    And user of browser sees two same root file paths "/space1/dir1" for datasets named "dir1"


  Scenario Outline: User selects desirable columns to be visible and can see only them in dataset browser
    # dataset need to be created otherwise columns won`t show up
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in files tab in Oneprovider page

    And user of browser enables only <columns_list> columns in columns configuration popover in dataset browser table
    Then user of browser sees only <columns_list> columns in dataset browser
    And user of browser refreshes site
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees only <columns_list> columns in dataset browser

  Examples:
    |columns_list|
    |["Archives"]|
    |[]          |
