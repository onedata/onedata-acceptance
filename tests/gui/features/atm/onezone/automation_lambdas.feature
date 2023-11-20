Feature: Basic lambdas management


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


  Scenario: User sees new lambda after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses "Add new lambda" button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker.onedata.org/lambda-echo" into docker image text field
    And user of browser confirms creating new lambda using "Create" button
    Then user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage


  Scenario: User sees new lambda revision after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses "Add new lambda" button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker.onedata.org/lambda-echo" into docker image text field
    And user of browser confirms creating new lambda using "Create" button
    And user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage
    And user of browser clicks on "Create new revision" in "Lambda1"
    And user of browser writes "Lambda2" into lambda name text field
    And user of browser confirms creating new revision using "Create" button
    Then user of browser sees that 2nd revision of "Lambda2" lambda is described "Lambda2"


  Scenario: User sees new lambda revision after using redesign as new revision
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses "Add new lambda" button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker.onedata.org/lambda-echo" into docker image text field
    And user of browser confirms creating new lambda using "Create" buttonn
    And user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage
    And user of browser clicks on "Redesign as new revision" button from 1st revision of "Lambda1" lambda menu
    And user of browser writes "Lambda2" into lambda name text field
    And user of browser confirms creating new revision using "Create" button
    Then user of browser sees that 2nd revision of "Lambda2" lambda is described "Lambda2"


  Scenario: User does not see new lambda after upload again the same workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory
    And user of browser sees there are 7 lambdas in lambdas list in inventory lambdas subpage
    And user of browser uploads "bagit-uploader" workflow as new workflow from automation-examples repository to "inventory1" inventory
    And user of browser sees there are 7 lambdas in lambdas list in inventory lambdas subpage
