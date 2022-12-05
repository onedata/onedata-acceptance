Feature: Basic management of qos privileges for spaces in Onezone GUI

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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: Non-space-owner successfully manages QoS if he got Qos management privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: Partially
            privilege subtypes:
              View QoS: True
              Manage QoS: False

    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Quality of Service" option in data row menu in file browser
    And user of browser_user1 sees "THERE ARE NO QOS REQUIREMENTS DEFINED FOR THIS DIRECTORY" in QoS panel
    And user of browser_user1 sees that "Add requirement" button is disabled in QoS panel
    And user of browser_user1 clicks on "X" button in modal "Directory details"

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: True

    Then user of browser_user1 creates "hello=WORLD" QoS requirement for "dir1" in space "space1"


  Scenario: Non-space-owner successfully views QoS in menu if he got View QoS privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: False

    # Non-space-owner fails to select Quality of Service option of the directory
    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 sees that Quality of Service option is not in selection menu on file browser page

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: Partially
            privilege subtypes:
              View QoS: True

    Then user of browser_user1 sees that Quality of Service option is in selection menu on file browser page
