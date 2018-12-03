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
    And user1 mounts oneclient in /home/user1/onedata using token
    And opened browser with user1 logged to "onezone onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User creates file using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user1 sees that POSIX permission for item named "file1" in "space1" is "664" in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |



  Scenario Outline: User creates directory using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "dir1" in "space1" in <host2>
    And using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "775" in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User changes file permission using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client1>, user1 succeeds to set "775" POSIX permission for item named "file1" in "space1" in <host1>
    Then using <client2>, user1 sees that POSIX permission for item named "file1" in "space1" is "775" in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User changes directory permission using <client1> and sees its permission using <client2>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in <host1>
    And using <client1>, user1 succeeds to set "664" POSIX permission for item named "dir1" in "space1" in <host1>
    Then using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "664" in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |



  Scenario Outline: User changes file permission using <client1> and using <client2> sees that status-change time has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And user1 waits 2 seconds
    And using <client1>, user1 succeeds to set "775" POSIX permission for item named "file1" in "space1" in <host1>
    Then using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user1 sees that POSIX permission for item named "file1" in "space1" is "775" in <host2>
    And using <client2>, user1 sees that status-change time of item named "file1" in "space1" space is greater than modification time in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User changes directory permission using <client1> and using <client2> sees that status-change time has changed
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in <host1>
    And user1 waits 2 seconds
    And using <client1>, user1 succeeds to set "664" POSIX permission for item named "dir1" in "space1" in <host1>
    Then using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "664" in <host2>
    And using <client2>, user1 sees that status-change time of item named "dir1" in "space1" space is greater than modification time in <host2>

  Examples:
  | client1   | client2   | host1         | host2         |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User creates file using <client1> and changes its permission using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in <host2>
    Then using <client2>, user1 succeeds to set "775" POSIX permission for item named "file1" in "space1" in <host2>
    And using <client2>, user1 sees that POSIX permission for item named "file1" in "space1" is "775" in <host2>
    And using <client1>, user1 sees that POSIX permission for item named "file1" in "space1" is "775" in <host1>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |

  Scenario Outline: User creates directory using <client1> and changes its permission using <client2>
    When using <client1>, user1 succeeds to create directory named "dir1" in "space1" in <host1>
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in <host2>
    Then using <client2>, user1 succeeds to set "664" POSIX permission for item named "dir1" in "space1" in <host2>
    And using <client2>, user1 sees that POSIX permission for item named "dir1" in "space1" is "664" in <host2>
    And using <client1>, user1 sees that POSIX permission for item named "dir1" in "space1" is "664" in <host1>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |



