Feature: Oneprovider transfers basic functionality

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: User selects desirable columns to be visible and can see only them in transfers table
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Transfers" of "space1" space in the sidebar
    And user of browser waits for Transfers page to load
    And user of browser selects only <columns_list> columns from columns list in transfers table
    Then user of browser sees <columns_list> columns in transfers table
    And user of browser does not see <other_columns_list> columns in transfers table
    And user of browser refreshes site
    And user of browser waits for Transfers page to load
    And user of browser sees <columns_list> columns in transfers table
    And user of browser does not see <other_columns_list> columns in transfers table

  # in standard browser view max 3 columns can be displayed
  Examples:
    |columns_list                              |other_columns_list                                                 |
    |["User", "Type", "Status"]                |["Destination", "Started at", "Processed", "Replicated", "Evicted"]|
    |["Destination", "Processed", "Replicated"]|["User", "Type", "Status", "Started at",  "Evicted"]               |