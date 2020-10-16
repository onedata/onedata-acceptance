Feature: Basic management of harvester in Space


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
              space1:
                owner: space-owner-user

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user ,admin] to [Onezone, Onezone] service


  Scenario: User adds two harvesters to space using invitation tokens and removes them from it
    When user of browser1 creates "harvester2" harvester in Onezone page
    And user of browser1 creates "harvester3" harvester in Onezone page
    And user of space_owner_browser clicks Harvesters of "space1" in the sidebar

    # Invite "harvester2" harvester to "space1" space
    And user of space_owner_browser clicks invite harvester using token button in space harvesters page
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser sends copied token to user of browser1
    And user of space_owner_browser clicks on "Close" button in modal "Invite using token"
    And user of browser1 adds harvester "harvester2" to space using copied token

    # Invite "harvester3" harvester to "space1" space
    And user of space_owner_browser clicks on "Invite harvester using token" button in space menu
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser sends copied token to user of browser1
    And user of space_owner_browser clicks on "Close" button in modal "Invite using token"
    And user of browser1 adds harvester "harvester3" to space using copied token

    # See that both harvesters are in "space1" space
    Then user of space_owner_browser sees "harvester2" in harvesters list on space harvesters subpage
    And user of space_owner_browser sees "harvester3" in harvesters list on space harvesters subpage

    And user of space_owner_browser removes "harvester2" harvester from "space1" space
    And user of space_owner_browser does not see "harvester2" in harvesters list on space harvesters subpage

    And user of space_owner_browser removes "harvester3" harvester from "space1" space
    And user of space_owner_browser does not see "harvester3" in harvesters list on space harvesters subpage


  Scenario: User adds one of his harvesters to space and another user deletes this harvester
    Given user admin has no harvesters
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar

    # Create "harvester1" harvester and give user appropriate privileges
    And user of browser1 creates "harvester1" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester1" harvester to user of space_owner_browser
    And user of space_owner_browser joins to harvester in Onezone page

    And user of browser1 sets following privileges for "space-owner-user" user in "harvester1" harvester:
          Space management:
            granted: Partially
            privilege subtypes:
              Add space: True

    And user of space_owner_browser adds "harvester1" harvester to "space1" space using available harvesters dropdown
    Then user of space_owner_browser sees "harvester1" in harvesters list on space harvesters subpage

    And user of browser1 removes "harvester1" harvester in Onezone page
    And user of space_owner_browser does not see "harvester1" in harvesters list on space harvesters subpage
