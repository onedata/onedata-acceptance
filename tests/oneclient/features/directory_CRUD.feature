Feature: Directory_CRUD

  Background:
    Given oneclient mounted in /home/user1/onedata using token by user1


  Scenario: Create directory
    When user1 creates directories [space1/dir1, space1/dir2, space1/dir3]
    Then user1 can stat [dir1, dir2, dir3] in space1
    And user1 sees [dir1, dir2, dir3] in space1


  Scenario: Create directory in spaces directory
    Then user1 fails to create directories [dir]


  Scenario: Create space
    Then user1 fails to create directories [space1]


  Scenario: Rename directory
    When user1 creates directories [space1/dir1]
    And user1 renames space1/dir1 to space1/dir2
    Then user1 can stat [dir2] in space1
    And user1 can't stat [dir1] in space1
    And user1 sees [dir2] in space1
    And user1 doesn't see [dir1] in space1


  Scenario: Delete empty directory
    When user1 creates directories [space1/dir1]
    Then user1 can stat [dir1] in space1
    And user1 sees [dir1] in space1
    And user1 deletes directories (rmdir) [space1/dir1]
    And user1 can't stat [dir1] in space1
    And user1 doesn't see [dir1] in space1


  Scenario: Fail to delete space
    When user1 deletes directories (rm -rf) [space1]
    # space directory cannot be deleted
    Then user1 can list space1


  Scenario: Create child directories
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir1/child3]
    Then user1 can stat [child1, child2, child3] in space1/dir1
    Then user1 sees [child1, child2, child3] in space1/dir1


  Scenario: Create child directories 2
    When user1 creates directory and parents [space1/dir1/dir2/dir3/child1, space1/dir1/dir2/child1, space1/dir1/child1]
    Then user1 can stat [dir2, child1] in space1/dir1
    And user1 can stat [dir3, child1] in space1/dir1/dir2
    And user1 can stat [child1] in space1/dir1/dir2/dir3
    Then user1 sees [dir2, child1] in space1/dir1
    And user1 sees [dir3, child1] in space1/dir1/dir2
    And user1 sees [child1] in space1/dir1/dir2/dir3


  Scenario: Fail to create a duplicate directory
    When user1 creates directories [space1/dir1]
    Then user1 fails to create directories [space1/dir1]


  Scenario: Delete empty directory and parents
    When user1 creates directory and parents [space1/dir1/dir2/dir3]
    And user1 sees [dir1] in space1
    And user1 sees [dir2] in space1/dir1
    And user1 sees [dir3] in space1/dir1/dir2
    And user1 deletes directory (rmdir -p) [space1/dir1/dir2/dir3]
    Then user1 can't stat [dir1] in space1
    Then user1 doesn't see [dir1] in space1


  Scenario: Fail to delete non-empty directory using rmdir
    When user1 creates directories [space1/dir1, space1/dir1/child1]
    And user1 sees [dir1] in space1
    And user1 sees [child1] in space1/dir1
    Then user1 fails to delete directories (rmdir) [space1/dir1]
    And user1 can stat [dir1] in space1
    And user1 can stat [child1] in space1/dir1
    And user1 sees [dir1] in space1
    And user1 sees [child1] in space1/dir1


  Scenario: Delete non-empty directory
    When user1 creates directory and parents [space1/dir1/child1, space1/dir1/child2, space1/dir2/dir3/child1]
    And user1 sees [dir1, dir2] in space1
    And user1 sees [child1, child2] in space1/dir1
    And user1 sees [dir3] in space1/dir2
    And user1 sees [child1] in space1/dir2/dir3
    And user1 deletes directories (rm -rf) [space1/dir1, space1/dir2]
    Then user1 can't stat [dir1, dir2] in space1
    Then user1 doesn't see [dir1, dir2] in space1


  Scenario: Move directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5]
    And user1 sees [dir1, dir4] in space1
    And user1 sees [dir2] in space1/dir1
    And user1 sees [dir3] in space1/dir1/dir2
    And user1 sees [dir5] in space1/dir4
    And user1 renames space1/dir4/dir5 to space1/dir1/dir2/dir3
    Then user1 can't stat [dir5] in space1/dir4
    Then user1 doesn't see [dir5] in space1/dir4
    And user1 can stat [dir1, dir4] in space1
    And user1 can stat [dir5] in space1/dir1/dir2/dir3
    And user1 sees [dir1, dir4] in space1
    And user1 sees [dir5] in space1/dir1/dir2/dir3


  Scenario: Copy directory
    When user1 creates directory and parents [space1/dir1/dir2/dir3, space1/dir4/dir5]
    And user1 sees [dir1, dir4] in space1
    And user1 sees [dir2] in space1/dir1
    And user1 sees [dir3] in space1/dir1/dir2
    And user1 sees [dir5] in space1/dir4
    And user1 copies directory space1/dir4 to space1/dir1/dir2/dir3
    Then user1 can stat [dir5] in space1/dir4
    And user1 can stat [dir5] in space1/dir1/dir2/dir3/dir4
    Then user1 sees [dir5] in space1/dir4
    And user1 sees [dir5] in space1/dir1/dir2/dir3/dir4


  Scenario: Fail to move directory to itself
    When user1 creates directories [space1/dir1]
    And user1 sees [dir1] in space1
    Then user1 fails to move space1/dir1 to space1/dir1 using shell command
    And user1 can stat [dir1] in space1
    And user1 sees [dir1] in space1


  Scenario: Fail to move directory to its subtree
    When user1 creates directory and parents [space1/dir1/dir2/dir3]
    And user1 sees [dir1] in space1
    And user1 sees [dir2] in space1/dir1
    And user1 sees [dir3] in space1/dir1/dir2
    And user1 fails to rename space1/dir1 to space1/dir1/dir2/dir3
    And user1 can stat [dir1] in space1
    And user1 sees [dir1] in space1
    And user1 can't stat [dir1] in space1/dir1/dir2/dir3
    And user1 doesn't see [dir1] in space1/dir1/dir2/dir3

