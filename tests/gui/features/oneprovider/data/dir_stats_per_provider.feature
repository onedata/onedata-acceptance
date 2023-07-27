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
                        - file2: 11111
                        - file3: 11111
                    - dir2:
                        - file4: 11111
                        - file5: 11111
                        - file6: 11111
                    - dir3:
                        - file7: 11111
                        - file8: 11111
                        - file9: 11111
                        - file10: 11111
                        - file11: 11111
                        - file12: 11111
    And directory tree structure on local file system:
      browser:
        file13:
          size: 40 B
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service



  Scenario: User checks space's size stats - provider1 full, provider2 empty, both providers' stats enabled
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
    And user of browser sees that oneprovider-1 contains "12 files, 3 directories"
    And user of browser sees that oneprovider-2 contains "12 files, 3 directories"
#
  Scenario: User checks space's size stats - provider1 full, provider2 empty, provider2 stats disabled
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
#    And trace
    Then user of browser sees that logical size for oneprovider-1 is "60 B"
    And user of browser sees that physical size for oneprovider-1 is "60 B"
    And user of browser sees that oneprovider-1 contains "12 files, 3 directories"
    And user of browser sees that error message for oneprovider-2 is "Directory statistics are disabled."

  Scenario: User checks space's size stats - provider1 - 60 B, provider2 - 40 B, both providers' stats enabled
    When user of browser clicks "space1" on the spaces list in the sidebar
#    And trace
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-2" provider on providers page
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser creates directory "dir4"
    And user of browser clicks and presses enter on item named "dir4" in file browser
    And user of browser uses upload button from file browser menu bar to upload local file "file13" to remote current dir
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks on menu on breadcrumbs on file browser
    And user of browser clicks "Information" option in menu popup
    And user of browser clicks on "Size stats" navigation tab in "Directory Details" modal
    And user of browser clicks "Show statistics per provider" button on Size stats modal
#    And trace
    Then user of browser sees that logical size for oneprovider-1 is "100 B"
    And user of browser sees that logical size for oneprovider-1 is "100 B"
    And user of browser sees that physical size for oneprovider-1 is "60 B"
    And user of browser sees that physical size for oneprovider-2 is "40 B"
    And user of browser sees that oneprovider-1 contains "13 files, 4 directories"
    And user of browser sees that oneprovider-2 contains "13 files, 4 directories"

 Scenario: User checks space's size stats - provider1 - full, provider2 - full, both providers' stats enabled
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser replicates "dir1" to provider "oneprovider-2"
    And user of browser replicates "dir2" to provider "oneprovider-2"
    And user of browser replicates "dir3" to provider "oneprovider-2"
    And user of browser clicks on menu on breadcrumbs on file browser
    And user of browser clicks "Information" option in menu popup
    And user of browser clicks on "Size stats" navigation tab in "Directory Details" modal
    And user of browser clicks "Show statistics per provider" button on Size stats modal
    Then user of browser sees that logical size for oneprovider-1 is "60 B"
    And user of browser sees that logical size for oneprovider-2 is "60 B"
    And user of browser sees that physical size for oneprovider-1 is "60 B"
    And user of browser sees that physical size for oneprovider-2 is "60 B"
    And user of browser sees that oneprovider-1 contains "12 files, 3 directories"
    And user of browser sees that oneprovider-2 contains "12 files, 3 directories"

