Feature: Access tokens with caveats set for path tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
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
                        - dir2:
                          - file2: 11111
                        - dir3
    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service
    And using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          path:
            - space: space1
              path: /dir1/dir2
    And user1 sends token to user2
#    And user2 mounts oneclient using received token


  Scenario Outline: Using <client1>, user can see file after getting token with caveat set for path, created by web GUI
    Then using <client1>, user2 succeeds to see item named "dir1/dir2/file2" using received access token in "space1" in oneprovider-1
    And using <client1>, user2 fails to see item named "file1" using received access token in "space1" in oneprovider-1
    And using <client1>, user2 fails to see item named "dir1/dir3" using received access token in "space1" in oneprovider-1


    Examples:
    | client1     |
    | REST        |
#    | oneclient1  |


  Scenario Outline: Using <client1>, user can rename file after getting token with caveat set for path, created by web GUI
    When using <client1>, user2 renames item named "dir1/dir2/file2" to "dir1/dir2/file3" using received access token in "space1" in oneprovider-1
    Then using web GUI, user1 succeeds to see item named "dir1/dir2/file3" in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "dir1/dir2/file2" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
#    | oneclient1  |


  Scenario Outline: Using <client1>, user cannot create file at path that he does not have access after getting token with caveat set for path, created by web GUI
    When using <client1>, user2 fails to create file named "file4" using received token in "space1/dir1/dir3" in oneprovider-1
    And using <client1>, user2 succeeds to create file named "file5" using received token in "space1/dir1/dir2" in oneprovider-1
    Then using web GUI, user1 succeeds to see item named "dir1/dir2/file5" in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "dir1/dir3/file4" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
#    | oneclient1  |


  Scenario Outline: Using <client1>, user cannot remove file at path that he does not have access after getting token with caveat set for path, created by web GUI
    When using <client1>, user2 fails to remove file named "file1" using received token in "space1" in oneprovider-1
    And using <client1>, user2 succeeds to remove file named "dir1/dir2/file2" using received token in "space1" in oneprovider-1
    Then using web GUI, user1 fails to see item named "dir1/dir2/file2" in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "file1" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
#    | oneclient1  |