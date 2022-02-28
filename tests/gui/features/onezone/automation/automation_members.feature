Feature: Management of inventories members


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: space-owner-user
            users:
                - user1
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
            users:
              - user1
            groups:
              - group2
        inventory2:
            owner: space-owner-user
            users:
              - user1
        inventory3:
            owner: space-owner-user

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


#  Scenario: User invites group to inventory using token
#    When user of space_owner_browser clicks on Automation in the main menu
#
#    # Space-owner-user generates invitation token
#    And user of space_owner_browser opens inventory "inventory3" members subpage
#    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory3" automation members view
#    And user of space_owner_browser copies invitation token from modal
#    And user of space_owner_browser closes "Invite using token" modal
#
#    # Space-owner-user adds group1 to view inventory
#    And user of space_owner_browser sends copied token to user of browser1
#    And user of browser1 adds group "group1" to inventory using copied token
#    Then user of browser1 sees inventory "inventory3" on inventory list
#
#
#  Scenario: User joins an inventory with group invitation token and sees renamed inventory
#    When user of space_owner_browser clicks on Automation in the main menu
#
#    # Space-owner-user generates invitation token
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
#    And user of space_owner_browser copies invitation token from modal
#    And user of space_owner_browser closes "Invite using token" modal
#
#    # Space-owner-user adds group1 to view inventory
#    And user of space_owner_browser sends copied token to user of browser1
#    And user of browser1 adds group "group1" to inventory using copied token
#
#    # Space-owner-user renames inventory
#    And user of space_owner_browser clicks on "Rename" button in inventory "inventory1" menu in the sidebar
#    And user of space_owner_browser writes "renamed_inventory1" into rename inventory text field
#    And user of space_owner_browser confirms inventory rename with confirmation button
#
#    # User1 sees inventory has different name
#    Then user of browser1 sees inventory "renamed_inventory1" on inventory list
#
#
#  Scenario: User fails to see inventory without view inventory privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory2" members subpage
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory2" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View inventory: False
#
#    # User1 can not view inventory1 content
#    And user of browser1 opens inventory "inventory2" main subpage
#    Then user of browser1 sees "Insufficient privileges to access this resource" label in "inventory2" main page
#
#
#  Scenario: User successfully renames inventory with modify inventory privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to rename inventory
#    And user of browser1 clicks on "Rename" button in inventory "inventory1" menu in the sidebar
#    And user of browser1 writes "renamed_inventory" into rename inventory text field
#    And user of browser1 confirms inventory rename with confirmation button
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              Modify inventory: True
#
#    # User1 renames inventory
#    And user of browser1 confirms inventory rename with confirmation button
#    Then user of browser1 sees inventory "renamed_inventory" on inventory list
#    And user of space_owner_browser sees inventory "renamed_inventory" on inventory list
#
#
#  Scenario: User successfully removes inventory with remove inventory privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              Remove inventory: True
#
#    # User1 removes inventory
#    And user of browser1 clicks on "Remove" button in inventory "inventory1" menu in the sidebar
#    And user of browser1 clicks on "Remove" button in modal "Remove inventory"
#    Then user of browser1 does not see inventory "inventory1" on inventory list
#    And user of space_owner_browser does not see inventory "inventory1" on inventory list
#
#
#  Scenario: User successfully views privileges with view privileges privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View privileges: True
#
#    # User1 views privileges
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks "user1" user in "inventory1" automation members users list
#    Then user of browser1 sees privileges for "user1" user in automation members subpage
#
#
#  Scenario: User successfully sets privileges with set privileges privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View privileges: True
#              Set privileges: True
#
#    # User1 sets privileges
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks "user1" user in "inventory1" automation members users list
#    And user of browser1 sets following privileges for "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View privileges: True
#              Set privileges: False
#
#    And user of browser1 clicks "user1" user in "inventory1" automation members users list
#    Then user of browser1 sees following privileges of "user1" user in automation members subpage:
#          Inventory management:
#            granted: Partially
#            privilege subtypes:
#              View privileges: True
#              Set privileges: False
#
#
#  Scenario: User successfully generates invitation token for user with add user privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to generate an ivnitation token
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks on "Invite user using token" button in users list menu in "inventory1" automation members view
#    And user of browser1 sees This resource could not be loaded alert in Invite user using token modal
#    And user of browser1 closes "Invite using token" modal
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#         User management:
#            granted: Partially
#            privilege subtypes:
#              Add user: True
#
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks on "Invite user using token" button in users list menu in "inventory1" automation members view
#    And user of browser1 sees that "Invite user using token" modal has appeared
#    Then user of browser1 copies invitation token from modal
#
#
#  Scenario: User successfully removes user from inventory with remove user privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory2" members subpage
#
#    # User1 fails to remove user
#    And user of browser1 removes "space-owner-user" user from "inventory2" automation members
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory2" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#         User management:
#            granted: Partially
#            privilege subtypes:
#              Remove user: True
#
#    And user of browser1 opens inventory "inventory2" members subpage
#
#    # User1 removes space-owner-user from inventory and space-owner can not view inventory1
#    Then user of browser1 removes "space-owner-user" user from "inventory2" automation members
#    And user of space_owner_browser does not see inventory "inventory2" on inventory list
#
#
#  Scenario: User successfully generates invitation token for group to join inventory with add group privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to generate an ivnitation token
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
#    And user of browser1 sees This resource could not be loaded alert in Invite user using token modal
#    And user of browser1 closes "Invite using token" modal
#
#    # Space-owner-user changes privileges for user1
#    And user of space_owner_browser clicks "user1" user in "inventory1" automation members users list
#    And user of space_owner_browser sets following privileges for "user1" user in automation members subpage:
#         Group management:
#            granted: Partially
#            privilege subtypes:
#              Add group: True
#
#    And user of browser1 clicks on "Invite group using token" button in groups list menu in "inventory1" automation members view
#    Then user of browser1 copies invitation token from modal
#
#
#  Scenario: User successfully removes group from inventory with remove group privilege
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to remove group
#    And user of browser1 removes "group2" group from "inventory1" automation members
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"
#
#    # Space-owner-user changes privileges for group2
#    And user of space_owner_browser clicks "group2" group in "inventory1" automation members groups list
#    And user of space_owner_browser sets following privileges for "group2" group in automation members subpage:
#         Group management:
#            granted: Partially
#            privilege subtypes:
#              Remove group: True
#
#    # User1 removes group from inventory
#    And user of browser1 removes "group2" group from "inventory1" automation members
#    Then user of browser1 does not see group "group2" on groups list
#
#
#  Scenario: User successfully manages lambda with menage lambda privilege
#    # Space-owner-user creates a lambda
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" lambdas subpage
#    And user of space_owner_browser uses Add new lambda button from menu bar
#    And user of space_owner_browser writes "Lambda1" into lambda name text field
#    And user of space_owner_browser writes "docker_image_example" into docker image text field
#    And user of space_owner_browser confirms create new lambda using Create button
#    And user of space_owner_browser sees "Lambda1" in lambdas list in inventory lambdas subpage
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to add new revision
#    And user of browser1 clicks on Automation in the main menu
#    And user of browser1 opens inventory "inventory1" members subpage
#    And user of browser1 clicks on Create new revision in "Lambda1"
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"
#
#    # Space-owner-user changes privileges for group2
#    And user of space_owner_browser clicks "group2" group in "inventory1" automation members groups list
#    And user of space_owner_browser sets following privileges for "group2" group in automation members subpage:
#         Schema management:
#            granted: Partially
#            privilege subtypes:
#              Manage lambdas: True
#
#
#    # User1 adds new revision
#    And user of browser1 clicks on Create new revision in "Lambda1"
#    And user of browser1 writes "Lambda2" into lambda name text field
#    And user of browser1 confirms create new revision using Create button
#    Then user of browser1 sees "Lambda2" in lambdas revision list of "Lambda2" in inventory lambdas subpage

#  Scenario: User successfully manages lambda with menage lambda privilege
#    # Space-owner-user creates a lambda
#    When user of space_owner_browser clicks on Automation in the main menu
#    And user of space_owner_browser opens inventory "inventory1" lambdas subpage
#    And user of space_owner_browser uses Add new lambda button from menu bar
#    And user of space_owner_browser writes "Lambda1" into lambda name text field
#    And user of space_owner_browser writes "docker_image_example" into docker image text field
#    And user of space_owner_browser confirms create new lambda using Create button
#    And user of space_owner_browser sees "Lambda1" in lambdas list in inventory lambdas subpage
#    And user of space_owner_browser opens inventory "inventory1" members subpage
#
#    # User1 fails to add new revision
#    And user of browser1 clicks on Automation in the main menu
#    And user of browser1 opens inventory "inventory1" lambdas subpage
#    And user of browser1 clicks on Create new revision in "Lambda1"
#    And user of browser1 writes "Lambda2" into lambda name text field
#    And user of browser1 confirms create new revision using Create button
#    And user of browser1 sees that error popup has appeared
#    And user of browser1 clicks on "Close" button in modal "Error"
#
#    # Space-owner-user changes privileges for group2
#    And user of space_owner_browser clicks "group2" group in "inventory1" automation members groups list
#    And user of space_owner_browser sets following privileges for "group2" group in automation members subpage:
#         Schema management:
#            granted: Partially
#            privilege subtypes:
#              Manage lambdas: True
#
#
#    # User1 adds new revision
#    And user of browser1 opens inventory "inventory1" lambdas subpage
#    And user of browser1 uses Add new lambda button from menu bar
#    And user of browser1 writes "Lambda1" into lambda name text field
#    And user of browser1 writes "docker_image_example" into docker image text field
#    And user of browser1 confirms create new lambda using Create button
#    Then user of browser1 sees "Lambda1" in lambdas list in inventory lambdas subpage


  Scenario: User successfully manages workflow with menage workflows schema privilege
    # Space-owner-user uploads workflow
    When user of space_owner_browser clicks on Automation in the main menu
    And user of space_owner_browser opens inventory "inventory1" workflows subpage
    And user of space_owner_browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of space_owner_browser clicks on "Apply" button in modal "Upload workflow"
    And user of space_owner_browser opens inventory "inventory1" workflows subpage
    And user of space_owner_browser sees "Workflow1" in workflows list in inventory workflows subpage
    And user of space_owner_browser opens inventory "inventory1" members subpage

    # User1 fails to edit worflow name
    And user of browser1 clicks on Automation in the main menu
    And user of browser1 opens inventory "inventory1" workflows subpage
    And user of browser clicks on "Change details" button in workflow "Workflow1" menu in workflows subpage
    And user of browser writes "Workflow Renamed" in name textfield of selected workflow
    And user of browser confirms edition of selected workflow details using Save button
    And user of browser1 sees that error popup has appeared
    And user of browser1 clicks on "Close" button in modal "Error"

    # Space-owner-user changes privileges for group2
    And user of space_owner_browser clicks "group2" group in "inventory1" automation members groups list
    And user of space_owner_browser sets following privileges for "group2" group in automation members subpage:
         Schema management:
            granted: Partially
            privilege subtypes:
              Manage workflows schemas: True


    # User1 sees edited workflow
    And user of browser clicks on "Change details" button in workflow "Workflow1" menu in workflows subpage
    And user of browser writes "Workflow Renamed" in name textfield of selected workflow
    And user of browser confirms edition of selected workflow details using Save button
    Then user of browser sees "Workflow Renamed" in workflows list in inventory workflows subpage


