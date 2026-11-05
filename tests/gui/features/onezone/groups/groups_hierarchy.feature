Feature: Basic management of groups hierarchy with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          parent_group:
            owner: user1
            groups:
              - base_group

          base_group:
            owner: user1
            groups:
              - child_group

          child_group:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User adds newly created children group
    When user of browser opens group "parent_group" hierarchy subpage
    And user of browser clicks on group "parent_group" menu button in hierarchy subpage
    And user of browser clicks on "Add child group" in group hierarchy menu
    And user of browser clicks on "Create new group" in group hierarchy menu
    And user of browser writes "group4" into group name text field in create group modal
    And user of browser clicks on "Create" button in modal "CREATE GROUP"
    Then user of browser sees "group4" as a child of "parent_group" in hierarchy subpage


  Scenario: User adds newly created parent group
    When user of browser opens group "parent_group" hierarchy subpage
    And user of browser clicks on group "parent_group" menu button in hierarchy subpage
    And user of browser clicks on "Add parent group" in group hierarchy menu
    And user of browser clicks on "Create new group" in group hierarchy menu
    And user of browser writes "group4" into group name text field in create group modal
    And user of browser clicks on "Create" button in modal "CREATE GROUP"
    And user of browser clicks show parent groups in hierarchy subpage
    Then user of browser sees "group4" as a parent of "parent_group" in hierarchy subpage


  Scenario: User removes child group
    When user of browser opens group "base_group" hierarchy subpage
    And user of browser clicks on group "child_group" menu button in hierarchy subpage
    And user of browser clicks on "Remove" in group hierarchy menu
    And user of browser clicks on "Remove" button in modal "REMOVE GROUP"
    Then user of browser does not see "child_group" as a child of "base_group" in hierarchy subpage
    And user of browser does not see group "child_group" on groups list


  Scenario: User removes parent group
    When user of browser opens group "base_group" hierarchy subpage
    And user of browser clicks show parent groups in hierarchy subpage
    And user of browser clicks on group "parent_group" menu button in hierarchy subpage
    And user of browser clicks on "Remove" in group hierarchy menu
    And user of browser clicks on "Remove" button in modal "REMOVE GROUP"
    Then user of browser does not see "parent_group" as a parent of "base_group" in hierarchy subpage
    And user of browser does not see group "parent_group" on groups list


  Scenario: User removes relation with child group
    When user of browser opens group "parent_group" hierarchy subpage
    And user of browser clicks on group "base_group" menu button to parent relation in hierarchy subpage
    And user of browser clicks on "Remove relation" in relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser does not see "base_group" as a child of "parent_group" in hierarchy subpage


  Scenario: User removes relation with parent group
    When user of browser opens group "base_group" hierarchy subpage
    And user of browser clicks show parent groups in hierarchy subpage
    And user of browser clicks on group "parent_group" menu button to child relation in hierarchy subpage
    And user of browser clicks on "Remove relation" in relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser does not see "parent_group" as a parent of "base_group" in hierarchy subpage


  Scenario Outline: User opens <group_B> page from <group_A> hierarchy subpage using group menu popup
    When user of browser opens group "<group_A>" hierarchy subpage
    And user of browser clicks on group "<group_B>" menu button in hierarchy subpage
    And user of browser clicks on "View group" in group hierarchy menu
    Then user of browser sees "<group_B>" group members subpage

    Examples:
    | group_A      | group_B     |
    | base_group   | base_group  |
    | parent_group | base_group  |
