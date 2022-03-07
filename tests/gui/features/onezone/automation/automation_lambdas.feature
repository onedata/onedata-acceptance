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
    And user of browser uses Add new lambda button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker_image_example" into docker image text field
    And user of browser confirms create new lambda using Create button
    Then user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage


  Scenario: User sees new lambda revision after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses Add new lambda button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker_image_example" into docker image text field
    And user of browser confirms create new lambda using Create button
    And user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage
    And user of browser clicks on Create new revision in "Lambda1"
    And user of browser writes "Lambda2" into lambda name text field
    And user of browser confirms create new revision using Create button
    Then user of browser sees "Lambda2" in lambdas revision list of "Lambda2" in inventory lambdas subpage


  Scenario: User sees new lambda revision after using redesign as new revision
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses Add new lambda button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker_image_example" into docker image text field
    And user of browser confirms create new lambda using Create buttonn
    And user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage
    And user of browser clicks on "Redesign as new revision" button in revision "Lambda1" menu in the "Lambda1" lambda revision list
    And user of browser writes "Lambda2" into lambda name text field
    And user of browser confirms create new revision using Create button
    Then user of browser sees "Lambda2" in lambdas revision list of "Lambda2" in inventory lambdas subpage

