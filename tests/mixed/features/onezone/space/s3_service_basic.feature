Feature: Basic management of space using OneS3 and boto3


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
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
                - oneprovider-1:
                    storage: posix
                    size: 10000000000

    And using REST, user1 creates token with following configuration:
        type: access
        interface: oneclient
        name: oc_token


  Scenario: User can see correct spaces listed in OneS3 service
    Then using OneS3, user user1 can see spaces "[space1, space2]"


  Scenario: User can see presence of a space in OneS3 service
    Then using OneS3, user user1 can see there is a space "space1"
    And using OneS3, user user1 can see there is a space "space1"


  Scenario: User can download a file using OneS3 service
    # browser here is needed to construct download dir path
    When using OneS3, user of browser downloads "file1" from "space1"
    Then user of browser sees that content of downloaded file "file1" is equal to: "11111"


  Scenario: User using GUI can see correct content of a file created using OneS3 service
    Given user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service

    When using OneS3, user user1 creates "new_file" with content "22222" in "space1"
    And user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "new_file" in file browser
    Then user of browser sees that content of downloaded file "new_file" is equal to: "22222"


  Scenario: User can see correct file content in OneS3 service
    Then using OneS3, user user1 can see that "file1" content is "11111" in "space1"


  Scenario: User can see correct non-empty space content in OneS3 service
    Then using OneS3, user user1 can see items ["file1", "dir1/file1"] in "space1"


  Scenario: User can see correct empty space content in OneS3 service
    Then using OneS3, user user1 can see items [] in "space2"