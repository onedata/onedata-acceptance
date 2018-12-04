Feature: Basic management of groups hierarchy with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            groups:
              - group2

          group2:
            owner: user1
            groups:
              - group3

          group3:
            owner: user1


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User adds newly created children group
    When user of browser goes to group "group1" hierarchy subpage
    And user of browser clicks on group "group1" menu button in hierarchy subpage
    And user of browser clicks on "Add child group" in group hierarchy menu
    And user of browser clicks on "Create new group" in group hierarchy menu
    And user of browser writes "group4" into group name text field in create group modal
    And user of browser clicks on button "Create" in modal "CREATE GROUP"
    Then user of browser sees "group4" as a child of "group1" in hierarchy subpage


  Scenario: User adds newly created parent group
    When user of browser goes to group "group1" hierarchy subpage
    And user of browser clicks on group "group1" menu button in hierarchy subpage
    And user of browser clicks on "Add parent group" in group hierarchy menu
    And user of browser clicks on "Create new group" in group hierarchy menu
    And user of browser writes "group4" into group name text field in create group modal
    And user of browser clicks on button "Create" in modal "CREATE GROUP"
    And user of browser clicks show parent groups in hierarchy subpage
    Then user of browser sees "group4" as a parent of "group1" in hierarchy subpage


  Scenario: User removes child group
    When user of browser goes to group "group2" hierarchy subpage
    And user of browser clicks on group "group3" menu button in hierarchy subpage
    And user of browser clicks on "Remove" in group hierarchy menu
    And user of browser clicks on button "Remove" in modal "REMOVE GROUP"
    Then user of browser does not see "group3" as a child of "group2" in hierarchy subpage
    And user of browser does not see group "group3" on groups list


  Scenario: User removes parent group
    When user of browser goes to group "group2" hierarchy subpage
    And user of browser clicks show parent groups in hierarchy subpage
    And user of browser clicks on group "group1" menu button in hierarchy subpage
    And user of browser clicks on "Remove" in group hierarchy menu
    And user of browser clicks on button "Remove" in modal "REMOVE GROUP"
    Then user of browser does not see "group1" as a parent of "group2" in hierarchy subpage
    And user of browser does not see group "group1" on groups list


  Scenario: User removes relation with child group
    When user of browser goes to group "group1" hierarchy subpage
    And user of browser clicks on group "group2" menu button to parent relation in hierarchy subpage
    And user of browser clicks on "Remove relation" in relation menu
    And user of browser clicks on button "Remove" in modal "REMOVE SUBGROUP"
    Then user of browser does not see "group2" as a child of "group1" in hierarchy subpage


  Scenario: User removes relation with parent group
    When user of browser goes to group "group2" hierarchy subpage
    And user of browser clicks show parent groups in hierarchy subpage
    And user of browser clicks on group "group1" menu button to child relation in hierarchy subpage
    And user of browser clicks on "Remove relation" in relation menu
    And user of browser clicks on button "Remove" in modal "REMOVE SUBGROUP"
    Then user of browser does not see "group1" as a parent of "group2" in hierarchy subpage

