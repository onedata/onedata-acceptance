Feature: Plain and BagIt archive basic operation

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
                            - file2: 100

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees directory tree in archive browser after creating plain archive
    # create dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks on "Close" button in modal "Datasets"

    #create archive
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir2" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on 1 in "dir2" Archives
    And user of browser double clicks on latest created archive
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure in archive file browser is as follow:
           - dir2:
               - dir3:
                 - dir4:
                   - file2: 100


