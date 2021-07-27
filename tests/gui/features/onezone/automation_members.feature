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


    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service



#  Scenario: User invites group to inventory using token
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser clicks on Create automation inventory button in automation sidebar
#    And user of space_owner_browser writes "inventory1" into inventory name text field
#    And user of space_owner_browser clicks on confirmation button on automation page
#
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
#    And user of space_owner_browser copies invitation token from modal
#    And user of space_owner_browser closes "Invite using token" modal
#
#    And user of space_owner_browser sends copied token to user of browser1
#    And user of browser1 adds group "group1" to space using copied token
#    Then user of browser1 sees inventory "inventory1" on inventory list
#
#
#  Scenario: User joins an inventory with group invitation token and see inventory was renamed
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser clicks on Create automation inventory button in automation sidebar
#    And user of space_owner_browser writes "inventory1" into inventory name text field
#    And user of space_owner_browser clicks on confirmation button on automation page
#
#    # Space-owner-user generates invitation token
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
#    And user of space_owner_browser copies invitation token from modal
#    And user of space_owner_browser closes "Invite using token" modal
#
#    # Space-owner-user adds user1 to view inventory
#    And user of space_owner_browser sends copied token to user of browser1
#    And user of browser1 adds group "group1" to space using copied token
#
#    # Space-owner-user renames inventory
#    And user of space_owner_browser clicks on "Rename" button in inventory "inventory1" menu in the sidebar
#    And user of space_owner_browser writes "inventory2" into rename inventory text field
#    And user of space_owner_browser confirms inventory rename using <confirmation_method>
#
#     # User1 sees inventory has different name
#    And user of space_owner_browser is idle for 4 seconds
#    Then user of browser1 sees inventory "inventory2" on inventory list


  Scenario: User fails to see inventory without view inventory privilege
    When user of space_owner_browser clicks on Automation in the main menu
    And user of space_owner_browser clicks on Create automation inventory button in automation sidebar
    And user of space_owner_browser writes "inventory1" into inventory name text field
    And user of space_owner_browser clicks on confirmation button on automation page

    # Space-owner-user generates invitation token
    And user of space_owner_browser opens inventory "inventory1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    # Space-owner-user adds user1 to view inventory
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group1" to space using copied token

    And user of space_owner_browser opens inventory "inventory1" members subpage

   #And user of space_owner_browser sets following privileges for "group1" group in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View inventory: False

#    And user of browser_standard sets following privileges for "user1" user in cluster members subpage:
#          Cluster management:
#            granted: Partially
#            privilege subtypes:
#              View privileges: False
    And user of browser sees following privileges on modal:
          User management:
            granted: False