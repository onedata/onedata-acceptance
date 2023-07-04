Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And user opened space_owner_browser window
    And user of space_owner_browser opened Onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service


  Scenario Outline: User successfully renames space
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser writes "space2" into rename space text field
    And user of space_owner_browser confirms rename the space using <confirmation_method>
    Then user of space_owner_browser sees that "space2" has appeared on the spaces list in the sidebar
    And user of space_owner_browser sees that "space1" has disappeared on the spaces list in the sidebar

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User successfully cancels rename space
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser writes "space2" into rename space text field
    And user of space_owner_browser clicks on cancel button on overview page
    Then user of space_owner_browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of space_owner_browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully leaves space
    When user of space_owner_browser creates "space2" space in Onezone

    # leave space
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Leave" button in space "space2" menu
    And user of space_owner_browser clicks on Leave button
    Then user of space_owner_browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully removes space
    When user of space_owner_browser creates "space2" space in Onezone

    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Remove" button in space "space2" menu
    And user of space_owner_browser clicks on understand notice checkbox in "Remove space" modal
    And user of space_owner_browser clicks on "Remove" button in "Remove space" modal
    Then user of space_owner_browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully cancels leave space
    When user of space_owner_browser creates "space2" space in Onezone

    # leave space
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Leave" button in space "space2" menu
    And user of space_owner_browser clicks on Cancel button
    Then user of space_owner_browser sees that "space2" has appeared on the spaces list in the sidebar


  Scenario: User sees no supporting providers after create new space
    When user of space_owner_browser creates "space2" space in Onezone
    Then user of space_owner_browser sees 0 number of supporting providers of "space2"


  Scenario: User sees that space size is zero right after creating
    When user of space_owner_browser creates "space2" space in Onezone
    Then user of space_owner_browser sees 0 B size of the "space2"


  Scenario: User sees that provider is added to supporters list after supporting space
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Providers" of "space1" space in the sidebar
    Then user of space_owner_browser sees "oneprovider-1" is on the providers list
    And user of space_owner_browser sees that length of providers list equals number of supporting providers of "space1"


  Scenario: User successfully copies support token (space has already supported by one provider)
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Providers" of "space1" space in the sidebar
    And user of space_owner_browser clicks Add support button on providers page
    And user of space_owner_browser clicks Copy button on Add support page
    Then user of space_owner_browser sees copy token and token in support token text field are the same
    And user of space_owner_browser sees that copied token is non-empty


  Scenario: User can leave the space which was owned by them and was its only user
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks show view expand button in space members subpage header
    And user of space_owner_browser clicks effective view mode in space members subpage
    And user of space_owner_browser sees 1 user in space members subpage
    And user of space_owner_browser sees [you, owner, direct] status labels for "space-owner-user" user in space members subpage

    And user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Leave" button in space "space1" menu
    And user of space_owner_browser clicks on Leave button
    Then user of space_owner_browser sees that "space1" has disappeared on the spaces list in the sidebar
