Feature: Onezone login page
  A site where you can login to Onezone.

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened onezone page


  Scenario: Onezone login page renders with proper title
    Then user of browser should see that the page title contains "Onezone"


  Scenario: User successfully logins and logouts
    When user of browser types "user1" to Username input in Onezone login form
    And user of browser types password of "user1" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    And user of browser sees an info notify with text matching to: Authentication succeeded!
    And user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Logout item in expanded settings dropdown in the sidebar
    Then user of browser sees that URL matches: https?://[^/]*/ozw/onezone/i#/login
    And user of browser should see that the page title contains "Onezone"
