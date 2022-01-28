Feature: Basic management of harvester memberships privileges with groups in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user admin has no harvesters
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User successfully adds group to harvester with add group privilege
    When user of browser2 creates group "group1"

    And user of browser1 creates "harvester18" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester18" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester18" has appeared on the harvesters list in the sidebar

    # fail to add group to harvester
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester18" on the harvesters list in the sidebar
    And user of browser2 adds "group1" group to "harvester18" harvester using available groups dropdown
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester18" harvester:
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True

    Then user of browser2 adds "group1" group to "harvester18" harvester using available groups dropdown
    And user of browser2 sees "group1" group in "harvester18" harvester members groups list

    And user of browser1 removes "harvester18" harvester in Onezone page


  Scenario: User successfully removes group from harvester with remove group privilege
    When user of browser1 creates group "group1"

    And user of browser1 creates "harvester19" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester19" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester19" has appeared on the harvesters list in the sidebar

    # add group to harvester
    Then user of browser1 adds "group1" group to "harvester19" harvester using available groups dropdown

    # fail to remove group from harvester
    And user of browser2 removes "group1" group from "harvester19" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester19" harvester:
          Group management:
            granted: Partially
            privilege subtypes:
              Remove group: True

    # remove group from harvester
    And user of browser2 removes "group1" group from "harvester19" harvester members
    And user of browser2 does not see "group1" group in "harvester19" harvester members groups list

    And user of browser1 removes "harvester19" harvester in Onezone page