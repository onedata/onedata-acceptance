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


  Scenario: User successfully renames inventory with modify inventory privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    #User1 fails to rename inventory
    And user of browser1 clicks on "Rename" button in inventory "inventory1" menu in the sidebar
    And user of browser1 writes "inventory2" into rename inventory text field
    And user of browser1 confirms inventory rename with confirmation button
    And user of browser1 sees that error popup has appeared
    And user of browser1 clicks on "Close" button in modal "Error"

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
          Inventory management:
            granted: Partially
            privilege subtypes:
              Modify inventory: True

    # User1 renames inventory
    And user of browser1 confirms inventory rename with confirmation button
    Then user of browser1 sees inventory "inventory2" on inventory list
    And user of space_owner_browser sees inventory "inventory2" on inventory list


  Scenario: User successfully removes inventory with modify inventory privilege
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
              Remove inventory: True

    # User1 removes inventory
    And user of browser1 clicks on "Remove" button in inventory "inventory1" menu in the sidebar
    And user of browser1 clicks on "Remove" button in modal "Remove inventory"
    Then user of browser1 does not see inventory "inventory1" on inventory list
    And user of space_owner_browser does not see inventory "inventory1" on inventory list


  Scenario: User successfully views privileges with view privileges privilege
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
              View privileges: True

    # User1 views privileges
    And user of browser1 opens inventory "inventory1" members subpage
    And user of browser1 clicks "group1" group in "inventory1" automation members groups list
    Then user of browser1 sees privileges for "group1" group in automation members subpage


  Scenario: User successfully sets privileges with set privileges privilege
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
              View privileges: True
              Set privileges: True

    # User1 sets privileges
    And user of browser1 opens inventory "inventory1" members subpage
    And user of browser1 clicks "group1" group in "inventory1" automation members groups list
    Then user of browser1 sets following privileges for "group1" group in automation members subpage:
          Inventory management:
            granted: Partially
            privilege subtypes:
              Remove inventory: True


  Scenario: User successfully generates invitation token for user with add user privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    #User1 fails to generate an ivnitation token
    And user of browser1 opens inventory "inventory1" members subpage
    And user of browser1 clicks on "Invite user using token" button in users list menu in "inventory1" automation members view
    And user of browser1 sees This resource could not be loaded alert in Invite user using token modal
    And user of browser1 closes "Invite using token" modal

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
         User management:
            granted: Partially
            privilege subtypes:
              Add user: True

    And user of browser1 opens inventory "inventory1" members subpage
    Then user of browser1 clicks on "Invite user using token" button in users list menu in "inventory1" automation members view


  Scenario: User successfully removes user from inventory with remove user privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    # User1 fails to remove user
    And user of browser1 removes "space-owner-user" user from "inventory1" automation members
    And user of browser1 sees that error popup has appeared
    And user of browser1 clicks on "Close" button in modal "Error"

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
         User management:
            granted: Partially
            privilege subtypes:
              Remove user: True

    And user of browser1 opens inventory "inventory1" members subpage

    #User1 removes space-owner-user from inventory and space-owner can not view inventory1
    Then user of browser1 removes "space-owner-user" user from "inventory1" automation members
    And user of space_owner_browser does not see inventory "inventory1" on inventory list


  Scenario: User successfully adds group to inventory with add group privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

    #User1 fails to generate an ivnitation token
    And user of browser1 opens inventory "inventory1" members subpage
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of browser1 sees This resource could not be loaded alert in Invite user using token modal
    And user of browser1 closes "Invite using token" modal

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
         Group management:
            granted: Partially
            privilege subtypes:
              Add group: True

    Then user of browser1 clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view


  Scenario: User successfully removes group to inventory with add group privilege
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    When user of space_owner_browser clicks on Automation in the main menu

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds group1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to inventory using copied token

#    # User1 fails to remove group
#    And user of browser1 removes "group1" group from "inventory1" automation members
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"

    # Space-owner-user changes privileges for group1
    And user of space_owner_browser clicks "group1" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
         Group management:
            granted: Partially
            privilege subtypes:
              Remove group: True

    And user of browser1 opens inventory "inventory1" members subpage

    #User1 removes group from inventory
    Then user of browser1 removes "group1" group from "inventory1" automation members
