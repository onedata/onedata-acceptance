Feature: Basic management of space management privileges for spaces in Onezone GUI

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


  Scenario: User fails to see privileges without view privileges
    When user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage


  Scenario: User fails to see space without view space privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: False

    Then user of browser_user1 sees that [Members, Shares, Harvesters] of "space1" in the sidebar are disabled

