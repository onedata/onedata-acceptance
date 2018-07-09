Feature: Management of user alias in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                alias: user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully changes his alias (clicks on confirm button after entering text)
    When user of browser expands the "USER ALIAS" Onezone sidebar panel
    And user of browser activates edit box by clicking on the user alias in expanded "USER ALIAS" Onezone panel
    And user of browser types "alias1" to user alias edit box in expanded "USER ALIAS" Onezone panel
    And user of browser clicks on confirm button displayed next to user alias edit box in expanded "USER ALIAS" Onezone panel
    Then user of browser sees that the user alias displayed in "USER ALIAS" Onezone panel is "alias1"


  Scenario: User successfully changes his alias (presses ENTER after entering text)
    When user of browser expands the "USER ALIAS" Onezone sidebar panel
    And user of browser activates edit box by clicking on the user alias in expanded "USER ALIAS" Onezone panel
    And user of browser types "alias2" to user alias edit box in expanded "USER ALIAS" Onezone panel
    And user of browser presses enter on keyboard
    Then user of browser sees that the user alias displayed in "USER ALIAS" Onezone panel is "alias2"


  Scenario: User sees that his alias remains unchanged after resigning from renaming it (clicks cancel button after entering alias)
    When user of browser expands the "USER ALIAS" Onezone sidebar panel
    And user of browser activates edit box by clicking on the user alias in expanded "USER ALIAS" Onezone panel
    And user of browser types "helloworld" to user alias edit box in expanded "USER ALIAS" Onezone panel
    And user of browser clicks on cancel button displayed next to user alias edit box in expanded "USER ALIAS" Onezone panel
    Then user of browser sees that the user alias displayed in "USER ALIAS" Onezone panel is "user1"
