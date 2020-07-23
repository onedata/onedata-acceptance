Feature: Basic data tab operations on public shares in file browser


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
                        - dir2:
                            - file2: 22222

    And users opened [browser1, browser2] browsers' windows
    And user of browser1 opened onezone page
    And user of browser1 logged as user1 to Onezone service



  Scenario: User views and downloads files from public interface of share shared from another user from "Share directory" modal
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory

    # hand share_dir1 URL to user of browser2
    And user of browser1 clicks on copy icon in modal "Share directory"
    And user of browser1 sends copied URL to user of browser2
    And user of browser1 clicks on "Close" button in modal "Share directory"

    # opening share by user of browser2
    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"

    # find and download file2
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser2 double clicks on item named "dir2" in file browser
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: /dir1/dir2
    And user of browser2 double clicks on item named "file2" in file browser
    Then user of browser2 sees that content of downloaded file "file2" is equal to: "22222"


  Scenario: User sees public URLs of share are equal
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 clicks on copy icon in modal "Share directory"
    And user of browser1 moves to "share_dir1" single share view using modal icon
    Then user of browser1 sees that share's URL is the same as URL from clipboard


  Scenario: User sees that share name in public interface has changed after owner renamed it
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"

    And user of browser1 moves to "share_dir1" single share view using sidebar
    And user of browser1 renames current share to "renamed_share_dir1" in single share view

    And user of browser2 refreshes site
    Then user of browser2 sees that public share is named "renamed_share_dir1"


  Scenario: User sees that he no longer can view public share after owner removed it
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"

    And user of browser1 moves to "share_dir1" single share view using sidebar
    And user of browser1 removes current share

    And user of browser2 refreshes site
    Then user of browser2 sees "The resource could not be found" error


  Scenario: User sees new files in share's public interface after owner added them to shared directory
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 does not see any item(s) named "20B-0.txt" in file browser

    # upload dir1/20B-0.txt
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir

    And user of browser2 refreshes site
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    Then user of browser2 sees item(s) named "20B-0.txt" in file browser


  Scenario: User does not see file in share's public interface after owner removed them from shared directory
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 sees item(s) named "file1" in file browser

    And user of browser1 succeeds to remove "dir1/file1" in "space1"

    And user of browser2 refreshes site
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    Then user of browser2 does not see any item(s) named "file1" in file browser


  Scenario: User changes working directory using breadcrumbs from file browser in share's public interface
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1
    And user of browser2 sees file browser on share's public interface
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser2 double clicks on item named "dir2" in file browser
    And user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: /dir1/dir2

    # using breadcrumbs
    And user of browser2 changes current working directory to /dir1 using breadcrumbs on share's public interface
    Then user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser2 changes current working directory to current share using breadcrumbs on share's public interface
    Then user of browser2 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1


  Scenario: User can copy URL of received share on share's public interface and share it further
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page

    And user of browser1 creates "share_dir1" share of "dir1" directory
    And user of browser1 hands "share_dir1" share's URL to user of browser2 using modal

    And user of browser2 opens received URL
    And user of browser2 sees that public share is named "share_dir1"
    And user of browser2 copies URL

    Then user of browser2 sends copied URL to user of browser1
    And user of browser1 opens URL received from user of browser2
    And user of browser1 sees that public share is named "share_dir1"
