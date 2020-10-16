Feature: Onezone account manage page


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully changes username in Profile page
    When user of browser changes user1 username to new_username
    Then user of browser sees that the user's name displayed in Profile page is "new_username"
    And user of browser logs out from Onezone page

    # fail to log in with old username
    And user of browser types "user1" to Username input in Onezone login form
    And user of browser types password of "user1" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    And user of browser sees error message about invalid credentials in Onezone login page

    # successfully log in with new username
    And user of browser refreshes site
    And user of browser types "new_username" to Username input in Onezone login form
    And user of browser types password of "user1" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    And user of browser successfully signed in Onezone


 Scenario: User successfully changes password in Profile page
    When user of browser changes user1 password to new_password
    And user of browser logs out from Onezone page

    # fail to log in with old password
    And user of browser types "user1" to Username input in Onezone login form
    And user of browser types "password" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    Then user of browser sees error message about invalid credentials in Onezone login page

    # successfully log in with new password
    And user of browser refreshes site
    And user of browser types "user1" to Username input in Onezone login form
    And user of browser types "new_password" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    And user of browser successfully signed in Onezone


 Scenario: User successfully logs in using new username and new password

    # change username
    When user of browser changes user1 username to new_username

    # change password
    And user of browser changes user1 password to new_password

    And user of browser logs out from Onezone page

    # successfully log in with new login and new password
    And user of browser types "new_username" to Username input in Onezone login form
    And user of browser types "new_password" to Password input in Onezone login form
    And user of browser presses Sign in button in Onezone login page
    Then user of browser successfully signed in Onezone

