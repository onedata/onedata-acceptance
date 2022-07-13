Feature: Multi_regular_file_CRUD

  Background:
    Given oneclients [client11, client21]
      mounted on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [user1, user2]


  Scenario: Create regular file
    When user1 creates regular files [space1/file1, space1/file2, space1/file3] on client11
    Then user1 can stat [file1, file2, file3] in space1 on client11
    And user2 can stat [file1, file2, file3] in space1 on client21
    Then user1 sees [file1, file2, file3] in space1 on client11
    And user2 sees [file1, file2, file3] in space1 on client21


  Scenario: Create many children
    When user1 creates child files of space1 with names in range [1, 127) on client11
    Then user2 lists children of space1 and gets names in range [1, 127) on client21


  Scenario: Create a file, read it on the second client, delete it, and repeat the whole process
    When user1 creates regular files [space1/file1] on client11
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/file1 on client21
    And user1 deletes files [space1/file1] on client11
    Then user1 creates regular files [space1/file1] on client11
    And user2 reads "" from file space1/file1 on client21
    And user1 writes "DIFFERENT TEST TEXT ONEDATA" to space1/file1 on client11
    And user2 reads "DIFFERENT TEST TEXT ONEDATA" from file space1/file1 on client21


  Scenario: Fail to rename regular file without write permission on parent
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 changes space1/dir1 mode to 755 on client11
    And mode of user2's space1/dir1 is 755 on client21
    And user2 fails to rename space1/dir1/file1 to space1/dir1/file2 on client21
    Then user1 sees [file1] in space1/dir1 on client11
    And user1 doesn't see [file2] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user2 doesn't see [file2] in space1/dir1 on client21


  Scenario: Rename regular file with write permission on parent
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user2 renames space1/dir1/file1 to space1/dir1/file2 on client21
    Then user1 can stat [file2] in space1/dir1 on client11
    And user1 can stat [file2] in space1/dir1 on client11
    And user2 can stat [file2] in space1/dir1 on client21
    And user1 can't stat [file1] in space1/dir1 on client11
    And user2 can't stat [file1] in space1/dir1 on client21
    Then user1 sees [file2] in space1/dir1 on client11
    And user1 sees [file2] in space1/dir1 on client11
    And user2 sees [file2] in space1/dir1 on client21
    And user1 doesn't see [file1] in space1/dir1 on client11
    And user2 doesn't see [file1] in space1/dir1 on client21


  Scenario: Delete regular file by owner
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 deletes files [space1/file1] on client11
    Then user1 can't stat [file1] in space1 on client11
    And user2 can't stat [file1] in space1 on client21
    Then user1 doesn't see [file1] in space1 on client11
    And user2 doesn't see [file1] in space1 on client21


  Scenario: Delete regular file by other user with write permission on parent
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user2 deletes files [space1/file1] on client21
    Then user1 can't stat [file1] in space1 on client11
    And user2 can't stat [file1] in space1 on client21
    Then user1 doesn't see [file1] in space1 on client11
    And user2 doesn't see [file1] in space1 on client21


  Scenario: Fail to delete regular file by other user without write permission on parent
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 changes space1/dir1 mode to 755 on client11
    And mode of user2's space1/dir1 is 755 on client21
    And user2 fails to delete files [space1/dir1/file1] on client21
    Then user1 can stat [file1] in space1/dir1 on client11
    And user2 can stat [file1] in space1/dir1 on client21
    Then user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21


  Scenario: Read and write to regular file
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/file1 on client21
    And size of user1's space1/file1 is 17 bytes on client11
    And size of user2's space1/file1 is 17 bytes on client21


  Scenario: Read right after write by other client
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/file1 on client21
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1 on client11
    And size of user1's space1/file1 is 17 bytes on client11
    And size of user2's space1/file1 is 17 bytes on client21


  Scenario: Read right after write by other client while file is open
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 opens space1/file1 with mode r+ on client11
    And user1 writes "TEST TEXT ONEDATA" to previously opened space1/file1 on client11
    And user2 opens space1/file1 with mode r+ on client21
    And user2 reads "TEST TEXT ONEDATA" from previously opened file space1/file1 on client21
    And user2 writes "NEW LINE" to previously opened space1/file1 on client21
    Then user1 reads "NEW LINET ONEDATA" from previously opened file space1/file1 on client11


  Scenario: Fail to read regular file without read permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/file1 on client11
    Then user2 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client21
    And user1 changes space1/dir1/file1 mode to 620 on client11
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client11
    And mode of user2's space1/dir1/file1 is 620 on client21
    And user2 cannot read from space1/dir1/file1 on client21
    And size of user1's space1/dir1/file1 is 17 bytes on client11


  Scenario: Write to regular file with write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 changes space1/dir1/file1 mode to 660 on client11
    And mode of user2's space1/dir1/file1 is 660 on client21
    And user2 writes "TEST TEXT ONEDATA" to space1/dir1/file1 on client21
    Then user2 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client21
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client11
    And size of user1's space1/dir1/file1 is 17 bytes on client11
    And size of user2's space1/dir1/file1 is 17 bytes on client21


  Scenario: Fail to write to regular file without write permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 changes space1/dir1/file1 mode to 600 on client11
    Then mode of user2's space1/dir1/file1 is 600 on client21
    And user2 fails to write "TEST TEXT ONEDATA" to space1/dir1/file1 on client21
    And user1 sees [file1] in space1/dir1 on client11
    And user1 reads "" from file space1/dir1/file1 on client11


  Scenario: Execute file with execute permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/script.sh] on client11
    And user1 changes space1/dir1/script.sh mode to 654 on client11
    And mode of user2's space1/dir1/script.sh is 654 on client21
    And user1 writes "#!/usr/bin/env bash\n\necho TEST" to space1/dir1/script.sh on client11
    And user2 reads "#!/usr/bin/env bash\n\necho TEST" from file space1/dir1/script.sh on client21
    And user2 executes space1/dir1/script.sh on client21


  Scenario: Fail to execute file without execute permission
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/script.sh] on client11
    And user2 sees [script.sh] in space1/dir1 on client21
    And user1 writes "#!/usr/bin/env bash\n\necho TEST" to space1/dir1/script.sh on client11
    And user2 reads "#!/usr/bin/env bash\n\necho TEST" from file space1/dir1/script.sh on client21
    And user2 fails to execute space1/dir1/script.sh on client21


  Scenario: Move regular file and read
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3] on client11
    And user1 creates regular files [space1/dir1/dir2/file1] on client11
    And user1 sees [dir3] in space1 on client11
    And user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [dir3] in space1 on client21
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1 on client11
    And user1 renames space1/dir1/dir2/file1 to space1/dir3/file1 on client11
    Then user1 can't stat [file1] in space1/dir1/dir2 on client11
    And user2 can't stat [file1] in space1/dir1/dir2 on client21
    Then user1 can stat [file1] in space1/dir3 on client11
    And user2 can stat [file1] in space1/dir3 on client21
    And user1 doesn't see [file1] in space1/dir1/dir2 on client11
    And user2 doesn't see [file1] in space1/dir1/dir2 on client21
    And user1 sees [file1] in space1/dir3 on client11
    And user2 sees [file1] in space1/dir3 on client21
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir3/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/dir3/file1 on client21


  Scenario: Move big regular file and check MD5
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3] on client11
    And user1 creates regular files [space1/dir1/dir2/file1] on client11
    And user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 writes 32 MB of random characters to space1/dir1/dir2/file1 on client11 and saves MD5
    And user1 renames space1/dir1/dir2/file1 to space1/dir3/file1 on client11
    Then user1 can't stat [file1] in space1/dir1/dir2 on client11
    And user2 can't stat [file1] in space1/dir1/dir2 on client21
    Then user1 can stat [file1] in space1/dir3 on client11
    And user2 can stat [file1] in space1/dir3 on client21
    And user1 doesn't see [file1] in space1/dir1/dir2 on client11
    And user2 doesn't see [file1] in space1/dir1/dir2 on client21
    And user1 sees [file1] in space1/dir3 on client11
    And user2 sees [file1] in space1/dir3 on client21
    And user1 checks MD5 of space1/dir3/file1 on client11
    And user2 checks MD5 of space1/dir3/file1 on client21


  Scenario: Copy regular file and read
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3] on client11
    And user1 creates regular files [space1/dir1/dir2/file1] on client11
    And user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/dir2/file1 on client11
    When user1 copies regular file space1/dir1/dir2/file1 to space1/dir3/file1 on client11
    Then user1 can stat [file1] in space1/dir1/dir2 on client11
    And user2 can stat [file1] in space1/dir1/dir2 on client21
    And user1 can stat [file1] in space1/dir3 on client11
    And user2 can stat [file1] in space1/dir3 on client21
    Then user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 sees [file1] in space1/dir3 on client11
    And user2 sees [file1] in space1/dir3 on client21
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir3/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/dir3/file1 on client21


  Scenario: Copy big regular file and check MD5
    When user1 creates directory and parents [space1/dir1/dir2, space1/dir3] on client11
    And user1 creates regular files [space1/dir1/dir2/file1] on client11
    And user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 writes 32 MB of random characters to space1/dir1/dir2/file1 on client11 and saves MD5
    And user1 copies regular file space1/dir1/dir2/file1 to space1/dir3/file1 on client11
    Then user1 can stat [file1] in space1/dir1/dir2 on client11
    And user2 can stat [file1] in space1/dir1/dir2 on client21
    And user1 can stat [file1] in space1/dir3 on client11
    And user2 can stat [file1] in space1/dir3 on client21
    Then user1 sees [file1] in space1/dir1/dir2 on client11
    And user2 sees [file1] in space1/dir1/dir2 on client21
    And user1 sees [file1] in space1/dir3 on client11
    And user2 sees [file1] in space1/dir3 on client21
    And user1 checks MD5 of space1/dir3/file1 on client11
    And user2 checks MD5 of space1/dir3/file1 on client21


  Scenario: Delete file opened by other user for reading
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/file1 on client11
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client11
    And user1 changes space1/dir1 mode to 777 on client11
    Then mode of user2's space1/dir1 is 777 on client21
    And user1 opens space1/dir1/file1 with mode r on client11
    And user2 deletes files [space1/dir1/file1] on client21
    And user2 can't stat [file1] in space1/dir1 on client21
    And user1 can't stat [file1] in space1/dir1 on client11
    And user2 doesn't see [file1] in space1/dir1 on client21
    And user1 doesn't see [file1] in space1/dir1 on client11
    And user1 reads "TEST TEXT ONEDATA" from previously opened file space1/dir1/file1 on client11
    And user1 closes space1/dir1/file1 on client11


  Scenario: Delete file opened by other user for reading and writing
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    Then mode of user2's space1/dir1 is 775 on client21
    And user1 opens space1/dir1/file1 with mode r+ on client11
    And user2 deletes files [space1/dir1/file1] on client21
    And user1 writes "TEST TEXT ONEDATA" to previously opened space1/dir1/file1 on client11
    And user1 sets current file position in space1/dir1/file1 at offset 0 on client11
    And user1 reads "TEST TEXT ONEDATA" from previously opened file space1/dir1/file1 on client11
    And user1 closes space1/dir1/file1 on client11
    And user1 can't stat [file1] in space1/dir1 on client11
    And user1 doesn't see [file1] in space1/dir1 on client11


  Scenario: Fail to delete file without permission, file is opened by other user
    When user1 creates directories [space1/dir1] on client11
    And user1 creates regular files [space1/dir1/file1] on client11
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [dir1] in space1 on client21
    And user2 sees [file1] in space1/dir1 on client21
    And user1 changes space1/dir1 mode to 755 on client11
    Then mode of user2's space1/dir1 is 755 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/dir1/file1 on client11
    And user1 opens space1/dir1/file1 with mode r+ on client11
    And user2 fails to delete files [space1/dir1/file1] on client21
    # because user2 has no write permission on space1/dir1
    And user1 closes space1/dir1/file1 on client11
    And user1 can stat [file1] in space1/dir1 on client11
    And user2 can stat [file1] in space1/dir1 on client21
    And user1 sees [file1] in space1/dir1 on client11
    And user2 sees [file1] in space1/dir1 on client21
    And user1 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/dir1/file1 on client21


  Scenario: Delete file right after closing it
    When user1 creates regular files [space1/file1] on client11
    And user1 sees [file1] in space1 on client11
    And user2 sees [file1] in space1 on client21
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user1 opens space1/file1 with mode r+ on client11
    And user1 closes space1/file1 on client11
    And user1 deletes files [space1/file1] on client11
    And space1 is empty for user1 on client11


  Scenario: Create nonempty file then copy it and remove source file
    When user1 creates regular files [space1/file1] on client11
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user1 copies regular file space1/file1 to space1/file1_copy on client11
    And user1 deletes files [space1/file1] on client11
    Then user1 reads "TEST TEXT ONEDATA" from file space1/file1_copy on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/file1_copy on client21


  Scenario: Create nonempty file then move it to another space
    When user1 creates regular files [space1/file1] on client11
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    And user2 reads "TEST TEXT ONEDATA" from file space1/file1 on client21
    And user1 renames space1/file1 to space2/file1_moved on client11
    Then user1 reads "TEST TEXT ONEDATA" from file space2/file1_moved on client11
    And user2 reads "TEST TEXT ONEDATA" from file space2/file1_moved on client21
