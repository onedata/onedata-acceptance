Feature: Archives cancel test


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
    And directory tree structure on local file system:
            browser_user1:
                dir2:
                  file50MiB.txt:
                    size: 50 MiB
            space_owner_browser:
                dir2:
                  file50MiB.txt:
                    size: 50 MiB

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User successfully cancels creation its own archive without manage, create and remove archives privileges
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
    And user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    And user of browser_user1 uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
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
    And user of browser_user1 clicks "Cancel archivization" option in data row menu in archive browser
    And user of browser_user1 clicks on "Yes" button in modal "Cancel archive"
    Then user of browser_user1 sees that item "dir1" has 0 archives


  Scenario: User cannot cancel creation another user archive without manage archives privilege
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
              Manage archives: False
    And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
    And user of browser_user1 sees archive browser in archives tab in Oneprovider page

    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain

    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
    And user of browser_user1 hovers over "Cancel archivisation" option in data row menu in archive browser
    Then user of browser_user1 sees popup message about insufficient privileges requiring "manage archives" privilege

