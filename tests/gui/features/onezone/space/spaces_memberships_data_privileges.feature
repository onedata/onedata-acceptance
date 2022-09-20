Feature: Basic management of data privileges for spaces in Onezone GUI

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


  Scenario: Non-space-owner successfully views data if he got Read files privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: False

    # Files in space1 tab is disabled when Read files privilege is not granted
    And user of browser_user1 sees that Files tab of "space1" is disabled

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True

    # Non-space-owner checks if he can view file in file browser
    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    Then user of browser_user1 sees item(s) named dir1 in file browser


  Scenario: Non-space-owner successfully creates directory if he got Write files privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: False

    # Non-space-owner fails to create directory in space1
    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser_user1 clicks "New directory" button from file browser menu bar
    And user of browser_user1 writes "new_directory" into text field in modal "Create dir"
    And user of browser_user1 confirms create new directory using button
    And user of browser_user1 sees that error modal with text "Creating directory failed" appeared
    And user of browser_user1 closes "Error" modal

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: True

    And user of browser_user1 is idle for 1 seconds
    And user of browser_user1 clicks "New directory" button from file browser menu bar
    And user of browser_user1 writes "new_directory" into text field in modal "Create dir"
    And user of browser_user1 confirms create new directory using button
    Then user of browser_user1 sees that item named "new_directory" has appeared in file browser


  # TODO: VFS-9603 reimplement gui shares tests after move to file info modal 
  # Scenario: Non-space-owner successfully creates share if he got Manage shares privilege
  #   When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
  #   And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
  #   And user of space_owner_browser clicks "user1" user in "space1" space members users list
  #   And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
  #         Data management:
  #           granted: Partially
  #           privilege subtypes:
  #             Manage shares: False

  #   # Non-space-owner fails to create share in space1
  #   And user of browser_user1 clicks "Files" of "space1" space in the sidebar
  #   And user of browser_user1 sees file browser in files tab in Oneprovider page
  #   And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
  #   And user of browser_user1 clicks on menu for "dir1" file in file browser
  #   And user of browser_user1 clicks "Share" option in data row menu in file browser
  #   And user of browser_user1 clicks on "Create" button in modal "Share directory"
  #   And user of browser_user1 sees that error modal with text "Creating share failed" appeared
  #   And user of browser_user1 closes "Error" modal
  #   And user of browser_user1 clicks on "Close" button in modal "Share directory"

  #   And user of space_owner_browser clicks "user1" user in "space1" space members users list
  #   And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
  #         Data management:
  #           granted: Partially
  #           privilege subtypes:
  #             Manage shares: True

  #   And user of browser_user1 clicks on menu for "dir1" file in file browser
  #   And user of browser_user1 clicks "Share" option in data row menu in file browser
  #   And user of browser_user1 clicks on "Create" button in modal "Share directory"
  #   And user of browser_user1 clicks on "Close" button in modal "Share directory"
  #   And user of browser_user1 opens shares view of "space1"
  #   And user of browser_user1 clicks "dir1" share in shares browser on shares view
  #   And user of browser_user1 sees file browser on single share view
  #   Then user of browser_user1 sees that item named "dir1" has appeared in file browser on single share view


