Feature: Directory_stat

  Background:
    Given oneclient mounted in /home/user1/onedata using token by user1

    
  Scenario: Check file type
    When user1 creates directories [space1/dir1]
    Then file type of user1's space1/dir1 is directory


  Scenario: Check default access permissions
    When user1 creates directories [space1/dir1]
    Then mode of user1's space1/dir1 is 775


  Scenario: Change access permissions
    When user1 creates directories [space1/dir1]
    And user1 changes space1/dir1 mode to 211
    Then mode of user1's space1/dir1 is 211
    And user1 changes space1/dir1 mode to 755
    And mode of user1's space1/dir1 is 755


  Scenario: Timestamps at creation
    When user1 creates directories [space1/dir1]
    Then modification time of user1's space1/dir1 is equal to access time
    And status-change time of user1's space1/dir1 is equal to access time


  Scenario: Update timestamps
    When user1 creates directories [space1/dir1]
    And user1 is idle for 2 seconds
    And user1 creates directories [space1/dir1/dir2]
    And user1 updates [space1/dir1] timestamps
    # aim of above step is to call touch on space1/dir1
    # after creation of subdir access time and
    # modification time were different
    # after touch both will be updated to current time
    Then modification time of user1's space1/dir1 is equal to access time


  Scenario: Access time
    When user1 creates directories [space1/dir1]
    And user1 is idle for 2 seconds
    And user1 creates directories [space1/dir1/dir2]
    # two steps above ensure that access time is older than
    # modification time or status-change time and
    # will be modified on next access
    And user1 is idle for 2 seconds
    Then user1 sees [dir2] in space1/dir1
    # aim of above step is to call ls
    And access time of user1's space1/dir1 is greater than modification time
    And access time of user1's space1/dir1 is greater than status-change time


  Scenario: Modification time
    When user1 creates directories [space1/dir1]
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 creates directories [space1/dir1/dir2]
    Then modification time of user1's space1/dir1 is greater than access time
    And modification time of user1's space1/dir1 is equal to status-change time


  Scenario: Status-change time when renaming
    When user1 creates directories [space1/dir1]
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 renames space1/dir1 to space1/dir2
    Then status-change time of user1's space1/dir2 is greater to modification time
    And status-change time of user1's space1/dir2 is greater to access time


  Scenario: Status-change time when changing mode
    When user1 creates directories [space1/dir1]
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 changes space1/dir1 mode to 711
    Then status-change time of user1's space1/dir1 is greater than modification time
    And status-change time of user1's space1/dir1 is greater than access time
