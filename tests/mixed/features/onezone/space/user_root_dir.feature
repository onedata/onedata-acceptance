Feature: Basic operations on user root dir using REST API

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browser with user1 signed in to "onezone" service


  Scenario: User fails to remove user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to remove user root dir of space "space1" in oneprovider-1


  Scenario: User fails to move user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to move user root dir of "space1" in oneprovider-1


  Scenario: User fails to create file in user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to create file "some_name.txt" in root dir of "space1" in oneprovider-1


  Scenario: User fails to add QoS requirement to user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to add qos requirement "geo=PL" to user root dir of "space1" in oneprovider-1


  Scenario: User fails to add metadata to user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata "{"id": 1}" to user root dir of "space1" in oneprovider-1


  Scenario: User fails to establish dataset of user root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset to user root dir of "space1" in oneprovider-1