Feature: Groups creation in Oneprovider GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    And user of browser clicked on the "groups" tab in main menu sidebar


  Scenario: User creates new group (presses ENTER after entering group name)
    When user of browser clicks on the Create button in groups sidebar header
    And user of browser sees that "Create a new group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    Then user of browser sees that group named "helloworld" has appeared in the groups list


  Scenario: User creates new group (clicks CREATE confirmation button after entering group name)
    When user of browser clicks on the Create button in groups sidebar header
    And user of browser sees that "Create a new group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser clicks "Create" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    Then user of browser sees that group named "helloworld" has appeared in the groups list
