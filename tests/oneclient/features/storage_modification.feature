Feature: Storage_modification

  Background:
    Given oneclient mounted using token by user1

  Scenario: Change Ceph parameters with active oneclient connection
    When user1 creates regular files [ceph/file1]
    And user1 writes "TEST TEXT ONEDATA CEPH" to ceph/file1
    Then user1 reads "TEST TEXT ONEDATA CEPH" from file ceph/file1
    Then using REST, user1 changes storage "cephrados" named "ceph" parameter "pool_name" to "no_such_pool" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 fails to write "ABCD" to ceph/file1
    Then using REST, user1 changes storage "cephrados" named "ceph" parameter "pool_name" to "test" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 reads "TEST TEXT ONEDATA CEPH" from file ceph/file1

  Scenario: Change S3 parameters with active oneclient connection
    When user1 creates regular files [s3/file1]
    And user1 writes "TEST TEXT ONEDATA S3" to s3/file1
    Then user1 reads "TEST TEXT ONEDATA S3" from file s3/file1
    Then using REST, user1 changes storage "s3" named "s3" parameter "bucket_name" to "no_such_bucket" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 fails to write "ABCD" to s3/file1
    Then using REST, user1 changes storage "s3" named "s3" parameter "bucket_name" to "test" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 reads "TEST TEXT ONEDATA S3" from file s3/file1

  Scenario: Change POSIX parameters with active oneclient connection
    When user1 creates regular files [posix/file1]
    And user1 writes "TEST TEXT ONEDATA POSIX" to posix/file1
    Then user1 reads "TEST TEXT ONEDATA POSIX" from file posix/file1
    Then using REST, user1 changes storage "posix" named "local-volume-1" parameter "mount_point" to "/tmp" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 fails to write "ABCD" to posix/file1
    Then using REST, user1 changes storage "posix" named "local-volume-1" parameter "mount_point" to "/volumes/local-volume-1" at provider "dev-oneprovider-krakow"
    Then user1 is idle for 15 seconds
    Then user1 reads "TEST TEXT ONEDATA POSIX" from file posix/file1