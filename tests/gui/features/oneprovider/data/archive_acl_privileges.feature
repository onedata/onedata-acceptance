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
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1
    And directory tree structure on local file system:
            file1MiB.txt:
              size: 1 MiB


    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


#  Scenario: User successfully edits description of another user archive with privilege Manage archive
#    When user of space_owner_browser creates dataset for item "dir1" in "space1"
#    And user of space_owner_browser succeeds to create archive for item "dir1" in "space1" with following configuration:
#        description: first archive
#        layout: plain
#    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
#    And user of space_owner_browser clicks "user1" user in "space1" space members users list
#    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
#          Dataset & archive management:
#            granted: Partially
#            privilege subtypes:
#              Manage archives: True
#              View archives: True
#
#    And user of browser_user1 clicks "Datasets, Archives" of "space1" space in the sidebar
#    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
#    And user of browser_user1 clicks on dataset for "dir1" in dataset browser
#    And user of browser_user1 sees archive browser in archives tab in Oneprovider page
#    And user of browser_user1 clicks on menu for archive with description: "first archive" in archive browser
#    And user of browser_user1 clicks "Edit description" option in data row menu in archive browser
#    And user of browser_user1 writes "new description" into edit description in Details Archive modal


  Scenario: User successfully cancels archive its own archive
    When trace