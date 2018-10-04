Feature: Multi_directory_CRUD

  Background:
    Given [user1, user2] mount oneclients [client11, client21] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [token, token]

    
  Scenario: Create directory
    When user1 creates directories [space1/dir1, space1/dir2, space1/dir3]
      on client11
    Then user1 can stat [dir1, dir2, dir3] in space1 on client11
    And user2 can stat [dir1, dir2, dir3] in space1 on client21
    Then user1 sees [dir1, dir2, dir3] in space1 on client11
    And user2 sees [dir1, dir2, dir3] in space1 on client21


  Scenario: Fail to rename someone's directory without write permission on parent
    When user1 creates directory and parents [space1/dir1/child1] on client11
    And user1 changes space1/dir1 mode to 755 on client11
    And mode of user2's space1/dir1 is 755 on client21
    And user2 fails to rename space1/dir1/child1 to space1/dir1/child2 on client21
    Then user1 can stat [child1] in space1/dir1 on client11
    And user1 can't stat [child2] in space1/dir1 on client11
    And user2 can stat [child1] in space1/dir1 on client21
    And user2 can't stat [child2] in space1/dir1 on client21
    Then user1 sees [child1] in space1/dir1 on client11
    And user1 doesn't see [child2] in space1/dir1 on client11
    And user2 sees [child1] in space1/dir1 on client21
    And user2 doesn't see [child2] in space1/dir1 on client21


  Scenario: Rename someone's directory with permission
    When user1 creates directory and parents [space1/dir1/child1] on client11
    And mode of user2's space1/dir1/child1 is 775 on client21
    And user2 renames space1/dir1/child1 to space1/dir1/child2 on client21
    Then user1 can stat [child2] in space1/dir1 on client11
    And user1 can't stat [child1] in space1/dir1 on client11
    And user2 can stat [child2] in space1/dir1 on client21
    And user2 can't stat [child1] in space1/dir1 on client21
    Then user1 sees [child2] in space1/dir1 on client11
    And user1 doesn't see [child1] in space1/dir1 on client11
    And user2 sees [child2] in space1/dir1 on client21
    And user2 doesn't see [child1] in space1/dir1 on client21


  Scenario: Rename own directory
    When user1 creates directories [space1/dir1] on client11
    And user1 renames space1/dir1 to space1/dir2 on client11
    Then user1 can stat [dir2] in space1 on client11
    And user2 can stat [dir2] in space1 on client21
    And user1 can't stat [dir1] in space1 on client11
    And user2 can't stat [dir1] in space1 on client21
    Then user1 sees [dir2] in space1 on client11
    And user2 sees [dir2] in space1 on client21
    And user1 doesn't see [dir1] in space1 on client11
    And user2 doesn't see [dir1] in space1 on client21


  Scenario: Delete someone's empty directory
    When user2 creates directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 deletes empty directories [space1/dir1] on client11
    And user1 doesn't see [dir1] in space1 on client11
    And user2 doesn't see [dir1] in space1 on client21


  Scenario: Fail to delete someone's empty directory without write permission on parent
    When user2 creates directory and parents [space1/dir1/child1] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And user1 sees [dir1] in space1 on client11
    And user1 sees [child1] in space1/dir1 on client11
    And mode of user1's space1/dir1 is 755 on client11
    And user1 fails to delete empty directories [space1/dir1/child1] on client11
    And user1 can stat [child1] in space1/dir1 on client11
    And user2 can stat [child1] in space1/dir1 on client21
    And user1 sees [child1] in space1/dir1 on client11
    And user2 sees [child1] in space1/dir1 on client21


  Scenario: Delete own empty directory
    When user2 creates directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user2 deletes empty directories [space1/dir1] on client21
    Then user1 can't stat [dir1] in space1 on client11
    And user2 can't stat [dir1] in space1 on client21
    Then user1 doesn't see [dir1] in space1 on client11
    And user2 doesn't see [dir1] in space1 on client21

  Scenario: List directory without read permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user2 changes space1/dir1/dir2 mode to 735 on client21
    And user1 can't list space1/dir1/dir2 on client11


  Scenario: Fail to create file in directory without write permission
    When user2 creates directories [space1/dir1] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And mode of user1's space1/dir1 is 755 on client11
    And user1 fails to create directories [space1/dir1/dir2] on client11


  Scenario: Delete directory right after deleting its subdirectory by other client
    When user2 creates directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 creates directories [space1/dir1/dir2] on client11
    Then user2 sees [dir2] in space1/dir1 on client21
    Then user1 deletes non-empty directories [space1/dir1/dir2] on client11
    Then user1 can't stat [dir2] in space1/dir1 on client11
    Then user2 can't stat [dir2] in space1/dir1 on client21
    Then user1 doesn't see [dir2] in space1/dir1 on client11
    Then user2 doesn't see [dir2] in space1/dir1 on client21


  Scenario: Create file in directory with write permission
    When user2 creates directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 creates directories [space1/dir1/dir2] on client11
    Then user2 can stat [dir2] in space1/dir1 on client21
    And user1 can stat [dir2] in space1/dir1 on client11
    Then user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir2] in space1/dir1 on client11


  Scenario: Fail to delete file in directory without write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And mode of user1's space1/dir1 is 755 on client11
    And user1 fails to delete empty directories [space1/dir1/dir2] on client11


  Scenario: Delete file in directory with write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user1 deletes empty directories [space1/dir1/dir2] on client11
    Then user2 can't stat [dir2] in space1/dir1 on client21
    Then user2 doesn't see [dir2] in space1/dir1 on client21


  Scenario: Fail to rename file in directory without write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And mode of user1's space1/dir1 is 755 on client11
    And user1 fails to rename space1/dir1/dir2 to space1/dir1/dir3 on client11


  Scenario: Rename file in directory with write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user1 renames space1/dir1/dir2 to space1/dir1/dir3 on client11
    Then user2 can stat [dir3] in space1/dir1 on client21
    And user2 can't stat [dir2] in space1/dir1 on client21
    Then user2 sees [dir3] in space1/dir1 on client21
    And user2 doesn't see [dir2] in space1/dir1 on client21


  Scenario: Recreate directory deleted by other user
    When user1 creates directories [space1/dir1] on client11
    And user2 sees [dir1] in space1 on client21
    And user1 deletes empty directories [space1/dir1] on client11
    And user2 doesn't see [dir1] in space1 on client21
    And user2 creates directories [space1/dir1] on client21
    Then user2 can stat [dir1] in space1 on client21
    And user1 can stat [dir1] in space1 on client11
    Then user2 sees [dir1] in space1 on client21
    And user1 sees [dir1] in space1 on client11


  Scenario: Child directories
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir1/child3]
      on client11
    Then user1 can stat [child1, child2, child3] in space1/dir1 on client11
    And user2 can stat [child1, child2, child3] in space1/dir1 on client21
    Then user1 sees [child1, child2, child3] in space1/dir1 on client11
    And user2 sees [child1, child2, child3] in space1/dir1 on client21


  Scenario: Child directories 2
    When user2 creates directory and parents [space1/dir1/dir2/dir3/child1, space1/dir1/dir2/child1, space1/dir1/child1]
      on client21
    Then user1 can stat [dir2, child1] in space1/dir1 on client11
    And user2 can stat [dir2, child1] in space1/dir1 on client21
    And user1 can stat [dir3, child1] in space1/dir1/dir2 on client11
    And user2 can stat [dir3, child1] in space1/dir1/dir2 on client21
    And user1 can stat [child1] in space1/dir1/dir2/dir3 on client11
    And user2 can stat [child1] in space1/dir1/dir2/dir3 on client21
    Then user1 sees [dir2, child1] in space1/dir1 on client11
    And user2 sees [dir2, child1] in space1/dir1 on client21
    And user1 sees [dir3, child1] in space1/dir1/dir2 on client11
    And user2 sees [dir3, child1] in space1/dir1/dir2 on client21
    And user1 sees [child1] in space1/dir1/dir2/dir3 on client11
    And user2 sees [child1] in space1/dir1/dir2/dir3 on client21


  Scenario: Duplication
    When user1 creates directories [space1/dir1] on client11
    And user2 sees [dir1] in space1 on client21
    And user2 fails to create directories [space1/dir1] on client21


  Scenario: Delete empty directory and parents
    # rmdir -p dir1/dir2/dir3
    When user1 creates directory and parents [space1/dir1/dir2/dir3] on client11
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1/dir1/dir2 on client21
    And user2 deletes empty directory and parents [space1/dir1/dir2/dir3] on client21
    And user1 can't stat [dir1] in space1 on client11
    And user2 can't stat [dir1] in space1 on client21
    And user1 doesn't see [dir1] in space1 on client11
    And user2 doesn't see [dir1] in space1 on client21


  Scenario: Delete non-empty directory in wrong way
    # wrong way means using rmdir instead of rm -rf
    When user2 creates directories [space1/dir1, space1/dir1/child1] on client21
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 sees [child1] in space1/dir1 on client11
    And user2 sees [child1] in space1/dir1 on client21

    # dir1 is not empty, but we use step for empty dirs
    And user1 fails to delete empty directories [space1/dir1] on client11
    And user1 can stat [dir1] in space1 on client11
    And user2 can stat [dir1] in space1 on client21
    And user1 can stat [child1] in space1/dir1 on client11
    And user2 can stat [child1] in space1/dir1 on client21
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 sees [child1] in space1/dir1 on client11
    And user2 sees [child1] in space1/dir1 on client21


  Scenario: Delete non-empty directory
    # rm -rf dir1 dir2
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir2/dir3/child1]
      on client11
    And user1 sees [dir1, dir2] in space1 on client11
    And user2 sees [dir1, dir2] in space1 on client21
    And user1 sees [child1, child2] in space1/dir1 on client11
    And user2 sees [child1, child2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir2 on client11
    And user2 sees [dir3] in space1/dir2 on client21
    And user1 sees [child1] in space1/dir2/dir3 on client11
    And user2 sees [child1] in space1/dir2/dir3 on client21
    And user1 deletes non-empty directories [space1/dir1, space1/dir2] on client11
    Then user1 can't stat [dir1, dir2] in space1 on client11
    Then user2 can't stat [dir1, dir2] in space1 on client21
    Then user1 doesn't see [dir1, dir2] in space1 on client11
    Then user2 doesn't see [dir1, dir2] in space1 on client21


  Scenario: Move directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5] on client11
    And user1 sees [dir1, dir4] in space1 on client11
    And user2 sees [dir1, dir4] in space1 on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1/dir1/dir2 on client21
    And user1 sees [dir5] in space1/dir4 on client11
    And user2 sees [dir5] in space1/dir4 on client21
    And user1 renames space1/dir4/dir5 to space1/dir1/dir2/dir3 on client11
    #    Uncomment after resolving VFS-4378
    #    Then user1 can't stat [dir5] in space1/dir4 on client11
    #    And user2 can't stat [dir5] in space1/dir4 on client21
    Then user1 can stat [dir5] in space1/dir1/dir2/dir3 on client11
    And user2 can stat [dir5] in space1/dir1/dir2/dir3 on client21
    And user1 doesn't see [dir5] in space1/dir4 on client11
    And user2 doesn't see [dir5] in space1/dir4 on client21
    And user1 sees [dir5] in space1/dir1/dir2/dir3 on client11
    And user2 sees [dir5] in space1/dir1/dir2/dir3 on client21


  Scenario: Copy directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5] on client11
    And user1 sees [dir1, dir4] in space1 on client11
    And user2 sees [dir1, dir4] in space1 on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1/dir1/dir2 on client21
    And user1 sees [dir5] in space1/dir4 on client11
    And user2 sees [dir5] in space1/dir4 on client21
    And user1 copies directory space1/dir4 to space1/dir1/dir2/dir3 on client11
    Then user1 can stat [dir4] in space1/dir1/dir2/dir3 on client11
    And user2 can stat [dir4] in space1/dir1/dir2/dir3 on client21
    And user1 can stat [dir5] in space1/dir1/dir2/dir3/dir4 on client11
    And user2 can stat [dir5] in space1/dir1/dir2/dir3/dir4 on client21
    And user1 can stat [dir5] in space1/dir4 on client11
    And user2 can stat [dir5] in space1/dir4 on client21
    Then user1 sees [dir4] in space1/dir1/dir2/dir3 on client11
    And user2 sees [dir4] in space1/dir1/dir2/dir3 on client21
    And user1 sees [dir5] in space1/dir1/dir2/dir3/dir4 on client11
    And user2 sees [dir5] in space1/dir1/dir2/dir3/dir4 on client21
    And user1 sees [dir5] in space1/dir4 on client11
    And user2 sees [dir5] in space1/dir4 on client21


  Scenario: Move directory to itself
    When user1 creates directories [space1/dir1] on client11
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 fails to move space1/dir1 to space1/dir1 using shell command on client11
    And user1 can stat [dir1] in space1 on client11
    And user2 can stat [dir1] in space1 on client21
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21


  Scenario: Move directory to its subtree
    When user1 creates directory and parents [space1/dir1/dir2/dir3] on client11
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1/dir1/dir2 on client21
    And user1 fails to rename space1/dir1 to space1/dir1/dir2/dir3 on client11
    And user1 can stat [dir1] in space1 on client11
    And user2 can stat [dir1] in space1 on client21
    And user1 can stat [dir2] in space1/dir1 on client11
    And user2 can stat [dir2] in space1/dir1 on client21
    And user1 can stat [dir3] in space1/dir1/dir2 on client11
    And user2 can stat [dir3] in space1/dir1/dir2 on client21
    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user2 sees [dir2] in space1/dir1 on client21
    And user1 sees [dir3] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1/dir1/dir2 on client21
