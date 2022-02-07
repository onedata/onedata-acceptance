Feature: Basic management of support privileges for spaces in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User fails to invite provider without privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Support management:
            granted: False
    And user of browser_user1 clicks Providers of "space1" in the sidebar
    And user of browser_user1 clicks Add support button on providers page
    Then user of browser_user1 sees INSUFFICIENT PRIVILEGES alert on providers page