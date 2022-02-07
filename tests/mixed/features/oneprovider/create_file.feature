Feature: Tests for creating file in Oneprovider

  Examples:
  | client1    | client2    | client3    |
  | REST       | web GUI    | REST       |
  | web GUI    | REST       | REST       |
  | oneclient1 | REST       | oneclient1 |
  | REST       | oneclient1 | REST       |
  | oneclient1 | web GUI    | oneclient1 |
  | web GUI    | oneclient1 | oneclient1 |


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


  Scenario Outline: User creates file using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client3>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User creates file using <client1> and removes it using <client2>
    When using <client3>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
	And using <client2>, user1 succeeds to remove file named "file1" in "space1" in oneprovider-1
	Then using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1

