Feature: Management of inventories members


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User invites group to inventory using token
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token
    Then user of browser1 sees inventory "inventory1" on inventory list


  Scenario: User joins an inventory with group invitation token and sees renamed inventory
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    # Space-owner-user renames inventory
    And user of space_owner_browser clicks on "Rename" button in inventory "inventory1" menu in the sidebar
    And user of space_owner_browser writes "inventory2" into rename inventory text field
    And user of space_owner_browser confirms inventory rename with confirmation button

    # User1 sees inventory has different name
    Then user of browser1 sees inventory "inventory2" on inventory list


  Scenario: User fails to see inventory without view inventory privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
          Inventory management:
            granted: Partially
            privilege subtypes:
              View inventory: False

    # User1 can not view inventory1 content
    Then user of browser1 sees "Insufficient privileges to access this resource" label in "inventory1" main page