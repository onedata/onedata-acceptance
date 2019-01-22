Feature: File content tests

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
    And opened browser with user1 logged to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User writes to file using <client2> and using <client1> sees that file's content has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "file1" in "space1" in oneprovider-1
    Then using <client1>, user1 reads "TEST TEXT ONEDATA" from file named "file1" in "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | oneclient1 |
  | web GUI    | oneclient1 |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |


  Scenario Outline: User appends text to file using <client2> and using <client1> sees that file's content has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 appends " APPENDED DATA" to file named "file1" in "space1" in oneprovider-1
    Then using <client1>, user1 reads "TEST TEXT ONEDATA APPENDED DATA" from file named "file1" in "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | oneclient1 |
  | web GUI    | oneclient1 |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |


  Scenario Outline: User replaces word in file using <client2> and using <client1> sees that file's content has changed
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 writes "TEST ONEDATA1 TEST ONEDATA2 TEST ONEDATA3" to file named "file1" in "space1" in oneprovider-1
    And using <client2>, user1 replaces "TEST" with "SYSTEM" in file named "file1" in "space1" in oneprovider-1
    Then using <client1>, user1 reads "SYSTEM ONEDATA1 SYSTEM ONEDATA2 SYSTEM ONEDATA3" from file named "file1" in "space1" in oneprovider-1

  Examples:
  | client1   | client2    |
  | REST      | oneclient1 |
  | web GUI   | oneclient1 |


   Scenario Outline: User removes file right after read using <client2> and using <client1> sees that it has been removed
     When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
      - dir1:
          - dir2:
              - file1
     And using <client2>, user1 writes "TEST TEXT ONEDATA" to file named "dir1/dir2/file1" in "space1" in oneprovider-1
     And using <client2>, user1 reads "TEST TEXT ONEDATA" from file named "dir1/dir2/file1" in "space1" in oneprovider-1
     And using <client2>, user1 succeeds to remove file named "dir1/dir2/file1" in "space1" in oneprovider-1
     Then using <client1>, user1 fails to see item named "dir1/dir2/file1" in "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | oneclient1 |
  | web GUI    | oneclient1 |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |


  Scenario Outline: User uploads file using <client1> and using <client2> he sees that it has appeared and has the same content
    When using <client1>, user1 uploads "20B-0.txt" to "space1" in oneprovider-1
    Then using <client2>, user1 succeeds to see item named "20B-0.txt" in "space1" in oneprovider-1
    And using <client2>, user1 reads "00000000000000000000" from file named "20B-0.txt" in "space1" in oneprovider-1

  Examples:
  | client1   | client2    |
  | web GUI   | REST       |
  | web GUI   | oneclient1 |
