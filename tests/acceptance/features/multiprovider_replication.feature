Feature: Multiprovider_replication

  Background:
    Given [user1, user2] mount oneclients [client11, client21] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [token, token]


  Scenario: Create files and see them on external provider
    When user1 creates regular files [space1/file1, space1/file2, space1/file3] on client11
    Then user2 can stat [file1, file2, file3] in space1 on client21
    Then user2 sees [file1, file2, file3] in space1 on client21


  Scenario: Create empty file and read it on external provider
    When user1 creates regular files [space1/file] on client11
    Then user2 reads "" from file space1/file on client21


  Scenario: Write to file and check size on remote provider
    When user1 creates regular files [space1/file] on client11
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    Then size of user2's space1/file1 is 17 bytes on client21


  Scenario: Write to file and read on remote provider
    When user1 creates regular files [space1/file1] on client11
    And user1 writes "TEST TEXT ONEDATA" to space1/file1 on client11
    Then user2 reads "TEST TEXT ONEDATA" from file space1/file1 on client21


  Scenario: Big file transfer with MD5 check
    When user1 creates regular files [space1/file1] on client11
    And user1 writes 8 MB of random characters to space1/file1 on client11 and saves MD5
    Then user2 checks MD5 of space1/file1 on client21
    And user1 writes 8 MB of random characters to space1/file1 on client11 and saves MD5
    And user2 checks MD5 of space1/file1 on client21


  Scenario: Create nonempty file and override its contents on remote provider
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 changes space1/file1 mode to 666 on client11
    And mode of user2's space1/file1 is 666 on client21
    And user1 writes "123456789" to space1/file1 on client11
    And user waits 10 seconds
    And user2 writes "abcd" to space1/file1 on client21
    And user1 reads "abcd" from file space1/file1 on client11


  Scenario: Create nonempty file and remove it on remote provider
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 writes "123456789" to space1/file1 on client11
    And user1 deletes files [space1/file1] on client11
    Then user1 can't stat [file1] in space1 on client11
    And user2 can't stat [file1] in space1 on client21
    Then user1 doesn't see [file1] in space1 on client11
    And user2 doesn't see [file1] in space1 on client21


  Scenario: Create nonempty file, append remotely, append locally and read both
    When user1 creates regular files [space1/file1] on client11
    And user1 writes "a" to space1/file1 on client11
    And user1 changes space1/file1 mode to 666 on client11
    And mode of user2's space1/file1 is 666 on client21
    And user1 waits 10 seconds
    And user2 appends "b" to space1/file1 on client21
    And user1 waits 10 seconds
    And user1 appends "c" to space1/file1 on client11
    Then user1 reads "abc" from file space1/file1 on client11
    And user2 reads "abc" from file space1/file1 on client21


  Scenario: Concurrently write disjoint ranges and read the same on both providers
    When user1 creates regular files [space1/file1] on client11
    And user2 sees [file1] in space1 on client21
    And user1 changes space1/file1 mode to 666 on client11
    And mode of user2's space1/file1 is 666 on client21
    And user2 writes "defg" at offset 3 to space1/file1 on client21
    And user1 writes "abc" at offset 0 to space1/file1 on client11
    Then user1 reads "abcdefg" from file space1/file1 on client11
    And user2 reads "abcdefg" from file space1/file1 on client21
