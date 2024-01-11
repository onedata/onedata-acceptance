Feature: Basic management of harvester memberships privileges in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user admin has no harvesters
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User fails to see harvester without view harvester privilege
    Given initial spaces configuration in "onezone" Onezone service:
            space1:
              owner: admin
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
    And user admin has "harvester11" harvester in "onezone" Onezone service
    When using REST, user admin adds space "space1" to "harvester11" harvester
    And user of browser1 sends invitation token from "harvester11" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester11" has appeared on the harvesters list in the sidebar

    # check view harvester privilege
    And user of browser1 sets following privileges for "user1" user in "harvester11" harvester:
          Harvester management:
            granted: Partially
            privilege subtypes:
              View harvester: False

    And user of browser2 refreshes site
    And user of browser2 clicks Members of "harvester11" harvester in the sidebar
    Then user of browser2 sees "Insufficient privileges" alert in harvester members subpage
    And user of browser2 clicks Spaces of "harvester11" harvester in the sidebar
    And user of browser2 sees Insufficient privileges alert on Spaces subpage
    And user of browser2 clicks Indices of "harvester11" harvester in the sidebar
    And user of browser2 sees Insufficient privileges alert on Indices subpage
    And user of browser2 clicks Data discovery of "harvester11" harvester in the sidebar
    And user of browser2 sees "This resource could not be loaded." alert on empty Data discovery page

    And user of browser1 removes "harvester11" harvester in Onezone page


  Scenario: User successfully renames harvester with modify harvester privilege
    When user of browser1 creates "harvester12" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester12" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester12" has appeared on the harvesters list in the sidebar

    And user of browser2 renames "harvester12" harvester to "harvester123" in Onezone page
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester12" harvester:
          Harvester management:
            granted: Partially
            privilege subtypes:
              Modify harvester: True
    Then user of browser2 refreshes site
    And user of browser2 renames "harvester12" harvester to "harvester123" in Onezone page
    And user of browser1 removes "harvester123" harvester in Onezone page


  Scenario: User successfully removes harvester with remove harvester privilege
    When user of browser1 creates "harvester13" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester13" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester13" has appeared on the harvesters list in the sidebar

    And user of browser2 removes "harvester13" harvester in Onezone page
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester13" harvester:
          Harvester management:
            granted: Partially
            privilege subtypes:
              Remove harvester: True

    And user of browser2 removes "harvester13" harvester in Onezone page
    And user of browser2 sees that "harvester13" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully views privileges with view privileges privilege
    When user of browser1 creates "harvester14" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester14" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester14" has appeared on the harvesters list in the sidebar

    # fail to view privileges
    And user of browser2 clicks Members of "harvester14" harvester in the sidebar
    And user of browser2 clicks "admin" user in "harvester14" harvester members users list
    And user of browser2 sees "Insufficient privileges" alert in harvester members subpage

    And user of browser1 sets following privileges for "user1" user in "harvester14" harvester:
          Harvester management:
            granted: Partially
            privilege subtypes:
              View privileges: True

    # view privileges
    And user of browser2 clicks "user1" user in "harvester14" harvester members users list
    Then user of browser2 sees privileges for "user1" user in harvester members subpage

    And user of browser1 removes "harvester14" harvester in Onezone page


  Scenario: User successfully sets privileges with set privileges privilege
    When user of browser1 creates "harvester15" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester15" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester15" has appeared on the harvesters list in the sidebar

    And user of browser2 sets following privileges for "user1" user in "harvester15" harvester:
          Harvester management:
            granted: True
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 sets following privileges for "user1" user in "harvester15" harvester:
          Harvester management:
            granted: Partially
            privilege subtypes:
              Set privileges: True
    And user of browser2 refreshes site
    Then user of browser2 sets following privileges for "user1" user in "harvester15" harvester:
          Harvester management:
            granted: True
    And user of browser1 clicks "user1" user in "harvester15" harvester members users list
    And user of browser1 sees following privileges of "user1" user in harvester members subpage:
          Harvester management:
            granted: True

    And user of browser1 removes "harvester15" harvester in Onezone page





