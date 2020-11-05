Feature: Regular_file_stat

  Background:
    Given oneclient mounted in /home/user1/onedata using token by user1

    
  Scenario: Check file type when empty
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    Then user1 checks using shell stat if file type of space1/file1 is regular empty file

    
  Scenario: Check file type when non-empty
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    And user1 writes "TEST TEXT ONEDATA" to space1/file1
    Then file type of user1's space1/file1 is regular

    
  Scenario: Check default access permissions
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    Then mode of user1's space1/file1 is 664

    
  Scenario: Change access permissions
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    And user1 changes space1/file1 mode to 211
    Then mode of user1's space1/file1 is 211

    
  Scenario:  Increase regular file size with truncate
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    And user1 changes space1/file1 size to 1000000 bytes
    Then size of user1's space1/file1 is 1000000 bytes

    
  Scenario: Decrease regular file size with truncate
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    And user1 changes space1/file1 size to 1000000 bytes
    And size of user1's space1/file1 is 1000000 bytes
    And user1 changes space1/file1 size to 0 bytes
    Then size of user1's space1/file1 is 0 bytes

    
  Scenario: Timestamps at creation
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    Then modification time of user1's space1/file1 is equal to access time
    And status-change time of user1's space1/file1 is equal to access time

    
  Scenario: Update timestamps
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    And user1 updates [space1/file1] timestamps
    Then modification time of user1's space1/file1 is equal to access time

    
  Scenario: Access time
    When user1 writes "TEST TEXT ONEDATA" to space1/file1
    And user1 sees file1 in space1
    # call sleep, to be sure that time of write and read is different
    And user1 is idle for 2 seconds
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1
    And access time of user1's space1/file1 is greater than modification time
    And access time of user1's space1/file1 is greater than status-change time

    
  Scenario: Modification time
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    # call sleep, to be sure that time of above and below operations is different
    And user1is idle for 2 seconds
    And user1 writes "TEST TEXT ONEDATA" to space1/file1
    Then modification time of user1's space1/file1 is greater than access time
    And modification time of user1's space1/file1 is equal to status-change time

    
  Scenario: Status-change time when changing mode
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    # call sleep, to be sure that time of above and below operations is different
    And user1 is idle for 2 seconds
    And user1 changes space1/file1 mode to 711
    Then mode of user1's space1/file1 is 711
    And status-change time of user1's space1/file1 is greater than modification time
  
    And status-change time of user1's space1/file1 is greater than access time

  Scenario: Status-change time when renaming
    When user1 creates regular files [space1/file1]
    And user1 sees file1 in space1
    # call sleep, to be sure that time of above and below operations is different
    And user1 is idle for 2 seconds
    And user1 renames space1/file1 to space1/file2
    Then user1 sees file2 in space1
    And user1 doesn't see file1 in space1
    And user1 is idle for 2 seconds
    And status-change time of user1's space1/file2 is greater to modification time
    And status-change time of user1's space1/file2 is greater to access time
