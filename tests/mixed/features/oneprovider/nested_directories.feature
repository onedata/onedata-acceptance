Feature: Tests for basic operations on nested directories

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


  Scenario Outline: User removes empty directory and its parents using <client2> and using <client1> sees that they have disappeared
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - dir1:
                - dir2:
                    - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 removes directory (rmdir -p) named "dir1/dir2/dir3" in "space1" in <host2>
    Then using <client1>, user1 fails to see item named "dir1" in "space1" in <host1>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User fails to remove non-empty directory (rmdir) using <client2> and using <client1> sees that it has not disappeared
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - dir1:
                - dir2:
                    - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 fails to remove directory (rmdir) named "dir1" in "space1" in <host2>
    Then using <client1>, user1 sees that directory structure in "space1" space in <host1> is as follow:
            - dir1:
                - dir2:
                    - dir3

  Examples:
  | client1   | client2   | host1         | host2         |
  | web GUI   | oneclient | oneprovider-1 | client1       |
  | REST      | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User removes non-empty directory using <client2> and using <client1> sees that they have disappeared
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - dir1:
                - child1
            - dir2:
                - child2
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 removes directory (rm -rf) named "dir1" in "space1" in <host2>
    Then using <client1>, user1 fails to see item named "dir1" in "space1" in <host1>

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User create directory structure using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - file1
            - dir1:
                - dir2:
                    - dir3
                    - dir4:
                        - file2
                        - file3
                        - dir5:
                            - dir6:
                                - dir7
                - dir8
                - file4
                - file5
                - dir9:
                    - file6
            - dir0
    Then using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |


  Scenario Outline: User create directory structure using <client1> and using <client2> sees that it has appeared v2
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - file1
            - dir1:
                - dir2:
                    - dir3:
                        - child1
                    - child1
                - child1

            - dir0
    Then using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client1       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client1       |
