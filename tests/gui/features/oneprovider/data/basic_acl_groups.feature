Feature: basic ACL operations

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

    
  Scenario: dssks
    # When user of browser1 sets "dir1" ACL [acl:read acl, acl:change acl] privileges for user user2 in "space1"
    # And user of browser1 sets "dir1" ACL [] privileges for group group1 in "space1"

    When user of browser1 clicks "Members" of "space1" space in the sidebar
    And user of browser1 clicks "user2" user in "space1" space members users list
    And user of browser1 sets following privileges for "user2" user in space members subpage:
        Space management:
            granted: False
        Transfer management:
            granted: False
    
    And user of browser1 clicks "group1" group in "space1" space members groups list
    And user of browser1 sets following privileges for "group1" group in space members subpage:
        Space management:
            granted: False
        Data management:
            granted: False
        Transfer management:
            granted: False
    
    And user of browser1 clicks "Files" of "space1" space in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 creates directory "dir1"
    And user of browser1 clicks on menu for "dir1" file in file browser
    And user of browser1 clicks "Information" option in data row menu in file browser
    And user of browser1 clicks on "Permissions" navigation tab in "Directory Details" modal
    And user of browser1 selects "ACL" permission type in edit permissions panel