Feature: Tests for creating symlinks and hardlinks in GUI

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
                    - file3
                    - file4
                  - file1
                  - file2
    And opened browser with user1 signed in to "onezone" service


  Scenario: User using GUI/REST, can see newly created with REST API hardlink
    When using REST, user user1 creates hardlink of "file1" placed in "dir1" directory in "space1" in oneprovider-1
    And using REST, user user1 sees that "file1" hardlinks point to "[dir1/file1, file1]" in space "space1" in oneprovider-1
    And using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser clicks on hardlink tag for "file1" in file browser in oneprovider-1
    Then using web GUI, user of browser sees paths ["space1/dir1/file1", "space1/file1"] of hardlinks in "File details" modal
    


  Scenario: Using REST we check that hardlinks created with GUI are the same which are returned by endpoint
    When using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser creates hardlink of "file1" placed in "/dir1" directory in "space1" in oneprovider-1
    And using REST, user user1 sees that "file1" hardlinks point to "[dir1/file1, file1]" in space "space1" in oneprovider-1
    Then using REST, user user1 can see that there is hardlink between "file1" and "dir1/file1" in space "space1" in oneprovider-1


  Scenario: Using GUI/REST we check that symlink created with REST is the same as returned by endpoint
    When using REST, user user1 creates symlink located in "/dir1/file5" pointing to "file1" in "space1" in file browser in oneprovider-1
    And using REST, user user1 sees that "dir1/file5" symlink points to "file1" in "space1" in oneprovider-1

    And using web GUI, user of browser opens file browser for "space1" space
    And user of browser goes to "/dir1" in file browser
    And using web GUI, user of browser clicks on menu for "file5" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    Then user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal

  Scenario: Using REST we check that symlink created with GUI is the same as returned by endpoint
    When using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser creates symlink located in "/dir1" pointing to "file1" in "space1" in file browser in oneprovider-1
    Then using REST, user user1 sees that "dir1/file1" symlink points to "file1" in "space1" in oneprovider-1
    