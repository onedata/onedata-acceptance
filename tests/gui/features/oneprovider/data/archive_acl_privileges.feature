Feature: Archives privileges test


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User successfully modifies another user archive with privilege manage archives
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
              Create archives: False
              Manage archives: True

    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
    And user of browser_user1 sees archive browser in archives tab in Oneprovider page
    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
    And user of browser_user1 clicks "Edit description" option in data row menu in archive browser
    Then user of browser_user1 writes "new description" into edit description and saves it, in details archive modal


  Scenario: User cannot modify another user archive without privilege manage archives
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
              Manage archives: False

    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
    And user of browser_user1 sees archive browser in archives tab in Oneprovider page
    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
    And user of browser_user1 hovers over "edit" option in data row menu in archive browser
    Then user of browser_user1 sees popup message about insufficient privileges requiring "manage archives" privilege


  Scenario: User successfully edits its own archive without manage, create and remove archives privileges
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True
              View archives: True
              Create archives: True

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 creates dataset for item "dir1" in "space1"
    And user of browser_user1 succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: False
              View archives: True
              Create archives: False
              Manage archives: False
              Remove archives: False

    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
    And user of browser_user1 clicks "Edit description" option in data row menu in archive browser
    Then user of browser_user1 writes "new description" into edit description and saves it, in details archive modal


  Scenario: User successfully removes another user archive with privilege remove archives
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
              Remove archives: True

    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
    And user of browser_user1 sees archive browser in archives tab in Oneprovider page
    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
    And user of browser_user1 clicks "Delete archive" option in data row menu in archive browser
    And user of browser_user1 writes "I understand that data of the archive will be lost" into confirmation input in Delete archive modal
    Then user of browser_user1 clicks on "Delete archive" button in modal "Delete archive"


  Scenario: User of browser sees Creator column in archive browser and Creator field in archive details
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of space_owner_browser sees creator column for archive with description "first archive"
    And user of space_owner_browser clicks on menu for archive with description: "first archive" in archive browser
    And user of space_owner_browser clicks "Properties" option in data row menu in archive browser
    Then user of space_owner_browser sees creator field in archive details


  Scenario: User of browser cannot create archive, when there is no archives in archive browser, without privilege create archives
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
              Create archives: False

    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
    And user of browser_user1 sees archive browser in archives tab in Oneprovider page
    And user of browser_user1 hovers over "Create archive" button in archive browser
    And user of browser_user1 sees popup message about insufficient privileges requiring "create archives" privilege
    Then user of browser_user1 sees that page with text "NO ARCHIVES" appeared in archive browser


  Scenario: User successfully creates archive without manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: False
              View archives: True
              Create archives: True

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks "Files" of "space1" space in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
