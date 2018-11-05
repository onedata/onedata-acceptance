Feature: Basic management of groups hierarchy with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User add children group
    When user of browser goes to group "group1" hierarchy subpage
    And user of browser clicks on active group trigger in hierarchy subpage
    And user of browser clicks on "Add child group" in group hierarchy menu
    And user of browser clicks on "Create new group" in group hierarchy menu
    And user of browser writes "group2" into group name text field in create child group modal
    And user of browser confirms create new child group in create child group modal
    Then user of browser sees "group2" as a children of "group1" in hierarchy subpage
