Feature: Limited visibility of users and groups in ACL panel when user lacks privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            users:
              - user2    
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            users:
                - user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
            groups:
                - group1

    And opened [browser1, browser2] with [user1, user2] signed in to [Onezone, Onezone] service

    
  Scenario: User with limited privileges opens ACL permissions in details modal and sees correct warning
    When user of browser1 clicks "Members" of "space1" space in the sidebar
    
    And user of browser1 clicks "group1" group in "space1" space members groups list
    And user of browser1 sets all privileges false for "group1" group in space members subpage

    And user of browser1 clicks "user2" user in "space1" space members users list
    And user of browser1 sets following privileges for "user2" user in space members subpage when all other are not granted:
        Data management:
            granted: Partially
            privilege subtypes:
                Read files: True
                Write files: True

    
    And user of browser2 opens file browser for "space1" space
    And user of browser2 creates directory "dir1"
    And user of browser2 clicks on menu for "dir1" file in file browser
    And user of browser2 clicks "Information" option in data row menu in file browser
    And user of browser2 clicks on "Permissions" navigation tab in "Directory Details" modal
    And user of browser2 selects "ACL" permission type in edit permissions panel

    Then user of browser2 sees the following warning: "Some space members may not be visible due to limited privileges." in ACL Edit Permissions tab
    And user of browser2 sees that [user1, user2, group1] are in subject list in ACL record