Feature: Scenarios featuring login page to Onepanel GUI


  Background:
    Given user opened browser window
    And user of browser opened onezone zone panel page


  Scenario: User successfully login to emergency interface of Onezone panel
    Given user of browser logged as admin to emergency interface of Onepanel service
    Then user of browser is logged in Onezone panel service


  Scenario: User fails to login because of invalid credentials
    When user of browser clicks Sign in to emergency interface in Onepanel login page
    And user of browser types "as" to Passphrase input in Onepanel login form
    Then user of browser fails to sign in Onepanel due to invalid credentials


  Scenario: User successfully logout
    Given user of browser logged as admin to emergency interface of Onepanel service
    When user of browser clicks on logout button in main menu
    Then user of browser sees that he was logged out from Onepanel


  Scenario: User successfully goes to Onezone page from emeregency interface
    Given user of browser logged as admin to emergency interface of Onepanel service
    When user of browser clicks info button on warning bar in Onepanel page
    And user of browser clicks open in onezone in modal
    And user of browser logs as admin to Onezone service
    Then user of browser sees that URL matches: https?://[^/]*/onp/onezone/i#/.*


  Scenario: User successfully goes to Onezone page from Onepanel login page
    When user of browser clicks open in onezone in Onepanel login page
    And user of browser logs as admin to Onezone service
    Then user of browser sees that URL matches: https?://[^/]*/onp/onezone/i#/.*