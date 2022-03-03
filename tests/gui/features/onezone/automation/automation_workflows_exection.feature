Feature: Workflows execution


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees that new workflow has been added after uploading it as json file
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Run workflow button
    And user of browser chooses "Revision1" in workflows revision list of "Workflow1" in inventory workflows subpage


