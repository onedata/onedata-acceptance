Feature: Advanced management of space using OneS3 and boto3 with set token caveats


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


  Scenario: Using OneS3, user cannot modify space content with read-only token
    When using REST, user1 creates token with following configuration:
        name: new_token
        type: access
        caveats:
          interface: oneclient
          read only: True
    And user starts using token "new_token" in OneS3

    Then using OneS3, user user1 fails to create "new_file" with content "22222" in "space1"
    And using OneS3, user user1 fails to create "new_file" with content "22222" in "space2"

    And using OneS3, user user1 fails to delete "file1" in "space1"
    And using OneS3, user user1 fails to delete "file1" in "space2"

    And using OneS3, user user1 fails to copy "file1" to "file2" in "space1"
    And using OneS3, user user1 fails to copy "file1" to "file2" in "space2"

    And using OneS3, user user1 fails to put tag "env"="prod" on "file1" in "space1"
    And using OneS3, user user1 fails to put tag "env"="prod" on "file1" in "space2"

    And using OneS3, user user1 fails to delete tags from "file1" in "space1"
    And using OneS3, user user1 fails to delete tags from "file1" in "space2"

    And using OneS3, user user1 fails to put ACL "public-read" on "file1" in "space1"
    And using OneS3, user user1 fails to put ACL "public-read" on "file1" in "space2"


  Scenario: Using OneS3, user can only modify space content within a path, restricted by a token
    When using REST, user1 creates token with following configuration:
        name: new_token
        type: access
        caveats:
          interface: oneclient
          path:
            - space: space1
              path: /dir1
    And user starts using token "new_token" in OneS3

    Then using OneS3, user user1 can see spaces "[space1]"
    And using OneS3, user user1 can see only items ["dir1/file1"] in "space1"

    # cannot modify content outside token scope
    # default error is AccessDenied
    And using OneS3, user user1 fails to create "new_file" with content "22222" in "space1"
    And using OneS3, user user1 fails to delete "file1" in "space1"
    And using OneS3, user user1 fails to copy "file1" to "dir1/file2" in "space1"
    And using OneS3, user user1 fails to copy "dir1/file1" to "file2" in "space1"
    And using OneS3, user user1 fails to put tag "env"="prod" on "file1" in "space1"
    And using OneS3, user user1 fails to delete tags from "file1" in "space1"
    And using OneS3, user user1 fails to put ACL "public-read" on "file1" in "space1"

    # cannot see spaces without access to
    And using OneS3, user user1 fails to create "new_file" with content "22222" in "space2", because of NoSuchBucket error
    And using OneS3, user user1 fails to delete "file1" in "space2", because of NoSuchBucket error

    # can modify content within token scope
    And using OneS3, user user1 deletes "dir1/file1" in "space1"
    And using OneS3, user user1 creates "dir1/new_file" with content "22222" in "space1"
    And using OneS3, user user1 copies "dir1/new_file" to "dir1/new_file2" in "space1"
    And using OneS3, user user1 puts tag "env"="prod" on "dir1/new_file2" in "space1"
    And using OneS3, user user1 deletes tags from "dir1/new_file2" in "space1"
    And using OneS3, user user1 puts ACL "public-read" on "dir1/new_file2" in "space1"


  Scenario: User cannot use OneS3 with token restricted to use by another user
    When using REST, user1 creates token with following configuration:
        name: new_token
        type: access
        interface: oneclient
        caveats:
          consumer:
            - type: user
              by: id
              consumer name: user2
    And user starts using token "new_token" in OneS3

    Then using OneS3, user user1 fails to list spaces
    And using OneS3, user user1 fails to list items in "space1"
    And using OneS3, user user1 fails to list items in "space2"

    And using OneS3, user user1 fails to create "new_file" with content "22222" in "space1"
    And using OneS3, user user1 fails to create "new_file" with content "22222" in "space2"

    And using OneS3, user user1 fails to delete "file1" in "space1"
    And using OneS3, user user1 fails to delete "file1" in "space2"

    And using OneS3, user user1 fails to copy "file1" to "file2" in "space1"
    And using OneS3, user user1 fails to copy "file1" to "file2" in "space2"

    And using OneS3, user user1 fails to put tag "env"="prod" on "file1" in "space1"
    And using OneS3, user user1 fails to put tag "env"="prod" on "file1" in "space2"

    And using OneS3, user user1 fails to delete tags from "file1" in "space1"
    And using OneS3, user user1 fails to delete tags from "file1" in "space2"

    And using OneS3, user user1 fails to put ACL "public-read" on "file1" in "space1"
    And using OneS3, user user1 fails to put ACL "public-read" on "file1" in "space2"


  Scenario: User can use OneS3 with token restricted to use by the same user
    When using REST, user1 creates token with following configuration:
        name: new_token
        type: access
        interface: oneclient
        caveats:
          consumer:
            - type: user
              by: id
              consumer name: user1
    And user starts using token "new_token" in OneS3

    Then using OneS3, user user1 can see spaces "[space1]"
    And using OneS3, user user1 can see items ["file1", "dir1/file1"] in "space1"

    And using OneS3, user user1 creates "new_file" with content "22222" in "space1"
    And using OneS3, user user1 deletes "file1" in "space1"
    And using OneS3, user user1 copies "file1" to "file2" in "space1"
    And using OneS3, user user1 puts tag "env"="prod" on "file1" in "space1"
    And using OneS3, user user1 deletes tags from "file1" in "space1
    And using OneS3, user user1 puts ACL "public-read" on "file1" in "space1"


  Scenario: User can use OneS3 with token with set expiration time
    When using REST, user1 creates token with following configuration:
        name: new_token
        type: access
        interface: oneclient
        caveats:
          expiration:
            after: 10
    And user starts using token "new_token" in OneS3

    Then using OneS3, user user1 can see spaces "[space1, space2]"
    And using OneS3, user user1 can see items ["file1", "dir1/file1"] in "space1"

    And using OneS3, user user1 creates "new_file" with content "22222" in "space1"
    And using OneS3, user user1 deletes "file1" in "space1"
    And using OneS3, user user1 copies "file1" to "file2" in "space1"
    And using OneS3, user user1 puts tag "env"="prod" on "file1" in "space1"
    And using OneS3, user user1 deletes tags from "file1" in "space1"
    And using OneS3, user user1 puts ACL "public-read" on "file1" in "space1"
