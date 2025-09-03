Feature: S3 service basic


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

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service
    And using REST, user1 creates token with following configuration:
        type: access
        interface: oneclient
        name: oc_token


  Scenario: User can see correct spaces listed in OneS3 service
    Then user of browser can see ["space1", "space2"] listed in OneS3 service


  Scenario: User can see presence of a space in OneS3 service
    Then user of browser can see there is "space1" in OneS3 service


  Scenario: User can download a file using OneS3 service
    When user of browser downloads "file1" from "space1" using OneS3 service
    Then user of browser sees that content of downloaded file "file1" is equal to: "11111"


  Scenario: User using GUI can see correct content of a file created using OneS3 service
    When user of browser creates "new_file" with content "22222" in "space1" using OneS3 service
    And user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "new_file" in file browser
    Then user of browser sees that content of downloaded file "new_file" is equal to: "22222"


  Scenario: User can see correct file content in OneS3 service
    Then user of browser can see that "file1" content is "11111" in "space1" using OneS3 service


  Scenario: User can see correct space content in OneS3 service
    Then user of browser can see items ["file1", "dir1/file1"] in "space1" using OneS3 service


  Scenario: User can see correct empty space content in OneS3 service
    Then user of browser can see items [] in "space2" using OneS3 service