Feature: Onezone account manage page


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


 Scenario: User successfully changes username in Profile page
   When user of browser expands account settings dropdown in the sidebar
   And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
   And user of browser activates edit box by clicking on the username in Profile page
   And user of browser types "new_username" to user name edit box in Profile page
   And user of browser clicks on confirm button displayed next to user name edit box in Profile page
   Then user of browser sees that the user name displayed in Profile page is "new_username"


 Scenario: User successfully logs in with new username
   When  user of browser changes username to new_username
   And user of browser logs out

   # log in with new username
   And user of browser types "new_username" to Username input in Onezone login form
   And user of browser types password of "user1" to Password input in Onezone login form
   And user of browser presses Sign in button in Onezone login page
   Then user of browser successfully signed in Onezone


 Scenario: User fails to log in using old username that has been changed
   When user of browser changes username to new_username
   And user of browser logs out

   # login with old username
   And user of browser types "user1" to Username input in Onezone login form
   And user of browser types password of "user1" to Password input in Onezone login form
   And user of browser presses Sign in button in Onezone login page
   Then user of browser sees error message about invalid credentials in Onezone login page


 Scenario: User successfully changes password in Profile page
   When user of browser expands account settings dropdown in the sidebar
   And user of browser clicks on Manage account item in expanded settings dropdown in the sidebar
   And user of browser activates edit box by clicking on the password in Profile page
   And user of browser types current password for "user1" in account management page
   And user of browser types "new_password" as new password for user in account management page
   And user of browser retypes "new_password" as new password for user in account management page
   And user of browser clicks on change password confirm button
   Then user of browser should see that the page title contains "Onezone"


 Scenario: User successfully logs in using new password in Profile page
   When user of browser changes user1 password to new_password
   And user of browser logs out

   # login with new password
   And user of browser types "user1" to Username input in Onezone login form
   And user of browser types "new_password" to Password input in Onezone login form
   And user of browser presses Sign in button in Onezone login page
   Then user of browser successfully signed in Onezone


 Scenario: User fails to log in using old password that has been changed
   When user of browser changes user1 password to new_password
   And user of browser logs out

   # login with old password
   And user of browser types "user1" to Username input in Onezone login form
   And user of browser types password of "user1" to Password input in Onezone login form
   And user of browser presses Sign in button in Onezone login page
   Then user of browser sees error message about invalid credentials in Onezone login page


 Scenario: User successfully logs in using new username and new password

   # change username
   When user of browser changes username to new_username

   # change password
   And user of browser changes user1 password to new_password
   And user of browser logs out

   # login with new login and new password
   And user of browser types "new_username" to Username input in Onezone login form
   And user of browser types "new_password" to Password input in Onezone login form
   And user of browser presses Sign in button in Onezone login page
   Then user of browser successfully signed in Onezone

