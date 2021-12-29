Feature: BagIt and DIP archives operations

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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - dir2:
                        - dir3:
                          - file1: 100
                    - dir4:
                      - file2: 100

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees BagIt tag after creating BagIt archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: BagIt
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees BagIt tag for archive with description: "first archive" on archives list in archive browser


   Scenario: User sees DIP tag after creating archive with "Include DIP" option
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: DIP archive
        layout: plain
        include DIP: True
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees DIP tag for archive with description: "DIP archive" on archives list in archive browser


  Scenario: User sees BagIt metadata files and directory tree in AIP tab and directory tree in DIP tab in archive browser after creating archive with "BagIt" layout and "Include DIP" option
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: BagIt
        include DIP: True
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - bagit.txt
         - data:
           - dir1:
             - dir2:
               - dir3:
                 - file1: 100
         - manifest-md5.txt
         - manifest-sha1.txt
         - manifest-sha256.txt
         - manifest-sha512.txt
         - metadata.json
         - tagmanifest-md5.txt
         - tagmanifest-sha1.txt
         - tagmanifest-sha256.txt
         - tagmanifest-sha512.txt
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser clicks on DIP view mode on archive file browser page
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100




