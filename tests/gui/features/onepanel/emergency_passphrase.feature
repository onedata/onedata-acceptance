Feature: Scenarios featuring emergency passphrase to Onepanel GUI

  Background:
    Given user opened browser_emergency window
    And opened browser_emergency with admin signed in to emergency interface of Onepanel service


  Scenario: User successfully change passphrase in emergency passphrase view
    When user of browser_emergency clicks on Emergency passphrase item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency clicks on Change passphrase button on emergency passphrase page
    And user of browser_emergency types "password" to Current passphrase input field on emergency passphrase page
    And user of browser_emergency types "new_password" to New passphrase input field on emergency passphrase page
    And user of browser_emergency types "new_password" to Retype new passphrase input field on emergency passphrase page
    And user of browser_emergency clicks on Change button on emergency passphrase page

    Then user of browser_emergency clicks on logout button in main menu
    And user of browser_emergency clicks Sign in to emergency interface in Onepanel login page
    And user of browser_emergency types "new_password" to Passphrase input in Onepanel login form
    And user of browser_emergency presses Sign in button in Onepanel login page
    And user of browser_emergency sees that he successfully signed in Oneprovider panel

    And user of browser_emergency changes passphrase from "new_password" to "password" on emergency passphrase page
    And user of browser_emergency clicks on logout button in main menu

