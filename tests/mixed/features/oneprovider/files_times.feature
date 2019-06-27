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
    And effective support for user in provider:
        oneprovider-1:
            - user1
    And oneclient mounted in /home/user1/onedata using token by user1
    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


   Scenario Outline: User renames file using <client2> and using <client1> he sees that status-change time has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And user1 waits 2 second
    And using <client2>, user1 renames item named "file1" to "file2" in "space1" in oneprovider-1
    Then using <client1>, user1 succeeds to see item named "file2" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "file2" in "space1" space is equal to modification time in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "file2" in "space1" space is equal to access time in oneprovider-1

  Examples:
  | client1    | client2    |
  | oneclient1 | REST       |
  | oneclient1 | web GUI    |
  | REST	   | web GUI	|
  | REST       | oneclient1 |


   Scenario Outline: User changes file using <client2> and using <client1> sees that modification time has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And user1 waits 80 second
    And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "file1" in "space1" in oneprovider-1
    Then using <client1>, user1 sees that modification time of item named "file1" in "space1" space is not earlier than 70 seconds ago in oneprovider-1

  Examples:
  | client1   | client2    |
  | web GUI   | REST       |
  | web GUI   | oneclient1 |
