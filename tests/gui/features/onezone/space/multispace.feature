Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
          space2:
            owner: space-owner-user


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User switches between spaces
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser sees "space1" label on overview page
    And user of browser clicks "space2" on the spaces list in the sidebar
    Then user of browser sees "space2" label on overview page
