Feature: LUMA local feed acceptance tests with non-imported storage


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And there is "luma_storage" storage in "oneprovider-1" Oneprovider panel service used by admin with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
          LUMA feed: local
    And initial spaces configuration in "onezone" Onezone service:
        space1:
          owner: user1
          users:
            - user2
          providers:
            - oneprovider-1:
                storage: luma_storage
                size: 1000000
        space2:
          owner: user2
          users:
            - user1
          providers:
            - oneprovider-1:
                storage: luma_storage
                size: 1000000
    And directory tree structure on local file system:
          user1:
            file_upload_u1.txt:
              content: 1111
          user2:
            file_upload_u2.txt:
              content: 1111
    And oneclients [client1, client2] 
      mounted on client_hosts [oneclient-1, oneclient-1] respectively,
      using [token, token] by [user1, user2]
    And opened browsers with [user1, user2] signed in to [onezone, onezone] service


  Scenario: LUMA local feed storage mappings on POSIX storage for new files are respected in oneclient interface
    When LUMA local feed mappings are created with following configuration:
           oneprovider-1:
             luma_storage:
               type: posix
               users:
                 user1:
                   storage uid: 1001
                 user2:
                   storage uid: 1002
                   display uid: 1012
               spaces:
                 space1:
                   space POSIX storage defaults: 2001
                 space2:
                   space POSIX storage defaults: 2002
                   space display defaults: 2022

    And using oneclient1, user1 succeeds to create file named "file_oneclient_u1_s1.txt" in "space1" in oneprovider-1
    And using REST, user1 succeeds to create file named "file_rest_u1_s1.txt" in "space1" in oneprovider-1
    And using web GUI, user1 uploads local file "file_upload_u1.txt" to "space1"

    And using oneclient1, user1 succeeds to create file named "file_oneclient_u1_s2.txt" in "space2" in oneprovider-1
    And using REST, user1 succeeds to create file named "file_rest_u1_s2.txt" in "space2" in oneprovider-1
    And using web GUI, user1 uploads local file "file_upload_u1.txt" to "space2"

    And using oneclient2, user2 succeeds to create file named "file_oneclient_u2_s1.txt" in "space1" in oneprovider-1
    And using REST, user2 succeeds to create file named "file_rest_u2_s1.txt" in "space1" in oneprovider-1
    And using web GUI, user2 uploads local file "file_upload_u2.txt" to "space1"

    And using oneclient2, user2 succeeds to create file named "file_oneclient_u2_s2.txt" in "space2" in oneprovider-1
    And using REST, user2 succeeds to create file named "file_rest_u2_s2.txt" in "space2" in oneprovider-1
    And using web GUI, user2 uploads local file "file_upload_u2.txt" to "space2"

    # user1 in space1
    Then using oneclient1, user1 sees that owner's UID and GID for "file_oneclient_u1_s1.txt" in space "space1" are equal to 1001 and 2001 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "file_rest_u1_s1.txt" in space "space1" are equal to 1001 and 2001 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "file_upload_u1.txt" in space "space1" are equal to 1001 and 2001 respectively

    # user1 in space2
    And using oneclient1, user1 sees that owner's UID and GID for "file_oneclient_u1_s2.txt" in space "space2" are equal to 1001 and 2022 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "file_rest_u1_s2.txt" in space "space2" are equal to 1001 and 2022 respectively
    And using oneclient1, user1 sees that owner's UID and GID for "file_upload_u1.txt" in space "space2" are equal to 1001 and 2022 respectively

    # user2 in space1
    And using oneclient2, user2 sees that owner's UID and GID for "file_oneclient_u2_s1.txt" in space "space1" are equal to 1012 and 2001 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "file_rest_u2_s1.txt" in space "space1" are equal to 1012 and 2001 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "file_upload_u2.txt" in space "space1" are equal to 1012 and 2001 respectively

    # user2 in space2
    And using oneclient2, user2 sees that owner's UID and GID for "file_oneclient_u2_s2.txt" in space "space2" are equal to 1012 and 2022 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "file_rest_u2_s2.txt" in space "space2" are equal to 1012 and 2022 respectively
    And using oneclient2, user2 sees that owner's UID and GID for "file_upload_u2.txt" in space "space2" are equal to 1012 and 2022 respectively
