Feature: Basic management of harvester memberships privileges with users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user admin has no harvesters
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User successfully adds user to harvester
    When user of browser1 creates "harvester10" harvester in Onezone page

    # copy invitation token
    And user of browser1 clicks on Discovery in the main menu
    And user of browser1 clicks "harvester10" on the harvesters list in the sidebar
    And user of browser1 clicks Members of "harvester10" harvester in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "harvester10" harvester members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    # join to harvester
    And user of browser2 joins to harvester in Onezone page
    Then user of browser2 sees that "harvester10" has appeared on the harvesters list in the sidebar
    And user of browser1 removes "harvester10" harvester in Onezone page


  Scenario: User successfully generates invitation token for user with add user privilege
    When user of browser1 creates "harvester16" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester16" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester16" has appeared on the harvesters list in the sidebar

    # fail to generate invitation token for user
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester16" on the harvesters list in the sidebar
    And user of browser2 clicks Members of "harvester16" harvester in the sidebar
    And user of browser2 clicks on "Invite user using token" button in users list menu in "harvester16" harvester members view
    And user of browser2 sees This resource could not be loaded alert in Invite user using token modal
    And user of browser2 closes "Invite using token" modal

    And user of browser1 sets following privileges for "user1" user in "harvester16" harvester:
          User management:
            granted: Partially
            privilege subtypes:
              Add user: True

    # generate invitation token for user
    Then user of browser2 clicks on "Invite user using token" button in users list menu in "harvester16" harvester members view
    And user of browser2 sees non-empty token in token area

    And user of browser1 removes "harvester16" harvester in Onezone page


  Scenario: User successfully removes user from harvester with remove user privilege
    When user of browser1 creates "harvester17" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester17" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester17" has appeared on the harvesters list in the sidebar

    # fail to remove user
    And user of browser2 removes "admin" user from "harvester17" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester17" harvester:
          User management:
            granted: Partially
            privilege subtypes:
              Remove user: True

    # remove user
    Then user of browser2 removes "admin" user from "harvester17" harvester members
    And user of browser1 sees that "harvester17" has disappeared on the harvesters list in the sidebar


