Feature: Delete Onezone user account


  Background:
    Given initial user for future delete configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User deletes account and fails to login using old credentials.
    When user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar

    # delete account
    And user of browser clicks on menu button on Profile page
    And user of browser clicks on remove user button in menu on Profile page
    And user of browser checks understand consequences of removing user account checkbox in modal
    And user of browser clicks on delete account button in modal

    # log in again
    And user of browser types "user1" to Username input in Onezone login form
    And user of browser types "password" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    Then user of browser sees error message about invalid credentials in Onezone login page


