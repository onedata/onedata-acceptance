Feature: Basic management of spaces privileges in Onezone GUI with two providers


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1
                - user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
                    - dir2
                    - file1
                    - file2

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


Scenario: Non-space-owner successfully views transfers if he got View Transfers privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: False

    And user of browser_user1 sees that Files tab of "space1" is disabled
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True

    And user of browser_user1 clicks Files of "space1" in the sidebar