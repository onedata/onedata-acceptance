Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
                  - oneprovider-2:
                      storage: posix
                      size: 1000000
          space2:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
                  - oneprovider-2:
                      storage: posix
                      size: 1000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser

  Scenario: User creates space in one provider and sees that it was created also in other provider
    When user of browser clicks on the "spaces" tab in main menu sidebar
    And user of browser clicks on the Create button in spaces sidebar header
    And user of browser sees that "Create a new space" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "multiprov" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared
    And user of browser sees that space named "multiprov" has appeared in the spaces list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is space named "multiprov" in expanded "DATA SPACE MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "spaces" tab in main menu sidebar
    Then user of browser sees that space named "multiprov" has appeared in the spaces list


  Scenario: User changes name of space in one provider and sees that it was changed also in other provider
    When user of browser clicks on the "spaces" tab in main menu sidebar

    And user of browser clicks on settings icon displayed for "space1" item on the spaces sidebar list
    And user of browser clicks on the "RENAME" item in settings dropdown for space named "space1"
    And user of browser sees that "Rename a space" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "NewNameSpace" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees an info notify with text matching to: .*space1.*renamed.*NewNameSpace.*
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that space named "space1" has disappeared from the spaces list
    And user of browser sees that space named "NewNameSpace" has appeared in the spaces list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is space named "NewNameSpace" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that there is no space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "spaces" tab in main menu sidebar
    And user of browser sees that space named "NewNameSpace" has appeared in the spaces list
    Then user of browser sees that space named "space1" has disappeared from the spaces list


  Scenario: User leaves space in one provider and sees that it was leaved from also in other provider
    When user of browser clicks on the "spaces" tab in main menu sidebar

    And user of browser clicks on settings icon displayed for "space1" item on the spaces sidebar list
    And user of browser clicks on the "LEAVE SPACE" item in settings dropdown for space named "space1"
    And user of browser sees that "Leave a space" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees an info notify with text matching to: .*space1.*left
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that space named "space1" has disappeared from the spaces list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is no space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "spaces" tab in main menu sidebar
    Then user of browser sees that space named "space1" has disappeared from the spaces list


  Scenario: User creates group in one provider and sees that it was created also in other provider
    When user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser clicks on the Create button in groups sidebar header
    And user of browser sees that "Create a new group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "multiprov" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that group named "multiprov" has appeared in the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "GROUP MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is group named "multiprov" in expanded "GROUP MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "groups" tab in main menu sidebar
    Then user of browser sees that group named "multiprov" has appeared in the groups list


  Scenario: User changes name of group in one provider and sees that it was changed also in other provider
    When user of browser clicks on the "groups" tab in main menu sidebar

    And user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "RENAME" item in settings dropdown for group named "group1"
    And user of browser sees that "Rename a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "NewNameGroup" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees an info notify with text matching to: .*group1.*renamed.*NewNameGroup.*
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list
    And user of browser sees that group named "NewNameGroup" has appeared in the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "GROUP MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is group named "NewNameGroup" in expanded "GROUP MANAGEMENT" Onezone panel
    And user of browser sees that there is no group named "group1" in expanded "GROUP MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser sees that group named "group1" has disappeared from the groups list
    Then user of browser sees that group named "NewNameGroup" has appeared in the groups list

  Scenario: User leaves group in one provider and sees that it was leaved from also in other provider
    When user of browser clicks on the "groups" tab in main menu sidebar

    And user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "LEAVE THIS GROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Leave the group" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    And user of browser sees an info notify with text matching to: .*group1.*left
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser expands the "GROUP MANAGEMENT" Onezone sidebar panel
    And user of browser sees that there is no group named "group1" in expanded "GROUP MANAGEMENT" Onezone panel

    And user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser clicks on "oneprovider-2" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on the "Go to your files" button in provider popup
    And user of browser clicks on the "groups" tab in main menu sidebar
    Then user of browser sees that group named "group1" has disappeared from the groups list



