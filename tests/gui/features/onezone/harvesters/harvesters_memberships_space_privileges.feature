Feature: Basic management of harvester memberships privileges with spaces in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user admin has no harvesters
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User successfully adds space with add space privilege
    Given admin user does not have access to any space
    When user of browser2 creates "space1" space in Onezone

    And user of browser1 creates "harvester20" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester20" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester20" has appeared on the harvesters list in the sidebar

    # fail to add space
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 adds "space1" space to "harvester20" harvester using available spaces dropdown
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester20" harvester:
          Space management:
            granted: Partially
            privilege subtypes:
              Add space: True
    And user of browser2 adds "space1" space to "harvester20" harvester using available spaces dropdown

    Then user of browser2 sees that "space1" has appeared on the spaces list in discovery page
    And user of browser1 removes "harvester20" harvester in Onezone page


  Scenario: User successfully removes space with remove space privilege
    Given admin user does not have access to any space
    When user of browser1 creates "space2" space in Onezone
    And user of browser1 creates "harvester21" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester21" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester21" has appeared on the harvesters list in the sidebar
    And user of browser1 adds "space2" space to "harvester21" harvester using available spaces dropdown

    # fail to remove space from harvester
    And user of browser2 clicks Spaces of "harvester21" harvester in the sidebar
    And user of browser2 removes "space2" space from harvester
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester21" harvester:
          Space management:
            granted: Partially
            privilege subtypes:
              Remove space: True
    Then user of browser2 removes "space2" space from harvester
    And user of browser1 removes "harvester21" harvester in Onezone page
    And user of browser1 leaves "space2" space in Onezone page
