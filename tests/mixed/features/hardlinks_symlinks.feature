Feature: Hardlinks/symlinks with oneclient/REST

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
                  - dir2
                  - file1

    And oneclient mounted using token by user1
  
  Scenario: User creates hardlink with oneclient and can see it using oneclient/REST
    When using oneclient1, user user1 creates hardlink of "file1" placed in "dir1" directory in "space1"
    
    Then using oneclient1, user user1 can see that "space1/file1" and "space1/dir1/file1" are hardlinked
    And using REST, user user1 sees that the path of "dir1/file1" hardlink is "file1" in space "space1" in oneprovider-1 


  Scenario: User creates hardlink with REST and can see it using oneclient
    When using REST, user user1 creates hardlink of "file1" placed in "dir1" directory in "space1" in oneprovider-1
    Then using oneclient1, user user1 can see that "space1/file1" and "space1/dir1/file1" are hardlinked


  Scenario: User creates symlink with oneclient and can see it using oneclient/REST
    When using oneclient1, user user1 creates symlink located in "dir2" pointing to "file1" in "space1"

    Then using REST, user user1 sees that "dir2/file1" symlink points to "file1" in "space1" in oneprovider-1
    And using oneclient1, user user1 can see that file "space1/dir2/file1" is a symlink and points to "space1/file1"


  Scenario: User creates symlink with REST and can see it using oneclient
    When using REST, user user1 creates symlink located in "dir2/file1" pointing to "file1" in "space1" in file browser in oneprovider-1
    Then using oneclient1, user user1 can see that file "space1/dir2/file1" is a symlink and points to "space1/file1"
