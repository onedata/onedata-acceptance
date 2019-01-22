Feature: LUMA acceptance tests

  Examples:
  | client1    | client2    | client3 |
  | oneclient1 | oneclient2 | web GUI |


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And oneclients [client1, client2]
      mounted in [/home/user1/onedata, /home/user2/onedata]
      on client_hosts [oneclient-1, oneclient-1] respectively,
      using [token, token] by [user1, user2]
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            users:
                - user2
                - user3
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And created LUMA mappings:
        users:
            user1: 1001
            user2: 1002
            user3: 1003
        space_gid:
            space1: 2000
        storage_name: posix
        storage_type: posix
    And opened browser with user3 logged to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user3


  Scenario: Users create files using web gui an clients and they see that ownership is correctly mapped
    When using <client1>, user1 succeeds to create file named "file_u1.txt" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to create file named "file_u2.txt" in "space1" in oneprovider-1
    And using <client3>, user3 succeeds to create file named "file_u3.txt" in "space1" in oneprovider-1

    Then using <client1>, user1 succeeds to see items named "[file_u1.txt, file_u2.txt, file_u3.txt]" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to see items named "[file_u1.txt, file_u2.txt, file_u3.txt]" in "space1" in oneprovider-1

    And using <client1>, user1 sees that "file_u1.txt" in space "space1" has:
        uid: 1001
        gid: 2000

    And using <client1>, user1 sees that "file_u2.txt" in space "space1" has:
        uid: 1002
        gid: 2000

    And using <client1>, user1 sees that "file_u3.txt" in space "space1" has:
        uid: 1003
        gid: 2000

    And using <client2>, user2 sees that "file_u1.txt" in space "space1" has:
        uid: 1001
        gid: 2000

    And using <client2>, user2 sees that "file_u2.txt" in space "space1" has:
        uid: 1002
        gid: 2000

    And using <client2>, user2 sees that "file_u3.txt" in space "space1" has:
        uid: 1003
        gid: 2000
