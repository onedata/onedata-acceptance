Feature: Basic management of harvester in Space


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
              space1:
                owner: user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And users of [browser1, browser2] logged as [user1 ,admin] to [Onezone, Onezone] service


  Scenario: User adds two harvesters to space using invitation tokens and removes them from it
    When user of browser2 creates "harvester2" harvester in Onezone page
    And user of browser2 creates "harvester3" harvester in Onezone page
    And user of browser1 clicks Harvesters of "space1" in the sidebar

    And user of browser1 clicks invite harvester using token button in space harvesters page
    And user of browser1 copies invitation token from modal
    And user of browser1 sends copied token to user of browser2
    And user of browser1 clicks on "Close" button in modal "Invite using token"
    And user of browser2 adds harvester "harvester2" to space using copied token

    And user of browser1 clicks on "Invite harvester using token" button in space menu
    And user of browser1 copies invitation token from modal
    And user of browser1 sends copied token to user of browser2
    And user of browser1 clicks on "Close" button in modal "Invite using token"
    And user of browser2 adds harvester "harvester3" to space using copied token

    Then user of browser1 sees "harvester2" in harvesters list on space harvesters subpage
    And user of browser1 sees "harvester3" in harvesters list on space harvesters subpage

    And user of browser1 removes "harvester2" harvester from "space1" space
    And user of browser1 does not see "harvester2" in harvesters list on space harvesters subpage

    And user of browser1 removes "harvester3" harvester from "space1" space
    And user of browser1 does not see "harvester3" in harvesters list on space harvesters subpage


  Scenario: User adds one of his harvesters to space and another user deletes this harvester
    Given user admin has no harvesters
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser2 creates "harvester1" harvester in Onezone page
    And user of browser2 sends invitation token from "harvester1" harvester to user of browser1
    And user of browser1 joins to harvester in Onezone page

    And user of browser2 sets following privileges for "user1" user in "harvester1" harvester:
          Space management:
            granted: Partially
            privilege subtypes:
              Add space: True

    And user of browser1 adds "harvester1" harvester to "space1" space using available harvesters dropdown
    Then user of browser1 sees "harvester1" in harvesters list on space harvesters subpage
    And user of browser2 removes "harvester1" harvester in Onezone page
    And user of browser1 does not see "harvester1" in harvesters list on space harvesters subpage
