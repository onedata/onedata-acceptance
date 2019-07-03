Feature: Management of user full name in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully changes his full name
    When user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
    And user of browser activates edit box by clicking on the user full name in Profile page
    And user of browser types "user2" to user full name edit box in Profile page
    And user of browser clicks on confirm button displayed next to user full name edit box in Profile page
    Then user of browser sees that the user full name displayed in Profile page is "user2"


  Scenario: User sees that his full name remains unchanged after resigning from renaming it (clicks cancel button after entering full name)
    When user of browser expands account settings dropdown in the sidebar
    And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
    And user of browser activates edit box by clicking on the user full name in Profile page
    And user of browser types "user2" to user full name edit box in Profile page
    And user of browser clicks on cancel button displayed next to user full name edit box in Profile page
    Then user of browser sees that the user full name displayed in Profile page is "user1"
