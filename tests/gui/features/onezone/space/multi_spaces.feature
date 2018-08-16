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
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

  Scenario: Switch between spaces
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser sees "space1" label on overview page
    And user of browser clicks "space2" on spaces on left sidebar menu
    Then user of browser sees "space2" label on overview page