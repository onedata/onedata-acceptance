Feature: Basic management of spaces privileges in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: space-owner-user
            groups:
                - group1
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
          space2:
            owner: space-owner-user
            users:
                - user1
                - user2
            groups:
                - group2
          space3:
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


  Scenario: User sees and modifies privileges to his space
    When user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: True
    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    Then user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: True


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


  Scenario: User fails to see privileges of another user until he is granted all privileges by becoming an owner
    When user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    And user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list

    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees "This user is a space owner and is authorized to perform all operations, regardless of the assigned privileges." warning for "user1" user in space members subpage

    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees privileges for "space-owner-user" user in space members subpage


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


  Scenario: User fails to remove group from space without remove group privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks show view expand button in space members subpage header
    And user of browser_user1 clicks memberships view mode in space members subpage
    And user of browser_user1 clicks "group2" group in "space2" space members groups list
    And user of browser_user1 clicks on "group2" member relation menu button to "space2" space
    And user of browser_user1 clicks on "Remove relation" in space membership relation menu
    And user of browser_user1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared


  Scenario: Appropriate tabs are disabled after removing some of user privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list

    # All tabs are enabled when all privileges are granted
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: True
          Data management:
            granted: True
          Transfer management:
            granted: True
          QoS management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: True
          Support management:
            granted: True
          Harvester management:
            granted: True
    Then user of browser_user1 sees that all tabs of "space1" are enabled

    # Some tabs are disabled when view space is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: False
    And user of browser_user1 sees that [Overview, Files, Transfers, Providers] tabs of "space1" are enabled
    And user of browser_user1 sees that [Shares, Members, Harvesters] tabs of "space1" are disabled

    # All tabs are enabled when only view space from space management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: True
              Modify space: False
              Remove space: False
              View privileges: False
              Set privileges: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Some tabs are disabled when none from space management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: False
    And user of browser_user1 sees that [Overview, Files, Transfers, Providers] tabs of "space1" are enabled
    And user of browser_user1 sees that [Shares, Members, Harvesters] tabs of "space1" are disabled

    # Only files tab is disabled when only read files is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: False
    And user of browser_user1 sees that [Overview, Shares, Transfers, Providers, Members, Harvesters] tabs of "space1" are enabled
    And user of browser_user1 sees that Files tab of "space1" is disabled

    # All tabs are enabled when only read files from data management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True
              Write files: False
              Register files: False
              Manage shares: False
              View database views: False
              Manage database views: False
              Query database views: False
              View statistics: False
              View changes stream: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only files tab is disabled when none from data management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: False
    And user of browser_user1 sees that [Overview, Shares, Transfers, Providers, Members, Harvesters] tabs of "space1" are enabled
    And user of browser_user1 sees that Files tab of "space1" is disabled

    # Only transfers tab is disabled when only view transfers is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: False
    And user of browser_user1 sees that [Overview, Files, Shares, Providers, Members, Harvesters] tabs of "space1" are enabled
    And user of browser_user1 sees that Transfers tab of "space1" is disabled

    # All tabs are enabled when only view transfers from transfer management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False
              Cancel replication: False
              Schedule eviction: False
              Cancel eviction: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only transfers tab is disabled when none from transfer management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: False
    And user of browser_user1 sees that [Overview, Files, Shares, Providers, Members, Harvesters] tabs of "space1" are enabled
    And user of browser_user1 sees that Transfers tab of "space1" is disabled

    # All tabs are enabled when none from QoS management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          QoS management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from user management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          User management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from group management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Group management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from support management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Support management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from harvester management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Harvester management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled


  Scenario: Non-owner-user fails to remove space because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              Remove space: False

    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks on "Remove" button in space "space2" menu
    And user of browser_user1 clicks on understand notice checkbox in "Remove space" modal
    And user of browser_user1 clicks on "Remove" button in "Remove space" modal
    Then user of browser_user1 sees that error modal with text "Removing the space failed" appeared


  Scenario: User fails to generate space invite token because of lack in privileges
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite user using token" button in users list menu in "space2" space members view
    Then user of browser_user1 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: User fails to rename space because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              Modify space: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 writes "space2" into rename space text field
    And user of browser_user1 confirms rename the space using confirmation button
    Then user of browser_user1 sees that error modal with text "Changing name failed" appeared


  Scenario: User fails to remove other user from given space because of lack in privileges
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 removes "user2" user from "space2" space members
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared


  Scenario: Non-space-owner successfully generates space invite token if he got user management privilege
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
            User management:
              granted: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite user using token" button in users list menu in "space2" space members view
    And user of browser_user1 sees that "Invite user using token" modal has appeared
    Then user of browser_user1 copies invitation token from modal


  Scenario: Non-owner-user fails to generate group invite token because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    Then user of browser_user1 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: Non-owner-user generates group invite token to join space
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    And user of browser_user1 sees that "Invite group using token" modal has appeared
    Then user of browser_user1 copies invitation token from modal


  Scenario: Non-owner-user generates add support token
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Support management:
            granted: True

    And user of browser_user1 clicks Providers of "space1" in the sidebar
    And user of browser_user1 clicks Add support button on providers page
    And user of browser_user1 clicks Copy button on Add support page
    Then user of browser_user1 sees an info notify with text matching to: .*copied.*


  Scenario: Non-owner-user views space
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: True

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: Non-owner-user fails to view space because of lack in privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that [Members, Shares, Harvesters] of "space1" in the sidebar are disabled


  Scenario: Non-owner-user sets privileges for other user
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user2" user in "space1" space members users list
    And user of browser_user1 sets following privileges for "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False

    And user of browser_user1 clicks "user2" user in "space1" space members users list
    Then user of browser_user1 sees following privileges of "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False


  Scenario: Non-owner-user fails to set privileges to other user because of lack in privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user2" user in "space1" space members users list
    And user of browser_user1 sets following privileges for "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared


  Scenario: Non-space-owner successfully views data if he got Read files privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
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
    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    Then user of browser_user1 sees item(s) named dir1 in file browser


  Scenario: Non-space-owner successfully creates directory if he got Write files privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: False

    # Non-space-owner checks if he can create directory in space1
    And user of browser_user1 clicks Files of "space1" in the sidebar
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


  Scenario: Non-space-owner successfully creates share if he got Manage shares privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Manage shares: False

    # Non-space-owner checks if he can create share in space1
    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Share" option in data row menu in file browser
    And user of browser_user1 clicks on "Create" button in modal "Share directory"
    And user of browser_user1 sees that error modal with text "Creating share failed" appeared
    And user of browser_user1 closes "Error" modal
    And user of browser_user1 clicks on "Close" button in modal "Share directory"

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Manage shares: True

    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Share" option in data row menu in file browser
    And user of browser_user1 clicks on "Create" button in modal "Share directory"
    Then user of browser_user1 clicks on "Close" button in modal "Share directory"


  Scenario: Non-space-owner successfully views QoS if he got View QoS privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: False

    # Non-space-owner checks if he can select Quality of Service option of the directory
    And user of browser_user1 clicks Files of "space1" in the sidebar
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


  Scenario: Non-space-owner successfully menages QoS if he got Qos management privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: Partially
            privilege subtypes:
              View QoS: True
              Manage QoS: False

    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Quality of Service" option in data row menu in file browser
    And user of browser_user1 sees "Insufficient privileges to access this resource" in modal "Quality of Service"
    And user of browser_user1 clicks on "Close" button in modal "Quality of Service"

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: True

    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Quality of Service" option in data row menu in file browser
    Then user of browser_user1 does not see "Insufficient privileges to access this resource" in modal "Quality of Service"

