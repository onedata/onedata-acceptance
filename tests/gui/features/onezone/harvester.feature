Feature: Basic management of harvester in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User successfully creates new harvester
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks on Create harvester button in discovery sidebar
    And user of browser types "harvester1" to name input field in discovery page
    And user of browser types elasticsearch client endpoint to endpoint input field in discovery page
    And user of browser clicks on Create button in discovery page
    Then user of browser sees that "harvester1" has appeared on the harvesters list in the sidebar


  Scenario: User fails to create new harvester
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks on Create harvester button in discovery sidebar
    And user of browser types "harvester1" to name input field in discovery page
    And user of browser types "incorrect_endpoint" to endpoint input field in discovery page
    And user of browser clicks on Create button in discovery page
    Then user of browser sees that error popup has appeared


  Scenario: User successfully adds space to harvester
    When user of browser creates space2 space in Onezone page
    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Spaces of "harvester1" harvester in the sidebar
    And user of browser clicks add one of your spaces button in harvester spaces page
    And user of browser chooses space2 from dropdown in add space modal
    And user of browser clicks on "Add" button in modal "Choose Space"
    Then user of browser sees that "space2" has appeared on the spaces list in discovery page


  Scenario: User successfully renames harvester
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks on "Rename" button in harvester "harvester1" menu in the sidebar
    And user of browser types "harvester2" to rename harvester input field
    And user of browser confirms harvester rename using button
    Then user of browser sees that "harvester2" has appeared on the harvesters list in the sidebar
    And user of browser sees that "harvester1" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully leave harvester
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester2" on the harvesters list in the sidebar
    And user of browser clicks on "Leave" button in harvester "harvester2" menu in the sidebar
    And user of browser clicks on "Leave" button in modal "Leave harvester"
    And user of browser sees that "harvester2" has disappeared on the harvesters list in the sidebar
