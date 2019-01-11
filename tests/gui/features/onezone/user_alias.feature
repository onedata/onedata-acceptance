Feature: Management of user alias in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                alias: user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully changes his alias
    When user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
    And user of browser activates edit box by clicking on the user alias in Profile page
    And user of browser types "alias1" to user alias edit box in Profile page
    And user of browser clicks on confirm button displayed next to user alias edit box in Profile page
    Then user of browser sees that the user alias displayed in Profile page is "alias1"


  Scenario: User sees that his alias remains unchanged after resigning from renaming it (clicks cancel button after entering alias)
    When user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
    And user of browser activates edit box by clicking on the user alias in Profile page
    And user of browser types "alias1" to user alias edit box in Profile page
    And user of browser clicks on cancel button displayed next to user alias edit box in Profile page
    Then user of browser sees that the user alias displayed in Profile page is "user1"
