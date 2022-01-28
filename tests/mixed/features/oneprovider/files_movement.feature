Feature: Files movement tests

  Examples:
  | client1    | client2    |
  | web GUI    | oneclient1 |
  | REST       | oneclient1 |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |


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


 Scenario Outline: User moves file using <client2> and using <client1> sees that file has been moved
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
          - dir1:
              - dir2:
                  - 20B-0.txt
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 succeeds to move "space1/dir1/dir2/20B-0.txt" to "space1/dir3/20B-0.txt" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
          - dir1:
              - dir2
          - dir3:
              - 20B-0.txt


  Scenario Outline: User moves non-empty file using <client2> and using <client1> sees that its content has not changed
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - 20B-0.txt
            - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 writes "TEST TEXT ONEDATA FILE" to file named "dir1/dir2/20B-0.txt" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to move "space1/dir1/dir2/20B-0.txt" to "space1/dir3/20B-0.txt" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
            - dir1:
                - dir2
            - dir3:
                - 20B-0.txt
    And using <client1>, user1 reads "TEST TEXT ONEDATA FILE" from file named "dir3/20B-0.txt" in "space1" in oneprovider-1


  Scenario Outline: User copies file using <client2> and using <client1> sees that it has been copied
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
          - dir1:
              - dir2:
                  - 20B-0.txt
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 copies file named "space1/dir1/dir2/20B-0.txt" to "space1/dir3/20B-0.txt" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
          - dir1:
              - dir2:
                  - 20B-0.txt
          - dir3:
              - 20B-0.txt


  Scenario Outline: User copies non-empty file using <client2> and using <client1> sees that it has not changed
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
          - dir1:
              - dir2:
                  - 20B-0.txt
          - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 writes "TEST TEXT ONEDATA FILE" to file named "dir1/dir2/20B-0.txt" in "space1" in oneprovider-1
    And using <client2>, user1 copies file named "space1/dir1/dir2/20B-0.txt" to "space1/dir3/20B-0.txt" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
          - dir1:
              - dir2:
                  - 20B-0.txt
          - dir3:
              - 20B-0.txt
    And using <client1>, user1 reads "TEST TEXT ONEDATA FILE" from file named "dir3/20B-0.txt" in "space1" in oneprovider-1
    And using <client1>, user1 reads "TEST TEXT ONEDATA FILE" from file named "dir1/dir2/20B-0.txt" in "space1" in oneprovider-1
