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
            owner: user1
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

  Scenario: User successfully adds group to space
    When user of browser2 adds "group1" group to "space1" space using available groups dropdown
    And user of browser2 clicks "group1" group in "space1" space members groups list
    Then user of browser2 sees following privileges of "group1" group in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: True
              Modify space: False
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True
              Write files: True
              Register files: False
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False


  Scenario: User successfully adds user to space
    When user of browser2 copies invite token to "space1" space
    And user of browser2 sends copied token to user of browser1
    And user of browser1 joins space using received token
    And user of browser2 clicks "admin" user in "space1" space members users list
    Then user of browser2 sees following privileges of "admin" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: True
              Modify space: False
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True
              Write files: True
              Register files: False
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False
  And user of browser1 leaves "space1" space in Onezone page


  Scenario: User successfully adds group to group
    When user of browser2 adds "group1" group to "group2" group using available groups dropdown
    And user of browser2 clicks "group1" group in "group2" group members groups list
    Then user of browser2 sees following privileges of "group1" group in group members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View group: True
              Modify group: False
          User management:
            granted: False

# waiting for harvesters update
#  Scenario: User successfully adds space to harvester
#    Given user admin has no harvesters
#    And using REST, user admin creates "harvester1", "harvester" harvester in "onezone" Onezone service
#
#    And user of browser1 removes "harvester1" harvester in Onezone page
##    And user of browser1 removes "harvester2" harvester in Onezone page

#  Scenario: User successfully adds harvester to space
