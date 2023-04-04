Feature: Workflow rerun tests


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: s3
                    size: 10000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees lane run indicators and statuses after rerunning workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "checksum-counting-different-lambdas.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "checksum-counting-different-lambdas", using "file1" as initial value, in "space1" space
    And user of browser awaits for status of "checksum-counting-different-lambdas" workflow to be "Active" maximum of 15 seconds

    And user of browser clicks "Cancel" button on "checksum-counting-different-lambdas" workflow status bar
    And user of browser awaits for status of "checksum-counting-different-lambdas" workflow to be "Cancelled" maximum of 15 seconds
    And user of browser sees that status is "Cancelled" for run "1" for "calculate-checksums" lane in popup that appeared after clicking run indicator
    And user of browser clicks "Rerun all items" option in run menu for "calculate-checksums" lane
    And user of browser awaits for status of "checksum-counting-different-lambdas" workflow to be "Finished" maximum of 30 seconds

    Then user of browser sees that run indicator with "2" number has appeared on run bar for "calculate-checksums" lane
    And user of browser sees that run indicator with "2" number is the only indicator on run bar for "calculate-checksums-lane2" lane
    And user of browser sees that status is "Finished" for run "2" for "calculate-checksums" lane in popup that appeared after clicking run indicator
    And user of browser sees that status is "Finished" for run "2" for "calculate-checksums-lane2" lane in popup that appeared after clicking run indicator
    And user of browser clicks on run indicator with "1" number on run bar for "calculate-checksums" lane
    And user of browser clicks "Rerun all items" option in run menu for "calculate-checksums" lane
    And user of browser awaits for status of "checksum-counting-different-lambdas" workflow to be "Finished" maximum of 30 seconds

    And user of browser sees that run indicator with "3" number has appeared on run bar for "calculate-checksums" lane
    And user of browser sees that origin run number for run "3" of "calculate-checksums" lane is "1"
    And user of browser sees that run indicator with "3" number has appeared on run bar for "calculate-checksums-lane2" lane
    And user of browser sees that status is "Finished" for run "3" for "calculate-checksums" lane in popup that appeared after clicking run indicator
    And user of browser sees that status is "Finished" for run "3" for "calculate-checksums-lane2" lane in popup that appeared after clicking run indicator

