Feature: Create archive

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
                    - file1: 100
                    - file2


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

    Scenario: User creates archives
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Files of "space1" in the sidebar
      And user of browser sees file browser in files tab in Oneprovider page
      And user of browser clicks on menu for "dir1" directory in file browser
      And user of browser clicks "Datasets" option in data row menu in file browser
      And user of browser clicks Mark this directory as Dataset toggle on Datasets menu
      And user of browser clicks Close button on Datasets menu
      And user of browser clicks Datasets of "space1" in the sidebar
      And user of browser sees dataset browser in datasets tab in Oneprovider page
      And user of browser sees that item "dir1" has 0 archives
      And user of browser clicks on menu for "dir1" dataset in dataset browser
      And user of browser clicks "Create archive" option in data row menu in desktop browser
      And user of {browser_id} clicks Create button on create archive menu
      Then user of browser sees that item "dir1" has 1 archives
      And user of browser clicks on 1 in "dir1" archives
      And user of browser sees "Preserved Archived: 1 files, 3 B" on first archive state on Archive menu
