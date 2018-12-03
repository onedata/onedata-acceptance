Feature: Tests for basic operations on sigle file in Oneprovider

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


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
    And user1 mounts oneclient in /home/user1/onedata using token
    And opened browser with user1 logged to "onezone onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User creates file using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>


  Scenario Outline: User creates file using <client1> and removes it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
	And using <client2>, user1 removes file named "file1" in "space1" in <host2>
	Then using <client1>, user1 fails to see item named "file1" in "space1" in <host1>


  Scenario Outline: User removes file using <client1> and using <client2> sees that it has disappeared
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
	And using <client1>, user1 removes file named "file1" in "space1" in <host1>
	Then using <client2>, user1 fails to see item named "file1" in "space1" in <host2>


  Scenario Outline: User creates file using <client1> and renames it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user1 renames item named "file1" to "file2" in "space1" in <host2>
    Then using <client1>, user1 succeeds to see item named "file2" in "space1" in <host1>
    And using <client1>, user1 fails to see item named "file1" in "space1" in <host1>


  Scenario Outline: User renames file using <client1> and using <client2> sees that its name has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client1>, user1 renames item named "file1" to "file2" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "file2" in "space1" in <host2>
    And using <client2>, user1 fails to see item named "file1" in "space1" in <host2>


  Scenario Outline: User creates file using <client1>, removes it using <client2> and then recreates it using <client1>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user1 removes file named "file1" in "space1" in <host2>

    And using <client2>, user1 fails to see item named "dir1/dir2/file1" in "space1" in <host2>
    And using <client1>, user1 fails to see item named "dir1/dir2/file1" in "space1" in <host1>

    And using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client1>, user1 succeeds to see item named "file1" in "space1" in <host1>
