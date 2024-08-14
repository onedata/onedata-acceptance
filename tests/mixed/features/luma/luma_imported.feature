Feature: LUMA local feed acceptance tests with imported storage


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And there are no spaces of user1 in "onezone" Onezone service
    And "luma_storage" storage backend in "oneprovider-1" Oneprovider panel service used by admin with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
          LUMA feed: local
          imported storage: true
    And there is following users configuration in storage's mount point:
          luma_group:
            GID: 3013
            users:
              s_user1: 7001
              s_user2: 7002
              s_user3: 7003
    And ownership ":luma_group" is granted for storage's mount point
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            users:
              - user2
            providers:
              - oneprovider-1:
                  storage: luma_storage
                  size: 1000000000
    And directory tree structure on local file system:
          user1:
            file_user1.txt:
              size: 1 MiB
            file_user2.txt:
              size: 1 MiB
            file_another_user.txt:
              size: 1 MiB
            upload_file.txt:
              size: 1 MiB
    And oneclients [client1, client2]
      mounted on client_hosts [oneclient-1, oneclient-1] respectively,
      using [token, token] by [user1, user2]
    And opened browsers with [user1, user2] signed in to [onezone, onezone] service


  Scenario: LUMA local feed Onedata user mappings on POSIX imported storage are respected in web interface and in oneclient
    When LUMA local feed mappings for imported storage "luma_storage" at "oneprovider-1" are created between [7001, 7002] and [user1, user2]

    And user user1 copies file_user1.txt to provider's storage mount point
    And user user1 copies file_user2.txt to provider's storage mount point
    And user user1 copies file_another_user.txt to provider's storage mount point

    # change file owners on storage
    And user user1 sets s_user1:luma_group as file_user1.txt owner on provider's storage mount point
    And user user1 sets s_user2:luma_group as file_user2.txt owner on provider's storage mount point
    And user user1 sets s_user3:luma_group as file_another_user.txt owner on provider's storage mount point

    And using REST, user1 forces start of storage import scan for "space1" at "oneprovider-1"
    And user1 is idle for 5 seconds

    And using web GUI, user1 succeeds to see item named "file_user1.txt" in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "file_user2.txt" in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "file_another_user.txt" in "space1" in oneprovider-1
    And using web GUI, user1 uploads local file "upload_file.txt" to "space1"

    Then using web GUI, user1 sees that "user1 (user1)" is owner of "file_user1.txt"

    And using web GUI, user2 succeeds to see item named "file_user1.txt" in "space1" in oneprovider-1
    And using web GUI, user2 succeeds to see item named "file_user2.txt" in "space1" in oneprovider-1
    And using web GUI, user2 fails to see item named "file_another_user.txt" in "space1" in oneprovider-1
    And using web GUI, user2 sees that "user2 (user2)" is owner of "file_user2.txt"

    And using oneclient1, user1 sees that owner's UID and GID for "file_user1.txt" in space "space1" are equal to 7001 and 3013 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "file_user2.txt" in space "space1" are equal to 7002 and 3013 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "upload_file.txt" in space "space1" are equal to 7001 and 3013 respectively
    And using oneclient1, user1 fails to see item named "file_another_user.txt" in "space1" in oneprovider-1

    And using oneclient2, user2 sees that owner's UID and GID for "file_user1.txt" in space "space1" are equal to 7001 and 3013 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "file_user2.txt" in space "space1" are equal to 7002 and 3013 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "upload_file.txt" in space "space1" are equal to 7001 and 3013 respectively
    And using oneclient2, user2 fails to see item named "file_another_user.txt" in "space1" in oneprovider-1
