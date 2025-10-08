Feature: Inheriting protection from hardlink 

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
              - file1
              - dir1:
                - file2
              - dir2:
                - file3

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see that hardlink, placed in non data protected dataset inherits protection from its target file, which is placed in data protected dataset
    When user of browser opens file browser for "space1" space
    And user of browser creates hardlink of file located in "/dir1/file2" path and places it in "/dir2" path in "space1"
    And user of browser goes to ".." in file browser

    And user of browser creates dataset with data and metadata write protection flags for item "dir1" in "space1"
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser goes to "dir2" in file browser

    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser sees "File's data is write protected" label in Datasets modal
    And user of browser sees "File's metadata is write protected" label in Datasets modal
    And user of browser clicks on "X" button in modal "Datasets"

    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees "Editor disabled" label in metadata panel
    And user of browser clicks on "X" button in modal "File details"

    Then using REST, user1 fails to append "1234" to file under a path "dir2/file2" in "space1" in oneprovider-1


  Scenario: User can see that hardlink inherited data and metadata protection flags from its target file, both are in main space
    When user of browser opens file browser for "space1" space
    And user of browser creates hardlink of "file1" file in space "space1" in file browser

    And user of browser creates dataset with data and metadata write protection flags for item "file1" in "space1"

    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees "Editor disabled" label in metadata panel
    And user of browser clicks on "X" button in modal "File details"
    
    Then using REST, user1 fails to append "1234" to file under a path "file1(1)" in "space1" in oneprovider-1