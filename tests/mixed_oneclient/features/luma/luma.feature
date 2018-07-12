Feature: LUMA acceptance tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    
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
    
    And created in oneclient containers:
        users:
            user1: 1001
            user2: 1002
            user3: 1003
        groups:
            group1: 2000

    And opened browser with user3 logged to "onezone onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user3

    And [user1, user2] mounted [client1, client2] to oneprovider-1

  Scenario: LUMA test
    When using client1 user1 creates file "file_u1.txt" in space "space1"
    And using client2 user2 creates file "file_u2.txt" in space "space1"
    And user of browser succeeds to create file "file_u3.txt" in "space1"

    Then using client1 user1 sees "[file_u1.txt, file_u2.txt, file_u3.txt]" in space "space1"
    And using client2 user2 sees "[file_u1.txt, file_u2.txt, file_u3.txt]" in space "space1"
    
    And using client1 user1 sees that "file_u1.txt" in space "space1" has:
        owner_name: user1
        owner_group: group1

    And using client1 user1 sees that "file_u2.txt" in space "space1" has:
        owner_name: user2
        owner_group: group1

    And using client1 user1 sees that "file_u3.txt" in space "space1" has:
        owner_name: user3
        owner_group: group1

    And using client2 user2 sees that "file_u1.txt" in space "space1" has:
        owner_name: user1
        owner_group: group1

    And using client2 user2 sees that "file_u2.txt" in space "space1" has:
        owner_name: user2
        owner_group: group1

    And using client2 user2 sees that "file_u3.txt" in space "space1" has:
        owner_name: user3
        owner_group: group1
