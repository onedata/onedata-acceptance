Feature: Public harvester site

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
                - dir1_1:
                  - file_with_xattrs:
                      content: 11111
                      metadata:
                        type: basic
                        author: John Smith
                        year: 2020
          space2:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1_2:
                    - file_with_json_metadata:
                        content: 11111
                        metadata:
                          type: json
                          author: Samantha Anderson
                          year: 1998

    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And users opened [browser_onedata, browser_not_signed_in] browsers' windows
    And user of browser_onedata opened Onezone page
    And user of browser_onedata logged as admin to Onezone service


  Scenario: Not signed in user sees public data discovery page when harvester is configured as public
    When user of browser_onedata clicks on Discovery in the main menu
    And user of browser_onedata clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_onedata clicks Configuration of "harvester1" harvester in the sidebar

    And user of browser_onedata sees that Public toggle is not checked on harvester configuration page
    And user of browser_onedata clicks on "Edit" button in General tab of harvester configuration page
    And user of browser_onedata checks Public toggle on harvester configuration page
    And user of browser_onedata clicks on "Save" button in General tab of harvester configuration page

    And user of browser_onedata sees that Public toggle is checked on harvester configuration page
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in
    And user of browser_not_signed_in opens URL received from user of browser_onedata
    Then user of browser_not_signed_in sees public data discovery page with no harvested data


  Scenario: Not signed in user cannot open public data discovery page if harvester is no longer public
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in
    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page with no harvested data

    And user of browser_onedata clicks on "Edit" button in General tab of harvester configuration page
    And user of browser_onedata unchecks Public toggle on harvester configuration page
    And user of browser_onedata clicks on "Save" button in General tab of harvester configuration page
    And user of browser_onedata sees that Public toggle is not checked on harvester configuration page

    And user of browser_not_signed_in refreshes site
    Then user of browser_not_signed_in sees "web GUI cannot be loaded" error on Onedata page


  Scenario: Not signed in user sees data of public harvester in public harvester GUI from given URL
    Given spaces ["space1", "space2"] belong to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    Then user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_with_xattrs:
            spaceId: space1
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: true
            xattrs:
              author: "\"John Smith\""
              year: 2020
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_with_json_metadata:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space1
            - space2


  Scenario: Public harvester site is updated after new files are uploaded to space
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
         dir1_2:
           jsonMetadataExists: false
           rdfMetadataExists: false
           xattrsMetadataExists: false
           spaceId: space2
         file_with_json_metadata:
           jsonMetadataExists: true
           rdfMetadataExists: false
           xattrsMetadataExists: false
           spaceId: space2
           author: "\"Samantha Anderson\""
           year: 1998
         spaces:
           - space2

    # upload and add metadata to file in space2
    And user of browser_onedata uploads "20B-0.txt" to the root directory of "space2"
    And user of browser_onedata succeeds to write "20B-0.txt" file basic metadata: "author=John Doe" in "space2"

    Then user of browser_not_signed_in sees only following files on public data discovery page:
         dir1_2:
           jsonMetadataExists: false
           rdfMetadataExists: false
           xattrsMetadataExists: false
           spaceId: space2
         file_with_json_metadata:
           jsonMetadataExists: true
           rdfMetadataExists: false
           xattrsMetadataExists: false
           spaceId: space2
           author: "\"Samantha Anderson\""
           year: 1998
         20B-0.txt:
           jsonMetadataExists: false
           rdfMetadataExists: false
           xattrsMetadataExists: true
           xattrs:
             author: "\"John Doe\""
         spaces:
           - space2


  Scenario: Public harvester site has another GUI after setting it in original harvester configuration
    Given user of browser_onedata downloads http://get.onedata.org/onezone-gui-plugin-ecrin/onezone-gui-plugin-ecrin-1.1.0.tar.gz as ecrin-plugin.tar.gz to local file system
    When user of browser_onedata clicks on Discovery in the main menu
    And user of browser_onedata clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_onedata clicks Configuration of "harvester1" harvester in the sidebar
    And user of browser_onedata clicks on GUI plugin tab on harvester configuration page

    # upload GUI plugin
    And user of browser_onedata chooses ecrin-plugin.tar.gz GUI plugin from local directory to be uploaded
    And user of browser_onedata clicks on "Upload" button in GUI Plugin tab of harvester configuration page
    And user of browser_onedata waits until plugin upload finish

    And user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    Then user of browser_not_signed_in sees public data discovery page with Ecrin GUI


  Scenario: Public harvester site is updated when space is added to original harvester
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_with_json_metadata:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    And user of browser_onedata adds "space1" space to "harvester1" harvester using available spaces dropdown
    Then user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_with_xattrs:
            spaceId: space1
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: true
            xattrs:
              author: "\"John Smith\""
              year: 2020
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_with_json_metadata:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space1
            - space2


  Scenario: Public harvester site is updated when files are removed from space in original harvester
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_with_json_metadata:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    # delete file from "space2"
    And user of browser_onedata opens file browser for "space2" space
    And user of browser_onedata succeeds to remove "dir1_2/file_with_json_metadata" in "space2"

    Then user of browser_not_signed_in sees only following files on public data discovery page:
           dir1_2:
             jsonMetadataExists: false
             rdfMetadataExists: false
             xattrsMetadataExists: false
             spaceId: space2
           spaces:
             - space2


  Scenario: Public harvester site is updated when file metadata is updated in space of original harvester
    Given space "space1" belongs to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
         dir1_1:
           jsonMetadataExists: false
           rdfMetadataExists: false
           xattrsMetadataExists: false
           spaceId: space1
         file_with_xattrs:
           spaceId: space1
           jsonMetadataExists: false
           rdfMetadataExists: false
           xattrsMetadataExists: true
           xattrs:
             author: "\"John Smith\""
             year: 2020
         spaces:
           - space1

    And user of browser_onedata removes basic metadata entry with key "author" for "dir1_1/file_with_xattrs" file in "space1" space
    Then user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_1:
             jsonMetadataExists: false
             rdfMetadataExists: false
             xattrsMetadataExists: false
             spaceId: space1
          file_with_xattrs:
            spaceId: space1
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: true
            xattrs:
              year: 2020
              unexpected:
                author: "\"John Smith\""
          spaces:
            - space1


  Scenario: User cannot open harvested file source from public harvester if they does not belong to space
    Given spaces "space2" belong to "harvester1" harvester of user admin
    When user of browser_onedata configures "harvester1" harvester as public
    And user of browser_onedata clicks on copy icon of public harvester URL
    And user of browser_onedata sends copied URL to user of browser_not_signed_in

    And user of browser_not_signed_in opens URL received from user of browser_onedata
    And user of browser_not_signed_in sees public data discovery page
    And user of browser_not_signed_in sees only following files on public data discovery page:
          dir1_2:
            spaceId: space2
          file_with_json_metadata:
            spaceId: space2
          spaces:
            - space2

    And user of browser_not_signed_in clicks on "Go to source file..." for "file_with_json_metadata"
    And user of browser_not_signed_in is redirected to newly opened tab
    And user of browser_not_signed_in sees Onezone login page

    And user of browser_not_signed_in logs as user1 to Onezone service
    Then user of browser_not_signed_in sees "YOU DON’T HAVE ACCESS TO THIS RESOURCE" error on spaces page
