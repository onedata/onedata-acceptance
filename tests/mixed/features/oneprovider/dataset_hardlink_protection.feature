Feature: Hardlinks of a data and metadata protected file inherites this protection

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

  # TODO VFS-10555 check hardlink inherited protection flags behavior
  Scenario: User can see that hardlink inherited data and metadata protection flags from its target file
    When user of browser opens file browser for "space1" space

    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    And user of browser clicks on menu for "file1" file in file browser

    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on "Establish dataset" button in modal "Datasets"
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser checks metadata write protection toggle in Write Protection modal
    And user of browser clicks on "X" button in modal "Datasets"

    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees "Editor disabled" label in metadata panel
    And user of browser clicks on "X" button in modal "File details"

    # And user of browser clicks on menu for "file1(1)" file in file browser
    # Then user of browser sees that "Delete" option is disabled in opened item menu in file browser
    
    Then using REST, user1 fails to append "1234" to file named "file1(1)" in "space1" in oneprovider-1


  Scenario: User can see that hardlink, placed in non data protected dataset inherited protection from its target file, placed in data protected dataset
    When user of browser opens file browser for "space1" space

    And user of browser goes to "dir1" in file browser

    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser goes to "../dir2" in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar
    And user of browser goes to ".." in file browser

    # And user of browser creates dataset with data and metadata write protection flags for item "dir1" in "space1"

    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on "Establish dataset" button in modal "Datasets"
    And user of browser checks data write protection toggle in Datasets modal
    And user of browser checks metadata write protection toggle in Write Protection modal
    And user of browser clicks on "X" button in modal "Datasets"

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

    # And user of browser clicks on menu for "file1" file in file browser
    # Then user of browser sees that "Delete" option is disabled in opened item menu in file browser

    # To demonstrate that this method works on non data protected, that are outside main space

    And using REST, user1 succeeds to append "1234" to file named "dir2/file3" in "space1" in oneprovider-1
    And user of browser downloads item "file3" by clicking and pressing enter and then sees that content of downloaded file is equal to: "1234"

    Then using REST, user1 fails to append "1234" to file named "dir2/file2" in "space1" in oneprovider-1