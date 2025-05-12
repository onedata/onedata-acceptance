Feature: Management of great number of groups

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see correct number of previously created groups in groups page
    When using REST, user user1 creates 500 groups
    And user of browser clicks on Groups in the main menu
    Then user of browser can see there is group "group0" in groups page
    And user of browser can see there are 500 groups in groups page