Feature: Storage s3 management using onepanel, REST


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-1 in Onepanel

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User sees actual space content after copying it into another location and changing s3 bucket for storage
    When user of browser creates "space1" space in Onezone

    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    And user of browser clicks on Add storage backend button in storages page in Onepanel
    And user of browser selects s3 from storage selector in storages page in Onepanel
    And user of browser types "new_storage1" to Storage name field in s3 form in storages page in Onepanel
    And user of browser types "http://volume-s3.dev-volume-s3-krakow.default:9000" to hostname field in s3 form in storages page in Onepanel
    And user of browser types "test" to bucket name field in s3 form in storages page in Onepanel
    And user of browser types "accessKey" to admin access key field in s3 form in storages page in Onepanel
    And user of browser types "verySecretKey" to admin secret key field in s3 form in storages page in Onepanel
    And user of browser clicks on Add button in add storage form in storages page in Onepanel
    And user of browser sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser sends support token for "space1" to user of browser

    # support space
    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage1
          size: 1
          unit: GiB

    And user of browser sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser sees that space support record for "space1" has appeared in Spaces page in Onepanel

    And user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir
    And user of browser clicks on "Information" in context menu for "20B-1.txt"
    And user of browser sees physical location path in file details and copies it into the clipboard

    And using REST, user creates s3 bucket "bucket2"
    And using REST, user of browser copies item with recently copied path from "test" bucket into "bucket2" bucket

    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Storage backends item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser is idle for 2 seconds

    And user of browser clicks on "Modify" button for "new_storage1" storage record in Storages page in Onepanel
    And user of browser types "bucket2" to bucket name field in s3 edit form for "new_storage1" storage in Onepanel
    And user of browser types "verySecretKey" to admin secret key field in s3 edit form for "new_storage1" storage in Onepanel
    And user of browser clicks on Save button in edit form for "new_storage1" storage in Onepanel
    And user of browser confirms committed changes in modal "Modify Storage"

    And user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "20B-1.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-1.txt" is equal to: "11111111111111111111"