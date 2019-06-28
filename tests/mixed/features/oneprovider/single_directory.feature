Feature: Tests for basic operations on single directory

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


  Scenario Outline: User creates directory using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1


  Scenario Outline: User creates directory using <client1> and removes it using <client2>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
	And using <client2>, user1 succeeds to remove directory (rmdir) named "dir1" in "space1" in oneprovider-1
	Then using <client1>, user1 fails to see item named "dir1" in "space1" in oneprovider-1


  Scenario Outline: User removes empty directory using <client1> and using <client2> sees that it has disappeared
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
	And using <client1>, user1 succeeds to remove directory (rmdir) named "dir1" in "space1" in oneprovider-1
	Then using <client2>, user1 fails to see item named "dir1" in "space1" in oneprovider-1


  Scenario Outline: User fails to create directory with the same name as existing one using <client2> and using <client1> sees only one directory
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1
    Then using <client2>, user1 fails to create directory named "dir1" in "space1" in oneprovider-1
    And using <client1>, user1 sees that there is 1 item in "space1" in oneprovider-1
    And using <client2>, user1 sees that there is 1 item in "space1" in oneprovider-1
