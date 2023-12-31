Feature: Files times tests

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
    And oneclient mounted using token by user1
    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


   Scenario Outline: User renames file using <client2> and using <client1> he sees that status-change time has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And user1 is idle for 2 seconds
    And using <client2>, user1 renames item named "file1" to "file2" in "space1" in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "file2" in "space1" space is greater than modification time in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "file2" in "space1" space is greater than access time in oneprovider-1

  Examples:
  | client1    | client2    |
  | oneclient1 | REST       |
  | oneclient1 | web GUI    |
  | REST       | web GUI    |
  | REST       | oneclient1 |


   Scenario Outline: User changes file using <client1> and using web GUI sees that modification time has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And user1 is idle for 80 seconds
    And using <client1>, user1 writes "TEST TEXT ONEDATA" to file named "file1" in "space1" in oneprovider-1
    And using web GUI, user1 refreshes site
    Then using web GUI, user1 sees that modification time of item named "file1" in current space is not earlier than 70 seconds ago in oneprovider-1

  Examples:
  | client1    |
  | REST       |
  | oneclient1 |
