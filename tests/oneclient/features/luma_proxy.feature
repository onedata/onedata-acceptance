Feature: LUMA proxy test

  Background:
    Given oneclient mounted using token by user1


  Scenario: Operations on POSIX storage
    When user1 creates regular files [posix/file1]
    And user1 writes "TEST TEXT ONEDATA POSIX" to posix/file1
    Then user1 reads "TEST TEXT ONEDATA POSIX" from file posix/file1


  Scenario: Operations on CEPH storage
    When user1 creates regular files [ceph/file1]
    And user1 writes "TEST TEXT ONEDATA CEPH" to ceph/file1
    Then user1 reads "TEST TEXT ONEDATA CEPH" from file ceph/file1


  Scenario: Operations on Amazon S3 storage
    When user1 creates regular files [s3/file1]
    And user1 writes "TEST TEXT ONEDATA S3" to s3/file1
    Then user1 reads "TEST TEXT ONEDATA S3" from file s3/file1


  Scenario: Operations on Openstack Swift storage
    When user1 creates regular files [swift/file1]
    And user1 writes "TEST TEXT ONEDATA SWIFT" to swift/file1
    Then user1 reads "TEST TEXT ONEDATA SWIFT" from file swift/file1