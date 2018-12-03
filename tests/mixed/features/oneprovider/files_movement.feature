Feature: Files movement tests

  Examples:
  | client1   | client2   | host1         | host2         |
  | web GUI   | oneclient | oneprovider-1 | client1       |
  | REST      | oneclient | oneprovider-1 | client1       |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |


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


 Scenario Outline: User moves file using <client2> and using <client1> sees that file has been moved
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
          - dir1:
              - dir2:
                  - file1
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 succeeds to move "space1/dir1/dir2/file1" to "space1/dir3/file1" in <host2>
    Then using <client1>, user1 sees that directory structure in "space1" space in <host1> is as follow:
          - dir1:
              - dir2
          - dir3:
              - file1


  Scenario Outline: User moves non-empty file using <client2> and using <client1> sees that its content has not changed
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
            - dir1:
                - dir2:
                    - file1
            - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "dir1/dir2/file1" in "space1" in <host2>
    And using <client2>, user1 succeeds to move "space1/dir1/dir2/file1" to "space1/dir3/file1" in <host2>
    Then using <client1>, user1 sees that directory structure in "space1" space in <host1> is as follow:
            - dir1:
                - dir2
            - dir3:
                - file1
    And using <client1>, user1 reads "TEST TEXT ONEDATA" from file named "dir3/file1" in "space1" in <host1>


  Scenario Outline: User copies file using <client2> and using <client1> sees that it has been copied
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
          - dir1:
              - dir2:
                  - file1
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 copies file named "space1/dir1/dir2/file1" to "space1/dir3/file1" in <host2>
    Then using <client1>, user1 sees that directory structure in "space1" space in <host1> is as follow:
          - dir1:
              - dir2:
                  - file1
          - dir3:
              - file1


  Scenario Outline: User copies non-empty file using <client2> and using <client1> sees that it has not changed
    When using <client1>, user1 creates directory structure in "space1" space on <host1> as follow:
          - dir1:
              - dir2:
                  - file1
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in <host2> is as previously created
    And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "dir1/dir2/file1" in "space1" in <host2>
    And using <client2>, user1 copies file named "space1/dir1/dir2/file1" to "space1/dir3/file1" in <host2>
    Then using <client1>, user1 sees that directory structure in "space1" space in <host1> is as follow:
          - dir1:
              - dir2:
                  - file1
          - dir3:
              - file1
    And using <client1>, user1 reads "TEST TEXT ONEDATA" from file named "dir3/file1" in "space1" in <host1>
    And using <client1>, user1 reads "TEST TEXT ONEDATA" from file named "dir1/dir2/file1" in "space1" in <host1>
