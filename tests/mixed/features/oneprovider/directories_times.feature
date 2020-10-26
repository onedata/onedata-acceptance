Feature: Directories times tests

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


  Scenario Outline: User renames directory using <client2> and check status-change time using <client1>
    When using <client1>, user1 succeeds to create directory named "/dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to see item named "dir1" in "space1" in oneprovider-1

     # call sleep, to be sure that time of above and below operations is different
    And user1 waits 2 seconds
    And using <client2>, user1 renames item named "dir1" to "dir2" in "space1" in oneprovider-1
    Then using <client1>, user1 sees that status-change time of item named "dir2" in "space1" space is greater than modification time in oneprovider-1
    Then using <client1>, user1 sees that status-change time of item named "dir2" in "space1" space is <comparator_times> access time in oneprovider-1

  Examples:
  | client1    | client2    | comparator_times  |
  | oneclient1 | REST       | equal to          |
  | oneclient1 | web GUI    | greater than      |
  | REST       | web GUI    | greater than      |
  | REST       | oneclient1 | greater than      |


  Scenario Outline: User changes directory using <client2> and using <client1> sees that modification time has changed
    When using <client1>, user1 succeeds to create directory named "/dir1" in "space1" in oneprovider-1
    And using <client2>, user1 succeeds to create directory named "/dir1/dir2" in "space1" in oneprovider-1

    # call sleep, to be sure that time of above and below operations is different
    And user1 waits 2 second
    And using <client2>, user1 renames item named "dir1/dir2" to "dir1/dir3" in "space1" in oneprovider-1
    Then using <client1>, user1 sees that modification time of item named "dir1" in "space1" space is <comparator_times> access time in oneprovider-1
    And using <client1>, user1 sees that modification time of item named "dir1" in "space1" space is equal to status-change time in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "dir1/dir3" in "space1" space is greater than modification time in oneprovider-1
    And using <client1>, user1 sees that status-change time of item named "dir1/dir3" is equal to status-change time of item named "dir1" in "space1" space in oneprovider-1

  Examples:
  | client1    | client2    | comparator_times  |
  | oneclient1 | REST       | greater than      |
  | REST       | oneclient1 | greater than      |
  | oneclient1 | web GUI    | equal to          |
  | REST       | web GUI    | equal to          |


  Scenario Outline: User changes directory using web GUI and using <client1> sees that modification time has changed
    When using web GUI, user1 succeeds to create directory named "/dir1" in "space1" in oneprovider-1

    # call sleep, to be sure that time of above and below operations is different
    And user1 waits 80 second
    And using <client1>, user1 succeeds to create directory named "/dir1/dir2" in "space1" in oneprovider-1
    And using web GUI, user1 refreshes site
    Then using web GUI, user1 sees that modification time of item named "dir1" in current space is not earlier than 70 seconds ago in oneprovider-1

  Examples:
  | client1    |
  | REST       |
  | oneclient1 |
