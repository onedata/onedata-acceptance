Feature: Storage S3 management using onepanel, REST


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-1 in Onepanel
    And "test_storage1" storage backend in "oneprovider-1" Oneprovider panel service used by admin with following configuration:
          storage type: S3
          hostname: http://dev-volume-s3-krakow.default:9000
          bucket name: test
          access key: accessKey
          secret key: verySecretKey

    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: admin
              providers:
                  - oneprovider-1:
                      storage: test_storage1
                      size: 1000000


    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service
    And S3 host entry is added to /etc/hosts


  Scenario: User sees file's content after modifying storage backend by setting new S3 bucket with copied content from the previous bucket
    When user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir
    And user of browser clicks on "Information" in context menu for "20B-1.txt"
    And user of browser sees physical location path in file details and copies it into the clipboard

    And using REST, user creates S3 bucket "bucket2"
    And using REST, user of browser copies item with recently copied path from "test" bucket into "bucket2" bucket

    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser clicks on "Modify" button for "new_storage1" storage record in Storages page in Onepanel
    And user of browser types "bucket2" to bucket name field in S3 edit form for "new_storage1" storage in Onepanel
    And user of browser types "verySecretKey" to admin secret key field in S3 edit form for "new_storage1" storage in Onepanel
    And user of browser clicks on Save button in edit form for "new_storage1" storage in Onepanel
    And user of browser confirms committed changes in modal "Modify Storage"

    And user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "20B-1.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-1.txt" is equal to: "11111111111111111111"