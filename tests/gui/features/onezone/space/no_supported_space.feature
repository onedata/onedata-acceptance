Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User generates different support tokens (space has no support)
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Add support button on providers page
    And user of browser clicks Copy button on Add support page
    And user of browser clicks Generate another token on Add support page
    Then user of browser sees that another token is different than first one


  Scenario: User generates different expose existing data tokens (space has no support)
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Add support button on providers page
    And user of browser clicks Expose existing data set tab on Add support page
    And user of browser clicks Copy button on Add support page
    And user of browser clicks Generate another token on Add support page
    Then user of browser sees that another token is different than first one