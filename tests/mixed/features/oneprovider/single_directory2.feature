Feature: Tests for basic operations on single directory 2

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |
  | web GUI    | oneclient1 |


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
    And oneclient mounted in /home/user1/onedata using token by user1
    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User renames directory using <client2> and using <client1> sees that its name has changed
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 renames item named "dir1" to "dir2" in "space1" in oneprovider-1
    Then using <client1>, user1 succeeds to see item named "dir2" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "dir1" in "space1" in oneprovider-1


  Scenario Outline: User creates directory using <client1> and renames it using <client2>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    And using <client1>, user1 renames item named "dir1" to "dir2" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "dir2" in "space1" in oneprovider-1
    And using <client2>, user1 fails to see item named "dir1" in "space1" in oneprovider-1


  Scenario Outline: User creates directory using <client1>, removes it using <client2> and then recreates it using <client1>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to remove directory (rmdir) named "dir1" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "dir1" in "space1" in oneprovider-1
    And using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    And using <client1>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
