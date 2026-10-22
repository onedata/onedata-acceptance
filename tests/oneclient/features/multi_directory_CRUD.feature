Feature: Multi_directory_CRUD

  Background:
    Given oneclients [client11, client21]
      mounted on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [user1, user2]

    
  Scenario: Create directory
    When user1 succeeds to create directories [space1/dir1, space1/dir2, space1/dir3] on client11

    Then user1 can see and can stat [dir1, dir2, dir3] in space1 on "client11"
    And user2 can see and can stat [dir1, dir2, dir3] in space1 on "client21"


  Scenario: Clean everything after creating directory and hidden directory
    When user1 succeeds to create directories [space1/dir1, space1/dir2, space1/dir3] on client11

    And user1 can see and can stat [dir1, dir2, dir3] in space1 on "client11"
    And user2 can see and can stat [dir1, dir2, dir3] in space1 on "client21"

    And user2 succeeds to create directories [space1/.dir4] on client21
    # waiting for synchronization and not listing directory is intentional
    # we want to purge spaces without listing or stating hidden directory
    And user1 is idle for 10 seconds
    And user1 purges all spaces on client11

    # TODO: VFS-13861 Changing order of 2 same steps only for different clients below changes result of this test, but shouldn't
    Then user1 doesn't see [dir1, dir2, dir3] in space1 on client11
    And user2 can't see and can't stat [dir1, dir2, dir3] in space1 on "client21"
    And user1 can't stat [dir1, dir2, dir3] in space1 on client11

    And user2 can't see and can't stat [.dir4] in space1 on "client21"
    And user1 can't see and can't stat [.dir4] in space1 on "client11"


  Scenario: Fail to rename someone's directory without write permission on parent
    When user1 creates directory and parents [space1/dir1/child1] on client11
    And user1 changes space1/dir1 mode to 755 on client11
    And mode of user2's space1/dir1 is 755 on client21
    And user2 fails to rename space1/dir1/child1 to space1/dir1/child2 on client21

    Then user1 can see and can stat [child1] in space1/dir1 on "client11"
    And user1 can't see and can't stat [child2] in space1/dir1 on "client11"

    And user2 can see and can stat [child1] in space1/dir1 on "client21"
    And user2 can't see and can't stat [child2] in space1/dir1 on "client21"


  Scenario: Rename someone's directory with permission
    When user1 creates directory and parents [space1/dir1/child1] on client11
    And mode of user2's space1/dir1/child1 is 775 on client21
    And user2 renames space1/dir1/child1 to space1/dir1/child2 on client21

    Then user1 can see and can stat [child2] in space1/dir1 on "client11"
    And user1 can't see and can't stat [child1] in space1/dir1 on "client11"
    And user2 can see and can stat [child2] in space1/dir1 on "client21"
    And user2 can't see and can't stat [child1] in space1/dir1 on "client21"


  Scenario: Rename own directory
    When user1 succeeds to create directories [space1/dir1] on client11
    And user1 renames space1/dir1 to space1/dir2 on client11

    Then user1 can see and can stat [dir2] in space1 on "client11"
    And user2 can see and can stat [dir2] in space1 on "client21"
    And user1 can't see and can't stat [dir1] in space1 on "client11"
    And user2 can't see and can't stat [dir1] in space1 on "client21"


  Scenario: Delete someone's empty directory
    When user2 succeeds to create directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 deletes directories (rmdir) [space1/dir1] on client11
    And user1 doesn't see [dir1] in space1 on client11
    And user2 doesn't see [dir1] in space1 on client21


  Scenario: Fail to delete someone's empty directory without write permission on parent
    When user2 creates directory and parents [space1/dir1/child1] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And user1 sees on "client11", that file tree rooted at "space1" contains following nodes:
        dir1:
          child1: present

    Then mode of user1's space1/dir1 is 755 on client11
    And user1 fails to delete directories (rmdir) [space1/dir1/child1] on client11
    And user1 can see and can stat [child1] in space1/dir1 on "client11"
    And user2 can see and can stat [child1] in space1/dir1 on "client21"


  Scenario: Delete own empty directory
    When user2 succeeds to create directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user2 deletes directories (rmdir) [space1/dir1] on client21

    Then user1 can't see and can't stat [dir1] in space1 on "client11"
    And user2 can't see and can't stat [dir1] in space1 on "client21"

  Scenario: Fail to list directory without read permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    Then user2 changes space1/dir1/dir2 mode to 735 on client21 and user1 sees that file can't be listed on client11


  Scenario: Fail to create file in directory without write permission
    When user2 succeeds to create directories [space1/dir1] on client21
    And user2 changes space1/dir1 mode to 755 on client21
    And mode of user1's space1/dir1 is 755 on client11

    Then user1 fails to create directories [space1/dir1/dir2] on client11


  Scenario: Delete directory right after deleting its subdirectory by other client
    When user2 succeeds to create directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 succeeds to create directories [space1/dir1/dir2] on client11

    Then user2 sees [dir2] in space1/dir1 on client21
    And user1 deletes directories (rm -rf) [space1/dir1/dir2] on client11
    And user1 can't see and can't stat [dir2] in space1/dir1 on "client11"
    And user2 can't see and can't stat [dir2] in space1/dir1 on "client21"


  Scenario: Create file in directory with write permission
    When user2 succeeds to create directories [space1/dir1] on client21
    And user1 sees [dir1] in space1 on client11
    And user1 succeeds to create directories [space1/dir1/dir2] on client11

    Then user2 can see and can stat [dir2] in space1/dir1 on "client21"
    And user1 can see and can stat [dir2] in space1/dir1 on "client11"


  Scenario: Fail to delete file in directory without write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user2 changes space1/dir1 mode to 755 on client21

    Then mode of user1's space1/dir1 is 755 on client11
    And user1 fails to delete directories (rmdir) [space1/dir1/dir2] on client11


  Scenario: Delete file in directory with write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user1 sees [dir2] in space1/dir1 on client11
    And user1 deletes directories (rmdir) [space1/dir1/dir2] on client11

    Then user2 can't see and can't stat [dir2] in space1/dir1 on "client21"


  Scenario: Fail to rename file in directory without write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user2 changes space1/dir1 mode to 755 on client21

    Then mode of user1's space1/dir1 is 755 on client11
    And user1 fails to rename space1/dir1/dir2 to space1/dir1/dir3 on client11


  Scenario: Rename file in directory with write permission
    When user2 creates directory and parents [space1/dir1/dir2] on client21
    And user1 renames space1/dir1/dir2 to space1/dir1/dir3 on client11

    Then user2 can see and can stat [dir3] in space1/dir1 on "client21"
    And user2 can't see and can't stat [dir2] in space1/dir1 on "client21"


  Scenario: Recreate directory deleted by other user
    When user1 succeeds to create directories [space1/dir1] on client11
    And user2 sees [dir1] in space1 on client21
    And user1 deletes directories (rmdir) [space1/dir1] on client11
    And user2 doesn't see [dir1] in space1 on client21
    And user2 succeeds to create directories [space1/dir1] on client21

    Then user2 can see and can stat [dir1] in space1 on "client21"
    And user1 can see and can stat [dir1] in space1 on "client11"


  Scenario: Create child directories
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir1/child3] on client11

    Then user1 can see and can stat [child1, child2, child3] in space1/dir1 on "client11"
    And user2 can see and can stat [child1, child2, child3] in space1/dir1 on "client21"


  Scenario: Create child directories 2
    When user2 creates directory and parents [space1/dir1/dir2/dir3/child1, space1/dir1/dir2/child1, space1/dir1/child1] on client21

    Then user1 can see and can stat [dir2, child1] in space1/dir1 on "client11"
    And user2 can see and can stat [dir2, child1] in space1/dir1 on "client21"

    And user1 can see and can stat [dir3, child1] in space1/dir1/dir2 on "client11"
    And user2 can see and can stat [dir3, child1] in space1/dir1/dir2 on "client21"

    And user1 can see and can stat [child1] in space1/dir1/dir2/dir3 on "client11"
    And user2 can see and can stat [child1] in space1/dir1/dir2/dir3 on "client21"


  Scenario: Fail to create a duplicate directory
    When user1 succeeds to create directories [space1/dir1] on client11
    And user2 sees [dir1] in space1 on client21

    Then user2 fails to create directories [space1/dir1] on client21


  Scenario: Delete empty directory and parents
    When user1 creates directory and parents [space1/dir1/dir2/dir3] on client11
    And [user1, user2] see on [client11, client21], that file tree rooted at "space1" contains following nodes:
        dir1:
          dir2:
            dir3: present

    And user2 deletes directory (rmdir -p) [space1/dir1/dir2/dir3] on client21

    Then user1 can't see and can't stat [dir1] in space1 on "client11"
    And user2 can't see and can't stat [dir1] in space1 on "client21"


  Scenario: Fail to delete non-empty directory using rmdir
    When user2 succeeds to create directories [space1/dir1, space1/dir1/child1] on client21
    And user1 sees on "client11", that file tree rooted at "space1" contains following nodes:
        dir1:
          child1: present

    And user2 sees on "client21", that file tree rooted at "space1" contains following nodes:
        dir1:
          child1: present

    Then user1 fails to delete directories (rmdir) [space1/dir1] on client11

    And user1 can see and can stat [dir1] in space1 on "client11"
    And user2 can see and can stat [dir1] in space1 on "client21"

    And user1 can see and can stat [child1] in space1/dir1 on "client11"
    And user2 can see and can stat [child1] in space1/dir1 on "client21"


  Scenario: Delete non-empty directory
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir2/dir3/child1] on client11

    And [user1, user2] sees on [client11, client21], that file tree rooted at "space1" contains following nodes:
        dir1:
          child1: present
          child2: present
        dir2:
          dir3:
            child1: present

    And user1 deletes directories (rm -rf) [space1/dir1, space1/dir2] on client11

    Then user1 can't see and can't stat [dir1, dir2] in space1 on "client11"
    And user2 can't see and can't stat [dir1, dir2] in space1 on "client21"


  Scenario: Move directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5] on client11
    
    And [user1, user2] sees on [client11, client21], that file tree rooted at "space1" contains following nodes:
        dir1:
          dir2:
            dir3: present
        dir4:
          dir5: present

    And user1 renames space1/dir4/dir5 to space1/dir1/dir2/dir3 on client11
    #    Uncomment after resolving VFS-4378
    #    Then user1 can't stat [dir5] in space1/dir4 on client11
    #    And user2 can't stat [dir5] in space1/dir4 on client21

    Then user1 can see and can stat [dir5] in space1/dir1/dir2/dir3 on "client11"
    And user2 can see and can stat [dir5] in space1/dir1/dir2/dir3 on "client21"

    And user1 doesn't see [dir5] in space1/dir4 on client11
    And user2 doesn't see [dir5] in space1/dir4 on client21


  Scenario: Copy directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5] on client11

    And [user1, user2] see on [client11, client21], that file tree rooted at "space1" contains following nodes:
        dir1:
          dir2:
            dir3: present
        dir4:
          dir5: present

    And user1 copies directory space1/dir4 to space1/dir1/dir2/dir3 on client11

    Then user1 can see and can stat [dir4] in space1/dir1/dir2/dir3 on "client11"
    And user2 can see and can stat [dir4] in space1/dir1/dir2/dir3 on "client21"

    And user1 can see and can stat [dir5] in space1/dir1/dir2/dir3/dir4 on "client11"
    And user2 can see and can stat [dir5] in space1/dir1/dir2/dir3/dir4 on "client21"

    And user1 can see and can stat [dir5] in space1/dir4 on "client11"
    And user2 can see and can stat [dir5] in space1/dir4 on "client21"


  Scenario: Fail to move directory to itself
    When user1 succeeds to create directories [space1/dir1] on client11

    And user1 sees [dir1] in space1 on client11
    And user2 sees [dir1] in space1 on client21

    Then user1 fails to move space1/dir1 to space1/dir1 using shell command on client11

    And user1 can see and can stat [dir1] in space1 on "client11"
    And user2 can see and can stat [dir1] in space1 on "client21"


  Scenario: Fail to move directory to its subtree
    When user1 creates directory and parents [space1/dir1/dir2/dir3] on client11

    And [user1, user2] see on [client11, client21], that file tree rooted at "space1" contains following nodes:
        dir1:
          dir2:
            dir3: present

    Then user1 fails to rename space1/dir1 to space1/dir1/dir2/dir3 on client11

    And user1 can see and can stat [dir1] in space1 on "client11"
    And user2 can see and can stat [dir1] in space1 on "client21"

    And user1 can see and can stat [dir2] in space1/dir1 on "client11"
    And user2 can see and can stat [dir2] in space1/dir1 on "client21"

    And user1 can see and can stat [dir3] in space1/dir1/dir2 on "client11"
    And user2 can see and can stat [dir3] in space1/dir1/dir2 on "client21"
