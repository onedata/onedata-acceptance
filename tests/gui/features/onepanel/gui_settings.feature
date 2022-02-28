Feature: Management of GUI settings in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User sees notification on log-in page after setting sign-in notification
    When user of browser sets sign in notification: "test sign-in notification" in GUI settings page of "onezone"
    And user of browser logs out from Onezone page
    Then user of browser sees sign in notification message: "test sign-in notification" in the login page
    And user of browser logs as admin to Onezone service
    And user of browser removes sign in notification: "test sign-in notification" in GUI settings page of "onezone"


  Scenario: User sees terms of use page after setting terms of use
    When user of browser sets terms of use: "test terms of use" in GUI settings page of "onezone"
    And user of browser clicks on Data in the main menu
    And user of browser goes to terms of use page
    Then user of browser sees "test terms of use" on terms of use page
    And user of browser clicks "Back to main page" button on terms of use page
    And user of browser removes terms of use: "test terms of use" in GUI settings page of "onezone"


  Scenario: User sees information about using cookies and link to privacy policy terms after setting cookies and privacy policy
    When user of browser sets privacy policy: "test privacy policy" in GUI settings page of "onezone"
    And user of browser sets cookie consent notification: "test cookie consent" in GUI settings page of "onezone"
    And user of browser inserts privacy policy link in cookie consent notification in GUI settings page of "onezone"
    And user of browser clicks on Data in the main menu
    And user of browser clicks on privacy policy link in cookies popup
    Then user of browser sees "test privacy policy" on privacy policy page
    And user of browser clicks "I understand" button in cookies popup
    And user of browser clicks "Back to main page" button on privacy policy page
    And user of browser removes privacy policy: "test privacy policy" in GUI settings page of "onezone"
    And user of browser removes cookie consent notification: "test cookie consent" in GUI settings page of "onezone"




