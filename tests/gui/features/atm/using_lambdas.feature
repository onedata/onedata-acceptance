Feature: Using lambda dumps


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


  Scenario: Each lambda dump from automation-examples remains the same after uploading and downloading it from automation inventory
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads all lambda dumps from automation-examples repository to "inventory1" inventory
    And user of browser downloads and removes all previously uploaded lambda dumps from "inventory1" inventory
    Then user of browser sees that each previously uploaded lambda dump is the same after download
