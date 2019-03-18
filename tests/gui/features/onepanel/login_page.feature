Feature: Scenarios featuring login page to Onepanel GUI


  Background:
    Given user opened browser window
    And user of browser opened onezone zone panel page


  Scenario: User successfully login to emergency interface Zone panel
    Given user of browser logged as admin to emergency interface Onepanel service
    Then user of browser sees that he successfully logged in Onezone panel


  Scenario: User fails to login because of invalid credentials
    When user of browser clicks Log in to emergency interface in Onepanel login page
    When user of browser types "admin" to Username input in Onepanel login form
    And user of browser types "as" to Password input in Onepanel login form
    And user of browser presses Sign in button in Onepanel login page
    Then user of browser sees error message about invalid credentials in Onepanel login page


  Scenario: User successfully logout
    Given user of browser logged as admin to emergency interface Onepanel service
    When user of browser clicks on logout button in main menu
    Then user of browser sees that he was logged out from Onepanel


  Scenario: User successfully go to onezone page from emeregency interface
    Given user of browser logged as admin to emergency interface Onepanel service
    When user of browser clicks button on warning bar in Onepanel page
    And user of browser clicks open in onezone in modal
    And user of browser logs as admin to Onezone service
    Then user of browser sees that URL matches: https?://[^/]*/ozp/onezone/i#/onedata/clusters/.*


  Scenario: User successfully go to onezone page from Onepanel login page
    When user of browser clicks open in onezone in Onepanel login page
    And user of browser logs as admin to Onezone service
    Then user of browser sees that URL matches: https?://[^/]*/ozp/onezone/i#/onedata/clusters/.*