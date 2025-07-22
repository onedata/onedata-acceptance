Feature: Archive audit logs

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000   

    And using REST, user1 creates a path with 20 nested directories named "long_0/.../long_19" in "space1" supported by "oneprovider-1" provider
    And using REST, user1 creates "file_20" file in the last of 20 nested directories "long_0/.../long_19" in "space1" supported by "oneprovider-1" provider
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

  Scenario: User sees correct path for archived nested directories with long names
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "long_0" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar

    And user of browser sees dataset browser in datasets tab in Oneprovider page

    And user of browser succeeds to create archive for item "long_0" in "space1" with following configuration:
        description: first archive
        layout: plain
    
    And user of browser waits for "Preserved" state for archive with description "first archive" in archive browser
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser

    And user of browser clicks on item "file_20" using scroll in archive audit log
    And user of browser checks that path in "Audit Log Entry Details" is like: "long_0/.../long_19/file_20"


    

