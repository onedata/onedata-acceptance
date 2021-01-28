Feature: Basic data tab operations on public shares in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
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
                        - dir2:
                            - file2: 22222

    And users opened [space_owner_browser, browser1] browsers' windows
    And user of space_owner_browser opened onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service
    And using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider


  Scenario: User views and downloads files from public interface of share shared from another user from "Share directory" modal
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    # opening share by user of browser1
    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"

    # find and download file2
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1
    And user of browser1 sees file browser on share's public interface
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser1 double clicks on item named "dir2" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1/dir2
    And user of browser1 double clicks on item named "file2" in file browser
    Then user of browser1 sees that content of downloaded file "file2" is equal to: "22222"


  Scenario: User sees public URLs of share are equal
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser copies share URL of "share_dir1" share of "dir1"
    And user of space_owner_browser opens "share_dir1" single share view of "dir1" using modal icon
    Then user of space_owner_browser sees that share's URL is the same as URL from clipboard


  Scenario: User sees that share name in public interface has changed after owner renamed it
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"

    And user of space_owner_browser opens "share_dir1" single share view of space "space1" using sidebar
    And user of space_owner_browser renames current share to "renamed_share_dir1" in single share view
    And user of browser1 refreshes site

    Then user of browser1 sees that public share is named "renamed_share_dir1"


  Scenario: User sees that he no longer can view public share after owner removed it
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"

    And user of space_owner_browser opens "share_dir1" single share view of space "space1" using sidebar
    And user of space_owner_browser removes current share

    And user of browser1 refreshes site

    Then user of browser1 sees "The resource could not be found" error


  Scenario: User sees new files in share's public interface after owner added them to shared directory
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 does not see any item(s) named "20B-0.txt" in file browser

    # upload dir1/20B-0.txt
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 clicks file browser refresh button
    And user of browser1 sees file browser on share's public interface
    Then user of browser1 sees item(s) named "20B-0.txt" in file browser


  Scenario: User does not see file in share's public interface after owner removed them from shared directory
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 sees item(s) named "file1" in file browser

    And user of space_owner_browser succeeds to remove "dir1/file1" in "space1"

    And user of browser1 clicks file browser refresh button
    And user of browser1 sees file browser on share's public interface
    Then user of browser1 does not see any item(s) named "file1" in file browser


  Scenario: User changes working directory using breadcrumbs from file browser in share's public interface
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1
    And user of browser1 sees file browser on share's public interface
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser1 double clicks on item named "dir2" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1/dir2

    # using breadcrumbs
    And user of browser1 changes current working directory to /dir1 using breadcrumbs on share's public interface
    Then user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser1 changes current working directory to current share using breadcrumbs on share's public interface
    Then user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1


  Scenario: User can copy URL of received share on share's public interface and share it further
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 copies URL

    Then user of browser1 sends copied URL to user of space_owner_browser
    And user of space_owner_browser opens URL received from user of browser1
    And user of space_owner_browser sees that public share is named "share_dir1"


  Scenario: Share owner description changes are visible on share's public interface
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of space_owner_browser opens "share_dir1" single share view of space "space1" using sidebar

    # create description
    And user of space_owner_browser opens description tab on share view
    And user of space_owner_browser clicks on add description button on share description tab
    And user of space_owner_browser appends "##use this share with responsibility" to description on share description tab
    And user of space_owner_browser clicks on save changes button in description share

    And user of browser1 refreshes site
    And user of browser1 opens description tab on share's public interface
    And user of browser1 sees "use this share with responsibility" description on share's public interface

    # update description
    And user of space_owner_browser appends " and joy" to description on share description tab
    And user of space_owner_browser clicks on save changes button in description share
    And user of browser1 refreshes site
    And user of browser1 opens description tab on share's public interface
    And user of browser1 sees "use this share with responsibility and joy" description on share's public interface


  Scenario: User sees appropriate message on share's public interface when directory containing shared file was deleted
    When using REST, user space-owner-user creates "share_dir2" share of "space1/dir1/dir2" supported by "oneprovider-1" provider
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser hands "share_dir2" share's URL of "dir2" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir2"

    # delete dir1
    And user of space_owner_browser clicks Data of "space1" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" directory in file browser
    And user of space_owner_browser clicks "Delete" option in data row menu in file browser
    And user of space_owner_browser clicks on "Yes" button in modal "Delete modal"

    And user of browser1 refreshes site
    And user of browser1 sees "SHARED FILES HAVE BEEN DELETED" instead of file browser on share's public interface


  Scenario: User cannot see share's public interface when space containing shared file was deleted
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of space_owner_browser removes "space1" space in Onezone page

    And user of browser1 refreshes site
    Then user of browser1 sees "web GUI cannot be loaded" error on Onedata page


  Scenario: Share's public interface still works after share owner left the space containing share
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of space_owner_browser leaves "space1" space in Onezone page

    And user of browser1 refreshes site
    Then user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 sees item(s) named "file1" in file browser
