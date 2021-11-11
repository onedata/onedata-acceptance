Feature: Regular_file_CRUD

  Background:
    Given oneclient mounted using token by user1

    
  Scenario: Create regular file
    When user1 creates regular files [space1/file1, space1/file2, space1/file3]
    Then user1 can stat [file1, file2, file3] in space1
    Then user1 sees [file1, file2, file3] in space1

    
  Scenario: Create many children
    When user1 creates child files of space1 with names in range [1, 127)
    Then user1 lists children of space1 and gets names in range [1, 127)


  Scenario: Rename regular file
    When user1 creates regular files [space1/file1]
    And user1 sees [file1] in space1
    And user1 renames space1/file1 to space1/file2
    Then user1 can stat [file2] in space1
    And user1 can't stat [file1] in space1
    Then user1 sees [file2] in space1
    And user1 doesn't see [file1] in space1

    
  Scenario: Delete regular file
    When user1 creates regular files [space1/file1]
    And user1 sees [file1] in space1
    And user1 deletes files [space1/file1]
    Then user1 can't stat [file1] in space1
    Then user1 doesn't see [file1] in space1

    
    Scenario: Read and write to regular file
    When user1 creates regular files [space1/file1]
    And user1 writes "TEST TEXT ONEDATA" to space1/file1
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1
    And size of user1's space1/file1 is 17 bytes

    
  Scenario: Append to regular file
    When user1 creates regular files [space1/file1]
    And user1 writes "TEST TEXT ONEDATA" to space1/file1
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1
    And user1 appends " APPENDED TEXT" to space1/file1
    Then user1 reads "TEST TEXT ONEDATA APPENDED TEXT" from file space1/file1
    And size of user1's space1/file1 is 31 bytes

    
  Scenario: Replace word in file
    When user1 creates regular files [space1/file1]
    And user1 writes "TEST ONEDATA TEST ONEDATA2 TEST ONEDATA3" to space1/file1
    And user1 replaces "TEST" with "SYSTEM" in space1/file1
    Then user1 reads "SYSTEM ONEDATA SYSTEM ONEDATA2 SYSTEM ONEDATA3" from file space1/file1
    And size of user1's space1/file1 is 46 bytes

    
  Scenario: Move regular file and read
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/dir2/file1
    And user1 renames space1/dir1/dir2/file1 to space1/dir3/file1
    Then user1 can't stat [file1] in space1/dir1/dir2
    And user1 can stat [file1] in space1/dir3
    Then user1 doesn't see [file1] in space1/dir1/dir2
    And user1 sees [file1] in space1/dir3
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir3/file1
    And size of user1's space1/dir3/file1 is 17 bytes

    
  Scenario: Move big regular file and check MD5
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes 32 MB of random characters to space1/dir1/dir2/file1 and saves MD5
    And user1 renames space1/dir1/dir2/file1 to space1/dir3/file1
    Then user1 can't stat [file1] in space1/dir1/dir2
    And user1 can stat [file1] in space1/dir3
    Then user1 doesn't see [file1] in space1/dir1/dir2
    And user1 sees [file1] in space1/dir3
    Then user1 checks MD5 of space1/dir3/file1

    
  Scenario: Copy regular file and read
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/dir2/file1
    And user1 copies regular file space1/dir1/dir2/file1 to space1/dir3
    Then user1 can stat [dir1, dir3] in space1
    And user1 can stat [file1] in space1/dir1/dir2
    And user1 can stat [file1] in space1/dir3
    Then user1 sees [dir1, dir3] in space1
    And user1 sees [file1] in space1/dir1/dir2
    And user1 sees [file1] in space1/dir3
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir3/file1
    And size of user1's space1/dir3/file1 is 17 bytes

    
  Scenario: Copy big regular file and check MD5
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes 32 MB of random characters to space1/dir1/dir2/file1 and saves MD5
    And user1 copies regular file space1/dir1/dir2/file1 to space1/dir3/file1
    Then user1 sees [file1] in space1/dir1/dir2
    And user1 sees [file1] in space1/dir3
    And user1 checks MD5 of space1/dir1/dir2/file1
    And user1 checks MD5 of space1/dir3/file1

    
  Scenario: Delete file copied right after read
    When user1 creates directory and parents [space1/dir1/dir2]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/dir2/file1
    And user1 deletes files [space1/dir1/dir2/file1]
    Then user1 doesn't see [file1] in space1/dir1/dir2

    
  Scenario: Restart provider with active oneclient connection
    When user1 creates directory and parents [space1/dir1/dir2]
    And user1 creates regular files [space1/dir1/dir2/file1]
    And user1 sees [file1] in space1/dir1/dir2
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1
    And user1 restarts oneprovider oneprovider-krakow
    Then user1 reads "TEST TEXT ONEDATA" from file space1/dir1/dir2/file1
