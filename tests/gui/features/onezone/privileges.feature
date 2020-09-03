Feature: Management of privileges in onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
          # - user2
    And admin user does not have access to any space
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
          space2:
            owner: admin
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user1
          group3:
            owner: admin
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


#    group-> space, user-> space, space->group, user-> group, harvester-> space, space-> harvester

#  Scenario: User successfully adds group to space
#    When user of browser2 adds "group1" group to "space1" space using available groups dropdown
#    And user of browser2 clicks "group1" group in "space1" space members groups list
#    Then user of browser2 sees following privileges of "group1" group in space members subpage:
#          Space management:
#            granted: Partially
#            privilege subtypes:
#              View space: True
#              Modify space: False
#          Data management:
#            granted: Partially
#            privilege subtypes:
#              Read files: True
#              Write files: True
#              Register files: False
#          Transfer management:
#            granted: Partially
#            privilege subtypes:
#              View transfers: True
#              Schedule replication: False
#
#
#  Scenario: User successfully adds user to space
#    When user of browser2 copies invite token to "space1" space
#    And user of browser2 sends copied token to user of browser1
#    And user of browser1 joins space using received token
#    And user of browser2 clicks "admin" user in "space1" space members users list
#    Then user of browser2 sees following privileges of "admin" user in space members subpage:
#          Space management:
#            granted: Partially
#            privilege subtypes:
#              View space: True
#              Modify space: False
#          Data management:
#            granted: Partially
#            privilege subtypes:
#              Read files: True
#              Write files: True
#              Register files: False
#          Transfer management:
#            granted: Partially
#            privilege subtypes:
#              View transfers: True
#              Schedule replication: False
#  And user of browser1 leaves "space1" space in Onezone page
#
#
#  Scenario: User successfully adds group to group
#    When user of browser2 adds "group1" group to "group2" group using available groups dropdown
#    And user of browser2 clicks "group1" group in "group2" group members groups list
#    Then user of browser2 sees following privileges of "group1" group in group members subpage:
#          Group management:
#            granted: Partially
#            privilege subtypes:
#              View group: True
#              Modify group: False
#          User management:
#            granted: False


#  Scenario: User successfully adds user to group
#    When using web gui, browser2 invites browser1 to group "group2" in "onezone" Onezone service
#    And using web gui, browser1 joins group he was invited to in "onezone" Onezone service
#    And user of browser2 clicks "admin" user in "group2" group members users list
#
#    Then user of browser2 sees following privileges of "admin" user in group members subpage:
#          Group management:
#            granted: Partially
#            privilege subtypes:
#              View group: True
#              Modify group: False
#          User management:
#            granted: False
#
#    And user of browser1 leaves group "group2"

  # user to group

#?? group user to harvester?
#  robię usera i group do harvestera
#ok, sprawdzę users po dodaniu harvestera do space


#  Scenario: User successfully adds harvester to space
#    Given user admin has no harvesters
#    And using REST, user admin creates "harvester1" harvester in "onezone" Onezone service
#    When user of browser1 clicks "space2" on the spaces list in the sidebar
#    And user of browser1 adds "harvester1" harvester to "space2" space using available harvesters dropdown
#
#    And user of browser1 sees "harvester1" in harvesters list on space harvesters subpage
##   click? on harvester?
##    new step? privileges on discovery pagr??
#
#    And user of browser1 removes "harvester1" harvester in Onezone page


  Scenario: User successfully adds user to harvester
    Given user admin has no harvesters
    And using REST, user admin creates "harvester2" harvester in "onezone" Onezone service

    When user of browser1 sends invitation token from "harvester2" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page

    Then user of browser1 sees following privileges of "user1" user in harvester members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View group: True
              Modify group: False
          User management:
            granted: False

    And user of browser1 removes "harvester1" harvester in Onezone page


  Scenario: User successfully adds group to harveser
    Given user admin has no harvesters
    And using REST, user admin creates "harvester3" harvester in "onezone" Onezone service

    When user of browser1 adds "group3" group to "harvester3" harvester using available groups dropdown
#    And user of browser2 clicks "group1" group in "group2" group members groups list

  # to jużnie? usunąć?
  ##################################################################################

#  Scenario: User successfully adds space to harvester
#    Given user admin has no harvesters
#    And using REST, user admin creates "harvester1" harvester in "onezone" Onezone service
#
#    Then user of browser1 clicks on Discovery in the main menu
#    And user of browser1 clicks "harvester1" on the harvesters list in the sidebar
#    And user of browser1 clicks Spaces of "harvester1" harvester in the sidebar
#    And user of browser1 clicks add one of your spaces button in harvester spaces page
#    And user of browser1 sees that "Add one of your spaces" modal has appeared
#    And user of browser1 chooses "space2" from dropdown in add space modal
#    And user of browser1 clicks on "Add" button in modal "Add one of spaces"
#
#    And user of browser1 sees that "space2" has appeared on the spaces list in discovery page
#
#    Then user of browser2 sees following privileges of "space2" user in harvester members subpage:
#          Group management:
#            granted: Partially
#            privilege subtypes:
#              View group: True
#              Modify group: False
#          User management:
#            granted: False
#
#    And user of browser1 removes "harvester1" harvester in Onezone page
