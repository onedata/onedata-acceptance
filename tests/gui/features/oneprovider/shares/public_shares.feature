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



    Scenario: User views and downloads files from public share (using copy icon from "Share directory" modal)
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
#      public share_dir1
      And user of browser1 clicks on copy icon in modal "Share directory"
      And user of browser1 sends copied URL to user of browser2
      And user of browser1 clicks on "Close" button in modal "Share directory"
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"

      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: share_dir1
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      And user of browser2 double clicks on item named "dir2" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1/dir2
      And user of browser2 double clicks on item named "file2" in file browser
      Then user of browser2 sees that content of downloaded file "file2" is equal to: "22222"


    Scenario: User sees that public share name has changed after other user renamed it
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
      And user of browser1 clicks on browser share icon in modal "Share directory"
      And user of browser1 sees file browser in data tab in Oneprovider page
      And user of browser1 sees that selected share is named "share_dir1"
#      public share_dir1
      And user of browser1 clicks on copy icon on shares page
      And user of browser1 sends copied URL to user of browser2
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
#      user of browser1 renames share
      And user of browser1 clicks on menu on shares_page
      And user of browser1 clicks "Rename" option in shares actions row menu in file browser
      And user of browser1 sees that "Rename share" modal has appeared
      And user of browser1 writes "renamed_share_dir1" into share name text field in modal "Rename share"
      And user of browser1 clicks on "Rename" button in modal "Rename share"
      And user of browser1 sees that selected share is named "renamed_share_dir1"

      And user of browser2 refreshes site
      Then user of browser2 sees that public share is named "renamed_share_dir1"

    Scenario: User sees that he no longer can view public share after other user removed it
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
  #      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
      And user of browser1 clicks on browser share icon in modal "Share directory"
      And user of browser1 sees file browser in data tab in Oneprovider page
      And user of browser1 sees that selected share is named "share_dir1"
#      public share_dir1
      And user of browser1 clicks on copy icon on shares page
      And user of browser1 sends copied URL to user of browser2
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
#      remove share_dir1
      And user of browser1 clicks on menu on shares_page
      And user of browser1 clicks "Remove" option in shares actions row menu in file browser
      And user of browser1 sees that "Remove share" modal has appeared
      And user of browser1 clicks on "Remove" button in modal "Remove share"
      And user of browser1 sees there are no shares on Shares page

      And user of browser2 refreshes site
      Then user of browser2 sees "The resource could not be found" error


    Scenario: User sees new files in public share view after other user added them to shared directory
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
#      public share_dir1
      And user of browser1 clicks on copy icon in modal "Share directory"
      And user of browser1 sends copied URL to user of browser2
      And user of browser1 clicks on "Close" button in modal "Share directory"
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: share_dir1
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      And user of browser2 does not see any item(s) named "20B-0.txt" in file browser
#       upload dir1/20B-0.txt
      And user of browser1 double clicks on item named "dir1" in file browser
      And user of browser1 sees that current working directory displayed in breadcrumbs is /dir1
      And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir

      And user of browser2 refreshes site
      And user of browser2 sees that public share is named "share_dir1"
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      Then user of browser2 sees item(s) named "20B-0.txt" in file browser


    Scenario: User does not see file in public share view after other user removed them from shared directory
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
#      public share_dir1
      And user of browser1 clicks on copy icon in modal "Share directory"
      And user of browser1 sends copied URL to user of browser2
      And user of browser1 clicks on "Close" button in modal "Share directory"
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: share_dir1
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      And user of browser2 sees item(s) named "file1" in file browser
#       remove dir1/file1
      And user of browser1 double clicks on item named "dir1" in file browser
      And user of browser1 clicks on menu for "file1" file in file browser
      And user of browser1 clicks "Delete" option in data row menu in file browser
      And user of browser1 clicks on "Yes" button in modal "Delete modal"

      And user of browser2 refreshes site
      And user of browser2 sees that public share is named "share_dir1"
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      Then user of browser2 does not see any item(s) named "file1" in file browser


#  TODO: wait until gui bug fixed
    Scenario: User changes working directory using breadcrumbs from file browser in public share view
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
#      public share_dir1
      And user of browser1 clicks on copy icon in modal "Share directory"
      And user of browser1 sends copied URL to user of browser2
      And user of browser1 clicks on "Close" button in modal "Share directory"
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: share_dir1
      And user of browser2 sees file browser in public share page
      And user of browser2 double clicks on item named "dir1" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      And user of browser2 double clicks on item named "dir2" in file browser
      And user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1/dir2
#      jumping using breadcrumbs
      And user of browser2 changes current working directory to /dir1 using breadcrumbs on public share page
      Then user of browser2 sees that current working directory path visible in public share's file browser is as follows: /dir1
      And user of browser2 changes current working directory to current share using breadcrumbs on public share page
      Then user of browser2 sees that current working directory path visible in public share's file browser is as follows: share_dir1


    Scenario: User can copy url of received share and share it further
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
#      share dir1
      And user of browser1 clicks on menu for "dir1" directory in file browser
      And user of browser1 clicks "Share" option in data row menu in file browser
      And user of browser1 sees that "Share directory" modal has appeared
      And user of browser1 writes "share_dir1" into share name text field in modal "Share directory"
      And user of browser1 clicks on "Create" button in modal "Share directory"
#      public share_dir1
      And user of browser1 clicks on copy icon in modal "Share directory"
      And user of browser1 sends copied URL to user of browser2
      And user of browser1 clicks on "Close" button in modal "Share directory"
#      user of browser2
      And user of browser2 opens received URL
      And user of browser2 sees that public share is named "share_dir1"
#      copy link
      And user of browser2 clicks on copy icon on public share page
      Then user of browser2 sends copied URL to user of browser1
#      user of browser 1 opens url
      And user of browser1 opens received URL
      And user of browser1 sees that public share is named "share_dir1"