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
    And directory tree structure on local file system:
          browser:
            large_file.txt:
              size: 50 MiB


  Scenario: User executes inout workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Ended in the navigation bar
    And user of browser chooses "Revision1" in workflows revision list of "Workflow1" in inventory workflows subpage
    And user of browser adds "File1" file as input of workflow
#    And user of browser confirms clicks Run workflow button
#
#    Then user of browser waits for all workflows to start
#    And user of browser waits for all workflows to finish
#    And user of browser sees workflow in ended workflows:
#            name: dir1
#            destination: oneprovider-2
#            username: space-owner-user
#            transferred: 50 MiB
#            type: replication
#            status: completed
#
#    And user of browser expands first transfer record
#    And user of browser sees status in workflow visualizer
#    And user of broswer clicks no parrallel box
#    And user of browser sees Proccessed: 1
#    And user of browser clicks Pods activity




