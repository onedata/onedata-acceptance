Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User successfully renames space
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser writes "space2" into rename space text field
    And user of browser confirms rename the space using <confirmation_method>
    Then user of browser sees that "space2" has appeared on the spaces list in the sidebar
    And user of browser sees that "space1" has disappeared on the spaces list in the sidebar

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User successfully cancels rename space
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser writes "space2" into rename space text field
    And user of browser clicks on cancel button on overview page
    Then user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully leaves space
    When user of browser creates "space2" space in Onezone

    # leave space
    And user of browser clicks "space2" on the spaces list in the sidebar
    And user of browser clicks on "Leave space" button in space menu
    And user of browser clicks on yes button
    Then user of browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully cancels leave space
    When user of browser creates "space2" space in Onezone

    # leave space
    And user of browser clicks "space2" on the spaces list in the sidebar
    And user of browser clicks on "Leave space" button in space menu
    And user of browser clicks on no button
    Then user of browser sees that "space2" has appeared on the spaces list in the sidebar


  Scenario: User sees no supporting providers after create new space
    When user of browser creates "space2" space in Onezone
    Then user of browser sees 0 number of supporting providers of "space2"


  Scenario: User sees that space size is zero right after creating
    When user of browser creates "space2" space in Onezone
    Then user of browser sees 0 B size of the "space2"


  Scenario: User sees that provider is added to supporters list after supporting space
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    Then user of browser sees "oneprovider-1" is on the providers list
    And user of browser sees that length of providers list equals number of supporting providers of "space1"


  Scenario: User successfully copies support token (space has already supported by one provider)
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Add support button on providers page
    And user of browser clicks Copy button on Add support page
    Then user of browser sees copy token and token in support token text field are the same
    And user of browser sees that copied token is non-empty


  Scenario: User can leave the space which was owned by them and was its only user
    When user of browser clicks Members of "space1" in the sidebar
    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks effective view mode in space members subpage
    And user of browser sees 1 user in space members subpage
    And user of browser sees [you, owner, direct] status labels for "user1" user in space members subpage

    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "Leave space" button in space menu
    And user of browser clicks on yes button
    Then user of browser sees that "space1" has disappeared on the spaces list in the sidebar
