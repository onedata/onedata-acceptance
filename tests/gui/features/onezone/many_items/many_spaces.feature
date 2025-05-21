Feature: Management of a great number of spaces

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see correct number of previously created spaces in spaces list in the sidebar
    When using REST, user1 creates 500 spaces in "onezone" Onezone service
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    Then user of browser can see there are 500 spaces on the spaces list in the sidebar


  Scenario: User can see that correct space is opened after refreshing page
    When using REST, user1 creates 500 spaces in "onezone" Onezone service
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser opens "space250" space on the spaces list in the sidebar
    And user of browser refreshes site
    And user of browser can see that opened space is "space250" on the spaces list in the sidebar
