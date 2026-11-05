Feature: Nested archives operations

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
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
                    - dir1:
                      - file1: 100

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service
  

  Scenario: User can see a newly created archive by another user without refreshing, with its status preserved
    When user of browser1 creates dataset for item "dir1" in "space1"
    And user of browser1 clicks "Members" of "space1" space in the sidebar
    And user of browser1 clicks "user2" user in "space1" space members users list
    And user of browser1 sets following privileges for "user2" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True

    And user of browser2 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser2 sees dataset browser in datasets tab in Oneprovider page
    And user of browser2 clicks on dataset for "dir1" in dataset browser
    And user of browser2 sees archive browser in archives tab in Oneprovider page

    And user of browser1 succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain

    Then user of browser2 sees that archive with description: "first archive" in archive browser has status: "preserved", number of files: 1, size: "3 B"


  Scenario: User, without refreshing, can see newly created dataset by other user
    When user of browser2 clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser2 sees dataset browser in datasets tab in Oneprovider page

    And user of browser1 creates dataset for item "dir1" in "space1"

    Then user of browser2 sees item(s) named "dir1" in dataset browser
    
