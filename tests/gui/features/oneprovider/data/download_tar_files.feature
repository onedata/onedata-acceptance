Feature: Download TAR files from GUI


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
                        - file1: 11111
                        - file_d1_2: 11111
                        - dir2:
                            - file_d2_1: 11111
                            - file_d2_2: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully downloads tar file created from single directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees item(s) named dir1 in file browser
    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Download (tar)" option in data row menu in file browser
    Then user of browser sees that contents of downloaded "dir1.tar" TAR file in download directory have following structure:
        - dir1:
            - file1: 11111
            - file_d1_2: 11111
            - dir2:
                - file_d2_1: 11111
                - file_d2_2: 11111
