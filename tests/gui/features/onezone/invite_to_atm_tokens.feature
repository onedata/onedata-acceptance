Feature: Management of invite to atm tokens in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1

    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: admin
          space2:
            owner: user1

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1

    And initial inventories configuration in "onezone" Onezone service:
          inventory1:
              owner: admin

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User has default inventory member privileges after consuming user to automation inventory invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite user to automation inventory
          invite target: inventory1
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite user to automation inventory
          invite target: inventory1
          privileges:
            Inventory management:
              granted: Partially
              privilege subtypes:
                View inventory: True
                Modify inventory: False
                Remove inventory: False
                View privileges: False
                Set privileges: False
            Schema management:
                granted: False
            User management:
                granted: False
            Group management:
                granted: False

    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    And user of browser2 joins inventory using copied token

    Then user of browser2 sees that "inventory1" has appeared on the automation list in the sidebar
    And user of browser2 sees that inventory inventory1 has following privilege configuration for user user1:
          privileges:
            Inventory management:
              granted: Partially
              privilege subtypes:
                View inventory: True
                Modify inventory: False
                Remove inventory: False
                View privileges: False
                Set privileges: False
            Schema management:
                granted: False
            User management:
                granted: False
            Group management:
                granted: False

    And user of browser1 removes all tokens


  Scenario: Group has default inventory member privileges after user consums group to automation inventory invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to automation inventory
          invite target: inventory1
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite group to automation inventory
          invite target: inventory1
          privileges:
            Inventory management:
              granted: Partially
              privilege subtypes:
                View inventory: True
                Modify inventory: False
                Remove inventory: False
                View privileges: False
                Set privileges: False
            Schema management:
                granted: False
            User management:
                granted: False
            Group management:
                granted: False

    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    And user of browser2 succeeds to consume token for "group1" group

    Then user of browser2 sees that "inventory1" has appeared on the automation list in the sidebar
    And user of browser1 sees that inventory inventory1 has following privilege configuration for group group1:
          privileges:
            Inventory management:
              granted: Partially
              privilege subtypes:
                View inventory: True
                Modify inventory: False
                Remove inventory: False
                View privileges: False
                Set privileges: False
            Schema management:
                granted: False
            User management:
                granted: False
            Group management:
                granted: False

    And user of browser1 removes all tokens