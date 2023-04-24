Feature: Basic management of space marketplace

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
        inventory2:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees owned space in the Marketplace after configuring it
    When user of browser clicks on Data in the main menu
    And user of browser clicks on Marketplace button in data sidebar
    And user of browser clicks on "Advertise your space" button in space marketplace subpage
    And user of browser chooses "space1" in data type dropdown menu in modal "Advertise space"
    And user of browser clicks on "Configure..." button in modal "Advertise space"
    And user of browser sees that Advertise in Marketplace: toggle is not checked on space configuration page


    And user of browser checks Advertise in Marketplace toggle on space configuration page
    And user of browser writes "example@gmail.com" into maintainer contact e-mail name text field in modal "Advertise space in marketplace
    And user of browser writes "example@gmail.com" into store name text field in modal "Advertise space in marketplace
    And user of browser clicks on "Proceed" button in modal "Advertise space"
    And user of browser sees that Advertise in Marketplace: toggle is checked on space configuration page
    And user of browser sees that "space1" space is advertised in the Marketplace in space sidebar
    And user of browser












