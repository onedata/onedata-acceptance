Feature: Access tokens tests

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
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service



  Scenario Outline: Using <client1>, user can see file after getting token with caveat set for path, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          path:
            - space: space1
              path: /dir1/dir2
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 succeeds to see item named "dir1/dir2/file2" using received access token in "space1" in oneprovider-1
    And using <client1>, user2 fails to see item named "file1" using received access token in "space1" in oneprovider-1
    And using <client1>, user2 fails to see item named "dir1/dir3" using received access token in "space1" in oneprovider-1


    Examples:
    | client1     |
    | REST        |
# TODO: VFS-8431
#   | oneclient1  |


  Scenario Outline: Using <client1>, user can rename file after getting token with caveat set for path, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          path:
            - space: space1
              path: /dir1/dir2
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 renames item named "dir1/dir2/file2" to "dir1/dir2/file3" using received access token in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "dir1/dir2/file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
# TODO: VFS-8431
#   | oneclient1  |


  Scenario Outline: Using <client1>, user can see file after getting token with caveat set for object ID, created by web GUI
    When using web GUI, user1 copies "dir1" ID to clipboard from "Directory Details" modal in space "space1" in oneprovider-1
    And using web GUI, user1 creates access token with caveats set for object which ID was copied to clipboard
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 succeeds to see item named "dir1/dir2/file2" using received access token in "space1" in oneprovider-1
    And using <client1>, user2 fails to see item named "file1" using received access token in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
# TODO: VFS-8431
#    | oneclient1  |


   Scenario Outline: Using <client1>, user can rename file after getting token with caveat set for object ID, created by web GUI
    When using web GUI, user1 copies "dir1" ID to clipboard from "File Details" modal in space "space1" in oneprovider-1
    And using web GUI, user1 creates access token with caveats set for object which ID was copied to clipboard
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 renames item named "dir1/dir2" to "dir1/dir4" using received access token in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "dir1/dir4" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
# TODO: VFS-8431
#    | oneclient1  |

