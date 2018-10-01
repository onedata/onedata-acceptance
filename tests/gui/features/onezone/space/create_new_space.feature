Feature: Create new space

  Examples:
    | confirmation_method |
    | enter               |
    | button              |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User creates new space (with new space button in the sidebar)
    When user of browser clicks on Spaces in the sidebar
    And user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "space1" into space name text field
    And user of browser confirms create new space using <confirmation_method>
    Then user of browser sees that "space1" has appeared on the spaces list in the sidebar


  Scenario Outline: User creates new space (with Get started button)
    When user of browser clicks Get started in spaces sidebar
    And user of browser clicks Create a space on Welcome page
    And user of browser writes "space1" into space name text field
    And user of browser confirms create new space using <confirmation_method>
    Then user of browser sees that "space1" has appeared on the spaces list in the sidebar
