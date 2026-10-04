Feature: Advanced management of space using OneS3 and boto3


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 10000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1: 11111
                    - file1: 11111
        space2:
            owner: user1
            providers:
                - oneprovider-2:
                    storage: s3
                    size: 10000000000
            storage:
                defaults:
                    provider: oneprovider-2
                directory tree:
                    - dir1:
                      - file1: 11111
                    - file1: 11111

    And using REST, user1 creates token with following configuration:
        type: access
        interface: oneclient
        name: oc_token


  Scenario: User renames spaces using REST and can see correct spaces listed in OneS3 service
    When using REST, user1 renames space named "space1" to "helloworld1" in "onezone" Onezone service
    And using REST, user1 renames space named "space2" to "helloworld2" in "onezone" Onezone service
    Then using OneS3 and list buckets boto3 function, user user1 can see spaces ["helloworld1", "helloworld2"]


  Scenario: User renames spaces using Web GUI and can see correct spaces listed in OneS3 service
    Given opened browsers with [user1] signed in to [onezone] service

    When using web GUI, user1 renames space named "space1" to "helloworld1" in "onezone" Onezone service
    And using web GUI, user1 renames space named "space2" to "helloworld2" in "onezone" Onezone service
    Then using OneS3 and list buckets boto3 function, user user1 can see spaces ["helloworld1", "helloworld2"]


  Scenario: User recreates spaces using REST and can see correct spaces listed in OneS3 service
    When using REST, user1 removes space named "space1" in "onezone" Onezone service
    And using REST, user1 removes space named "space2" in "onezone" Onezone service
    Then using OneS3 and list buckets boto3 function, user user1 can see spaces []
    And using REST, user1 creates space "space1" in "onezone" Onezone service
    And using REST, user1 creates space "space2" in "onezone" Onezone service
    And using OneS3 and list buckets boto3 function, user user1 can see spaces ["space1", "space2"]

