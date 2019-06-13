Feature: Tests for basic operations on single file in Oneprovider

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
    And provider effectively supports user:
        oneprovider-1:
            - user1
    And oneclient mounted in /home/user1/onedata using token by user1
    And opened browser with user1 logged to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User creates file using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User creates file using <client1> and removes it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
	And using <client2>, user1 succeeds to remove file named "file1" in "space1" in oneprovider-1
	Then using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User removes file using <client1> and using <client2> sees that it has disappeared
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
	And using <client1>, user1 succeeds to remove file named "file1" in "space1" in oneprovider-1
	Then using <client2>, user1 fails to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User creates file using <client1> and renames it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 renames item named "file1" to "file2" in "space1" in oneprovider-1
    Then using <client1>, user1 succeeds to see item named "file2" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User renames file using <client1> and using <client2> sees that its name has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 renames item named "file1" to "file2" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "file2" in "space1" in oneprovider-1
    And using <client2>, user1 fails to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User creates file using <client1>, removes it using <client2> and then recreates it using <client1>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to remove file named "file1" in "space1" in oneprovider-1

    And using <client2>, user1 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1

    And using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
