Feature: Multi_directory_stat

  Background:
    Given oneclients [client11, client21]
      mounted in [/home/user1/onedata, /home/user2/onedata]
      on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [user1, user2]

    
  Scenario: Check file type
    When user1 creates directories [space1/dir1] on client11
    Then file type of user2's space1/dir1 is directory on client21


  Scenario: Check default access permissions
    When user1 creates directories [space1/dir1] on client11
    Then mode of user2's space1/dir1 is 775 on client21


  Scenario: Change access permissions
    When user1 creates directories [space1/dir1] on client11
    And user1 changes space1/dir1 mode to 211 on client11
    Then mode of user2's space1/dir1 is 211 on client21
    And user1 changes space1/dir1 mode to 775 on client11
    Then mode of user2's space1/dir1 is 775 on client21


  Scenario: Fail to change someone's file access permissions
    When user1 creates directories [space1/dir1] on client11
    And user2 fails to change space1/dir1 mode to 211 on client21
    And mode of user2's space1/dir1 is 775 on client21
    And mode of user1's space1/dir1 is 775 on client11


  Scenario: Timestamps at creation
    When user1 creates directories [space1/dir1] on client11
    Then modification time of user2's space1/dir1 is equal to access time on client21
    And status-change time of user2's space1/dir1 is equal to access time on client21


  Scenario: Fail to update timestamps (touch) without write permission
    # touch space1/dir1
    When user1 creates directories [space1/dir1] on client11
    And user1 changes space1/dir1 mode to 755 on client11
    And user1 creates directories [space1/dir1/dir2] on client11
    And user2 fails to update [space1/dir1] timestamps on client21
    # updating timestamps without write permission should fail


  Scenario: Update timestamps (touch) with write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 waits 2 second
    And user1 changes space1/dir1 mode to 725 on client11
    And user1 creates directories [space1/dir1/dir2] on client11
    And user2 updates [space1/dir1] timestamps on client21
    # aim of above step is to call touch on space1/dir1
    # after creation of subdir access time and
    # modification time were different
    # after touch both will be updated to current time
    Then modification time of user2's space1/dir1 is equal to access time on client21


  Scenario: Access time
    When user1 creates directories [space1/dir1] on client11
    And user1 waits 2 second
    And user1 creates directories [space1/dir1/dir2] on client11
    # two steps above ensure that access time is older than
    # modification time or status-change time and
    # will be modified on next access
    And user1 waits 2 second
    Then user1 sees [dir2] in space1/dir1 on client11
    #aim of above step is to call ls
    And access time of user2's space1/dir1 is greater than modification time on client21
    And access time of user2's space1/dir1 is greater than status-change time on client21


  Scenario: Modification time
    When user1 creates directories [space1/dir1] on client11
    And user1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    And user1 creates directories [space1/dir1/dir2] on client11
    Then modification time of user2's space1/dir1 is greater than access time on client21
    And modification time of user2's space1/dir1 is equal to status-change time on client21


  Scenario: Status-change time when renaming
    When user1 creates directories [space1/dir1] on client11
    When user1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    When user1 renames space1/dir1 to space1/dir2 on client11
    Then status-change time of user2's space1/dir2 is equal to modification time on client21
    Then status-change time of user2's space1/dir2 is equal to access time on client21


  Scenario: Status-change time when changing mode
    When user1 creates directories [space1/dir1] on client11
    When user1 waits 2 second
    # call sleep, to be sure that time of above and below operations is different
    When user1 changes space1/dir1 mode to 711 on client11
    Then status-change time of user2's space1/dir1 is greater than modification time on client21
    Then status-change time of user2's space1/dir1 is greater than access time on client21