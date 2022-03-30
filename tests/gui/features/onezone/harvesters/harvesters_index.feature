Feature: Basic management of harvester index in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
      space1:
        owner: admin
        providers:
          - oneprovider-1:
              storage: posix
              size: 1000000
        storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1
    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service



  Scenario: User does not see file name after creating index that does not include file name file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["rdf", "basic", "json"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser does not see "dir1" in results list on data discovery page


  Scenario: User sees file type after creating index that includes file type file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["basic", "file_name", "file_type"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page

    Then user of browser sees only following files in Data discovery page:
        dir1:
          xattrs:
            attr: "\"val\""
          fileType:
            "\"DIR\""
        spaces:
          - space1


  Scenario: User sees space ID after creating index that includes space_id file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["basic", "file_name", "space_id"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
        dir1:
          xattrs:
            attr: "\"val\""
          spaceId: space1
        spaces:
          - space1


  Scenario: User sees dataset info after creating index that includes dataset info file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["basic", "file_name", "dataset_info"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
        dir1:
          xattrs:
            attr: "\"val\""
          isDataset: true
        spaces:
          - space1


  Scenario: User sees archive info after creating index that includes archive info file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And  user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first_archive
        layout: plain

    # copy archive id
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser saves time of creation archive with description: "first_archive" for "dir1"
    And user of browser clicks on menu for archive with description: "first_archive" in archive browser
    And user of browser clicks "Copy archive ID" option in data row menu in archive browser

    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown
    And user of browser creates new index "index1" that includes ["basic", "file_name", "archive_info"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"
    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page

    Then user of browser sees archives ID in results list on data discovery page
    And user of browser sees archives description: "first_archive" in results list on data discovery page
    And user of browser sees that archives creation time in results list on data discovery page is the same as on the archives page
    And user of browser sees file name for archive: "dir1" in results list on data discovery page

