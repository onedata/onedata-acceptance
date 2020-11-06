Feature: POSIX privileges tests
  
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


  Scenario Outline: User creates file using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 sees that POSIX permission for item named "file1" in "space1" is "664" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |


  Scenario Outline: User creates directory using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create directory named "/dir1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "775" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |
  | web GUI    | oneclient1 |


  Scenario Outline: Using <client3> user sees change of POSIX permissions an status-change time after changing permissions using <client2> for file created with <client1>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And user1 is idle for 2 seconds
    And using <client2>, user1 succeeds to set "775" POSIX permission for item named "file1" in "space1" in oneprovider-1
    Then using <client3>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client3>, user1 sees that POSIX permission for item named "file1" in "space1" is "775" in oneprovider-1
    And using <client3>, user1 sees that status-change time of item named "file1" in "space1" space is greater than modification time in oneprovider-1

  Examples:
  | client1     | client2    | client3    |
  | REST        | web GUI    | REST       |
  | oneclient1  | oneclient1 | REST       |
  | REST        | REST       | oneclient1 |
  | oneclient1  | web GUI    | oneclient1 |


  Scenario Outline: Using <client2> user sees change of POSIX permissions an status-change time after changing permissions using <client1> for directory
    When using <client1>, user1 succeeds to create directory named "/dir1" in "space1" in oneprovider-1
    And user1 is idle for 2 seconds
    And using <client1>, user1 succeeds to set "664" POSIX permission for item named "dir1" in "space1" in oneprovider-1
    Then using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "664" in oneprovider-1
    And using <client2>, user1 sees that status-change time of item named "dir1" in "space1" space is greater than modification time in oneprovider-1

  Examples:
  | client1    | client2    |
  | web GUI    | REST       |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | web GUI    | oneclient1 |

