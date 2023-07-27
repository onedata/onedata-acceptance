Feature: Data distribution operations for directories


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111
                        - file2: 22222
                        - file3: 33333
                    - dir2:
                        - file4: 11111
                        - file5: 22222
                        - file6: 33333
                    - dir3:
                        - file7: 11111
                        - file8: 22222
                        - file9: 33333
                        - file10: 11111
                        - file11: 22222
                        - file12: 33333
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service



  Scenario: User check's space's size stats - provider1 full, provider2 empty, both providers' stats enabled
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser clicks on menu on breadcrumbs on file browser
    And user of browser clicks "Information" option in menu popup
    And user of browser clicks on "Size stats" navigation tab in "Directory Details" modal
    And user of browser clicks "Show statistics per provider" button on Size stats modal
    Then user of browser sees that logical size for oneprovider-1 is "60 B"
    And user of browser sees that logical size for oneprovider-2 is "60 B"
    And user of browser sees that physical size for oneprovider-1 is "60 B"
    And user of browser sees that physical size for oneprovider-2 is "0 B"

  Scenario: User check's space's size stats - provider1 full, provider2 empty, both providers' stats enabled
    When user of browser clicks "space1" on the spaces list in the sidebar
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-2" provider on providers page
    And user of browser unchecks size statistics toggle in selected provider settings on providers page
    And user of browser clicks on "Disable" button in modal "Disable directory statistics"
    And user of browser clicks on "oneprovider-1" provider on providers page
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser clicks on menu on breadcrumbs on file browser
    And user of browser clicks "Information" option in menu popup
    And user of browser clicks on "Size stats" navigation tab in "Directory Details" modal
    And user of browser clicks "Show statistics per provider" button on Size stats modal
    And trace
    Then user of browser sees that logical size for oneprovider-1 is "60 B"
    And user of browser sees that physical size for oneprovider-1 is "60 B"
    And user of browser sees that error message for oneprovider-2 is "Directory statistics are disabled."
