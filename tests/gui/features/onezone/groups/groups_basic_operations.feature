Feature: Basic management of groups with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User renames group
    When user of browser clicks on button "Rename" in group "group1" menu
    And user of browser writes "group2" into rename group text field
    And user of browser confirms group rename using <confirmation_method>
    Then user of browser sees group "group2" on groups list
    And user of browser does not see group "group1" on groups list

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User removes group
    When user of browser clicks on button "Remove" in group "group1" menu
    And user of browser clicks on button "Remove" in modal "REMOVE GROUP"
    Then user of browser does not see group "group1" on groups list


  Scenario: User leaves group
    When user of browser clicks on button "Leave" in group "group1" menu
    And user of browser clicks on button "Leave" in modal "LEAVE GROUP"
    Then user of browser does not see group "group1" on groups list


  Scenario Outline: User fails to add group as its subgroup
    When user of browser clicks on text "generate an invitation token" in group "group1" members groups list
    And user of browser copies invitation token from Groups page

    And user of browser goes to group "group1" parents subpage
    And user of browser pastes copied token into group token text field
    And user of browser confirms using <confirmation_method>

    Then user of browser sees that error modal with text "joining group as subgroup failed" appeared

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User generates group invitation token
    When user of browser clicks on button "Invite group" in group "group1" members menu
    And user of browser sees that area with invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User generates user invitation token
    When user of browser clicks on button "Invite user" in group "group1" members menu
    And user of browser sees that area with invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User fails to view group after leaving it
    When user of browser goes to group "group1" main subpage
    And user of browser copies a first resource ID from URL
    And user of browser leaves group "group1"

    And user of browser refreshes site

    And user of browser changes webapp path to "/#/onedata/groups" concatenated with copied item

    Then user of browser see that page with text "RESOURCE NOT FOUND" appeared




