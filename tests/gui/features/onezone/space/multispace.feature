Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
          space2:
            owner: user1


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User switches between spaces
    When user of browser clicks on Spaces in the sidebar
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser sees "space1" label on overview page
    And user of browser clicks "space2" on the spaces list in the sidebar
    Then user of browser sees "space2" label on overview page