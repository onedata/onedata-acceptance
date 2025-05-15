Feature: Management of a great number of spaces

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see correct number of previously created spaces in spaces list in the sidebar
    When using REST, user1 creates 500 spaces in "onezone" Onezone service
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser clicks on Data in the main menu
    Then user of browser can see there are 500 spaces on the spaces list in the sidebar


  Scenario: User can see that correct space is opened after refreshing page
    When using REST, user1 creates 500 spaces in "onezone" Onezone service
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser opens "space250" space on the spaces list in the sidebar
    And user of browser refreshes site
    And user of browser can see that opened space is "space250" on the spaces list in the sidebar


  Scenario: User can see correct number of shares created in multiple spaces in shares sidebar
    When using REST, user1 creates 150 spaces each with share in "onezone" Onezone service
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser clicks on Shares in the main menu
    Then user of browser can see there are 150 shares on the shares list in the sidebar


  Scenario: User can see correct number of shares created in single space
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    When using REST, user1 creates 150 shares in space "space1" in oneprovider-1
    And user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser clicks on Shares in the main menu
    Then user of browser can see there are 150 shares on the shares list in the sidebar
    And user of browser clicks on Data in the main menu
    And user of browser clicks on Data in the main menu
    And user of browser clicks "Shares, Public Data" of "space1" space in the sidebar
    And user of browser can see there are 150 shares in shares view