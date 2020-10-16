Feature: Space join methods in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000

    And users opened [browser1, space_owner_browser] browsers' windows
    And users of [browser1, space_owner_browser] opened [onezone, onezone] page
    And users of [browser1, space_owner_browser] logged as [user1, space-owner-user] to [Onezone, Onezone] service
    And user of space_owner_browser expanded the "go to your files" Onezone sidebar panel
    And user of space_owner_browser clicked on "oneprovider-1" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of space_owner_browser clicked on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map
    And user of space_owner_browser seen that Oneprovider session has started
    And user of space_owner_browser clicked on the "spaces" tab in main menu sidebar


  Scenario: User successfully joins space from Onezone gui level (presses ENTER after entering token)
    # invite user1 to space
    When user of space_owner_browser clicks on settings icon displayed for "space1" item on the spaces sidebar list
    And user of space_owner_browser clicks on the "INVITE USER" item in settings dropdown for space named "space1"
    And user of space_owner_browser sees that "Invite user to the space" modal has appeared
    And user of space_owner_browser clicks on copy button in active modal
    And user of space_owner_browser sees an info notify with text matching to: .*copied to clipboard.*
    And user of space_owner_browser clicks "OK" confirmation button in displayed modal
    And user of space_owner_browser sees that the modal has disappeared
    And user of space_owner_browser sends copied token to user of browser1

    # user1 joins space
    And user of browser1 expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser1 clicks on "Join to space" button in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser1 sees that "Join a space" modal has appeared
    And user of browser1 clicks on input box in active modal
    And user of browser1 types received token on keyboard
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared

    Then user of browser1 sees that space named "space1" has appeared in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of space_owner_browser selects "space1" from spaces sidebar list
    And user of space_owner_browser refreshes site
    And user of space_owner_browser sees that "user1" item has appeared on current USERS permissions table in Spaces tab


  Scenario: User successfully joins space from Onezone gui level (clicks JOIN confirmation button after entering token)
    # invite user1 to space
    When user of space_owner_browser clicks on settings icon displayed for "space1" item on the spaces sidebar list
    And user of space_owner_browser clicks on the "INVITE USER" item in settings dropdown for space named "space1"
    And user of space_owner_browser sees that "Invite user to the space" modal has appeared
    And user of space_owner_browser clicks on copy button in active modal
    And user of space_owner_browser sees an info notify with text matching to: .*copied to clipboard.*
    And user of space_owner_browser clicks "OK" confirmation button in displayed modal
    And user of space_owner_browser sees that the modal has disappeared
    And user of space_owner_browser sends copied token to user of browser1

    # user1 joins space
    And user of browser1 expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser1 clicks on "Join to space" button in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser1 sees that "Join a space" modal has appeared
    And user of browser1 clicks on input box in active modal
    And user of browser1 types received token on keyboard
    And user of browser1 clicks "Join" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    Then user of browser1 sees that space named "space1" has appeared in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of space_owner_browser selects "space1" from spaces sidebar list
    And user of space_owner_browser refreshes site
    And user of space_owner_browser sees that "user1" item has appeared on current USERS permissions table in Spaces tab
