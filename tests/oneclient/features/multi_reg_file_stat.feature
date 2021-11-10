Feature: Multi_regular_file_stat

  Background:
    Given oneclients [client11, client21]
      mounted in [/home/user1/onedata, /home/user2/onedata]
      on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [user1, user2]


  Scenario: Check file type when empty
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    Then user2 checks using shell stat if file type of space1/file1 is regular empty file on client21


  Scenario: Check file type when non-empty
    When user2 creates regular files [space1/file1] on client21
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user2 writes "TEST TEXT ONEDATA" to space1/file1 on client21
    Then file type of user1's space1/file1 is regular on client11


  Scenario: Check default access permissions
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    Then mode of user2's space1/file1 is 664 on client21


  Scenario: Change access permissions
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 changes space1/file1 mode to 211 on client11
    Then mode of user2's space1/file1 is 211 on client21


  Scenario: Increase regular file size with truncate
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 changes space1/file1 size to 1000000 bytes on client11
    Then size of user2's space1/file1 is 1000000 bytes on client21


  Scenario: Decrease regular file size with truncate
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 changes space1/file1 size to 1000000 bytes on client11
    And size of user2's space1/file1 is 1000000 bytes on client21
    And user1 changes space1/file1 size to 0 bytes on client11
    Then size of user2's space1/file1 is 0 bytes on client21


  Scenario: Fail to truncate regular file without write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 changes space1/dir1/file1 mode to 644 on client11
    And mode of user2's space1/dir1/file1 is 644 on client21
    And user2 fails to change space1/dir1/file1 size to 1000000 bytes on client21


  Scenario: Timestamps at creation
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    Then modification time of user2's space1/file1 is equal to access time on client21
    And status-change time of user2's space1/file1 is equal to access time on client21


  Scenario: Fail to update timestamps (touch) without write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 changes space1/dir1/file1 mode to 644 on client11
    And mode of user2's space1/dir1/file1 is 644 on client21
    And user2 fails to update [space1/dir1/file1] timestamps on client21


  Scenario: Update timestamps (touch) with write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 changes space1/dir1/file1 mode to 624 on client11
    And mode of user2's space1/dir1/file1 is 624 on client21
    And user2 updates [space1/dir1/file1] timestamps on client21
    Then modification time of user2's space1/dir1/file1 is equal to access time on client21


  Scenario: Access time
    When user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of write and read is different
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1 on client11
    And access time of user2's space1/file1 is greater than modification time on client21
    And access time of user2's space1/file1 is greater than status-change time on client21


  Scenario: Modification time
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    Then modification time of user2's space1/file1 is greater than access time on client21
    And modification time of user2's space1/file1 is equal to status-change time on client21


  Scenario: Status-change time when changing mode
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 changes space1/file1 mode to 211 on client11
    Then mode of user2's space1/file1 is 211 on client21
    And status-change time of user2's space1/file1 is greater than modification time on client21
    And status-change time of user2's space1/file1 is greater than access time on client21


  Scenario: Status-change time when renaming on storage
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user2 records [space1/file1] stats on client21
    And user1 is idle for 2 seconds
    # call sleep, to be sure that time of above and below operations is different
    And user1 renames space1/file1 to space1/file2 on client11
    Then user2 sees [file2] in space1 on client21
    And access time of user2's space1/file2 is equal to recorded one of space1/file1 on client21
    And modification time of user2's space1/file2 is equal to access time on client21
    And status-change time of user2's space1/file2 is not less than access time on client21
