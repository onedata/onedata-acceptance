Feature: Tests for creating symlinks and hardlinks using web GUI/REST

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
                  - dir1
                  - file1
    And opened browser with user1 signed in to "onezone" service


  Scenario: User creates hardlink using REST and can see correct info about it using web GUI
    When using REST, user user1 creates hardlink of "file1" placed in "dir1" directory in "space1" in oneprovider-1
    And using REST, user user1 sees that "file1" hardlinks point to "[dir1/file1, file1]" in space "space1" in oneprovider-1
    And using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser clicks on hardlink tag for "file1" in file browser in oneprovider-1
    Then using web GUI, user of browser sees paths ["space1/dir1/file1", "space1/file1"] of hardlinks in "File details" modal


  Scenario: User creates hardlink using web GUI and can see correct info about it using REST
    When using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser creates hardlink of "file1" placed in "/dir1" directory in "space1" in oneprovider-1
    And using REST, user user1 sees that "file1" hardlinks point to "[dir1/file1, file1]" in space "space1" in oneprovider-1
    Then using REST, user user1 sees that the path of "dir1/file1" hardlink is "file1" in space "space1" in oneprovider-1


  Scenario: User creates symlink using REST and can see correct info about it using web GUI and REST
    When using REST, user user1 creates symlink located in "/dir1/file1" pointing to "file1" in "space1" in file browser in oneprovider-1
    And using REST, user user1 sees that "dir1/file1" symlink points to "file1" in "space1" in oneprovider-1

    And using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser goes to "/dir1" in file browser
    And using web GUI, user of browser clicks on menu for "file1" file in file browser
    And using web GUI, user of browser clicks "Information" option in data row menu in file browser
    And using web GUI, user of browser sees that "Symbolic link details" modal has appeared
    Then using web GUI, user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal


  Scenario: User creates symlink using web GUI and can see correct info about it using REST
    When using web GUI, user of browser opens file browser for "space1" space
    And using web GUI, user of browser creates symlink located in "/dir1" pointing to "file1" in "space1" in file browser in oneprovider-1
    Then using REST, user user1 sees that "dir1/file1" symlink points to "file1" in "space1" in oneprovider-1
    