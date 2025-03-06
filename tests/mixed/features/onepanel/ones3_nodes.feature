Feature: OneS3 nodes operations using REST API

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1


  Scenario: User can see suitable statutes of oneS3 node
    When user user1 adds oneS3 node to provider cluster in oneprovider-1
    And user user1 sees that oneS3 node in provider cluster in oneprovider-1 is of status "healthy"
    And user user1 stops oneS3 node in provider cluster in oneprovider-1
    Then user user1 sees that oneS3 node in provider cluster in oneprovider-1 is of status "stopped"