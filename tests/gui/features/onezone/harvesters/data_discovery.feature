Feature: Data harvesting in Discovery Page in Onezone GUI

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
                      - file_xattrs:
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
                        - file_json:
                            content: 11111
                            metadata:
                              type: json
                              author: Samantha Anderson
                              year: 1998
          space3:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1_3:
                        - file1_3
                        - file2_3
                        - file3_3


    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: Data discovery has another GUI after setting it in harvester GUI configuration
    Given user of browser downloads http://get.onedata.org/onezone-gui-plugin-ecrin/onezone-gui-plugin-ecrin-1.1.0.tar.gz as ecrin-plugin.tar.gz to local file system
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Configuration of "harvester1" harvester in the sidebar
    And user of browser clicks on GUI plugin tab on harvester configuration page

    # upload GUI plugin
    And user of browser chooses ecrin-plugin.tar.gz GUI plugin from local directory to be uploaded
    And user of browser clicks on "Upload" button in GUI Plugin tab of harvester configuration page
    And user of browser waits until plugin upload finish

    # check GUI plugin configuration
    And user of browser sees that GUI plugin version is 1.1.0
    And user of browser sees that harvester index for study GUI plugin index is "Not assigned"
    And user of browser sees that harvester index for data_object GUI plugin index is "Not assigned"
    And user of browser sees that injected configuration is: {}

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    Then user of browser sees Data Discovery page with Ecrin GUI


  Scenario: Files of supported spaces are visible in Data discovery page
    Given spaces ["space1", "space2"] belong to "harvester1" harvester of user admin
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page

    Then user of browser sees only following files in Data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_xattrs:
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
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space1
            - space2


  Scenario: Space data is harvested in data discovery when space is added to harvester
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown
    And user of browser opens Data Discovery page of "harvester1" harvester
    Then user of browser sees only following files in Data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_xattrs:
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
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space1
            - space2


  Scenario: Files uploaded to harvested space are visible in Data discovery page
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    # upload and add metadata to file in space2
    And user of browser uploads "20B-0.txt" to the root directory of "space2"
    And user of browser succeeds to write "20B-0.txt" file basic metadata: "author=John Doe" in "space2"

    And user of browser opens Data Discovery page of "harvester1" harvester
    Then user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
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


  Scenario: Files deleted from harvested space are no longer visible in Data discovery page
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    # delete file from "space2"
    And user of browser opens file browser for "space2" space
    And user of browser succeeds to remove "dir1_2/file_json" in "space2"

    And user of browser opens Data Discovery page of "harvester1" harvester
    Then user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          spaces:
            - space2


  Scenario: Metadata changes of file in harvested space are visible in Data discovery page
    Given space "space1" belongs to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_xattrs:
            spaceId: space1
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: true
            xattrs:
              author: "\"John Smith\""
              year: 2020
          spaces:
            - space1

    # delete part of metadata
    And user of browser removes basic metadata entry with key "author" for "dir1_1/file_xattrs" file in "space1" space
    And user of browser opens Data Discovery page of "harvester1" harvester
    Then user of browser sees only following files in Data discovery page:
          dir1_1:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space1
          file_xattrs:
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


  Scenario: User successfully opens space of harvested file
    Given spaces ["space2", "space3"] belong to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            spaceId: space2
          file_json:
            spaceId: space2
          dir1_3:
            spaceId: space3
          file1_3:
            spaceId: space3
          file2_3:
            spaceId: space3
          file3_3:
            spaceId: space3
          spaces:
            - space2
            - space3

    And user of browser clicks on "Go to source file..." for "file2_3"
    Then user of browser is redirected to newly opened tab
    And user of browser is idle for 4 seconds
    And user of browser sees that opened space name is "space3"
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees only items named ["file1_3", "file2_3", "file3_3"] in file browser
    And user of browser sees that "file2_3" item is selected in file browser
    And user of browser sees that ["file1_3", "file3_3"] items are not selected in file browser


   Scenario: Data could not be presented when elasticsearch does not respond
    Given space "space2" belongs to "harvester1" harvester of user admin
    When user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2

    And elasticsearch plugin stops working
    And user of browser is idle for 2 seconds
    And user of browser clicks "Query" button on Data discovery page
    Then user of browser sees "This resource could not be loaded." alert on Data discovery page

    And elasticsearch plugin starts working
    And user of browser is idle for 5 seconds
    And user of browser clicks "Query" button on Data discovery page
    And user of browser sees Data Discovery page
    And user of browser sees only following files in Data discovery page:
          dir1_2:
            jsonMetadataExists: false
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
          file_json:
            jsonMetadataExists: true
            rdfMetadataExists: false
            xattrsMetadataExists: false
            spaceId: space2
            author: "\"Samantha Anderson\""
            year: 1998
          spaces:
            - space2
