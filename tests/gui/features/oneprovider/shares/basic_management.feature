Feature: Basic share management in Oneprovider GUI


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
                    - dir1
                    - dir2:
                        - file1: 11111
                        - file2: 22222
                        - dir3:
                            - file3: 33333
                            - dir4

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees shared status tag for directory after sharing it
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share / Publish" option in data row menu in file browser
    And user of browser sees that "Share / Publish directory" modal has appeared
    And user of browser writes "share_dir1" into text field in modal "Share / Publish directory"
    And user of browser clicks on "Create" button in modal "Share / Publish directory"

    And user of browser sees that item named "dir1" is shared 1 time in modal
    And user of browser clicks on "X" button in modal "Directory details"

    Then user of browser sees shared status tag for "dir1" in file browser
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 1


  Scenario: User shares a directory and opens its view in full Onezone interface from modal
    When user of browser opens file browser for "space1" space
    And user of browser creates "share_dir1" share of "dir1" directory
    And user of browser clicks on "Show details" link for "share_dir1" share in shares panel
    And user of browser sees file browser in files tab in Oneprovider page
    Then user of browser sees that item named "dir1" has appeared in file browser on single share view
    And user of browser sees that selected share is named "share_dir1"


  Scenario: User creates two shares of one directory and sees them in shares view
    When user of browser opens file browser for "space1" space
    And user of browser creates "share_dir1" share of "dir1" directory

    # create another share
    And user of browser clicks on "Create another share" button in shares panel
    And user of browser writes "share2_dir1" into text field in modal "Share / Publish directory"
    And user of browser clicks on "Create" button in modal "Share / Publish directory"
    Then user of browser sees that item named "dir1" is shared 2 times in modal

    # open shares view
    And user of browser clicks on "X" button in modal "Directory details"
    And user of browser clicks "Shares, Open Data" of "space1" space in the sidebar
    And user of browser sees shares browser in files tab in Oneprovider page
    Then user of browser sees that there is "share_dir1" share on shares view
    And user of browser sees that there is "share2_dir1" share on shares view
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 2


  Scenario: User opens share panel using shared status tag
    Given using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks on shared status tag for "dir1" in file browser
    Then user of browser sees that "Directory details" modal is opened on "Shares" tab
    And user of browser sees that item named "dir1" is shared 1 time in modal


  Scenario: User renames share from single share view
    Given using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir1" single share view of "dir1" using "Shared" tag

    # rename share
    And user of browser clicks on menu on share view
    And user of browser clicks "Rename" option in shares actions row menu
    And user of browser sees that "Rename share" modal has appeared
    And user of browser writes "renamed_share_dir1" into text field in modal "Rename share"
    And user of browser clicks on "Rename" button in modal "Rename share"
    Then user of browser sees that selected share is named "renamed_share_dir1"


  Scenario: User removes share from single share view
    Given using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir1" single share view of "dir1" using "Shared" tag

    # remove share
    And user of browser clicks on menu on share view
    And user of browser clicks "Remove" option in shares actions row menu
    And user of browser sees that "Remove share" modal has appeared
    And user of browser clicks on "Remove" button in modal "Remove share"
    Then user of browser sees there are no shares on shares view
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 0


  Scenario: User removes one of two shares of directory from single share view
    Given using REST, user space-owner-user creates following shares:
         - name: share_dir1
           path: space1/dir1
           provider: oneprovider-1
         - name: share2_dir1
           path: space1/dir1
           provider: oneprovider-1
    When user of browser opens file browser for "space1" space

    And user of browser opens "share2_dir1" single share view of "dir1" using "Shared" tag

    And user of browser removes current share
    Then user of browser sees that there is no "share2_dir1" share on shares view
    And user of browser sees that there is "share_dir1" share on shares view
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 1


  Scenario: User removes share using shares browser
    Given using REST, user space-owner-user creates following shares:
          - name: share_dir1
            path: space1/dir1
            provider: oneprovider-1
          - name: share2_dir1
            path: space1/dir1
            provider: oneprovider-1
    When user of browser opens file browser for "space1" space

    And user of browser opens shares view of "space1"

    And user of browser clicks on menu for "share_dir1" share in shares browser
    And user of browser clicks "Remove share" option in shares actions row menu in shares browser
    And user of browser sees that "Remove share" modal has appeared
    And user of browser clicks on "Remove" button in modal "Remove share"

    Then user of browser sees that there is no "share_dir1" share on shares view
    And user of browser sees that there is "share2_dir1" share on shares view
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 1


  Scenario: User renames share using shares browser
    Given using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space

    And user of browser opens shares view of "space1"

    # rename share
    And user of browser clicks on menu for "share_dir1" share in shares browser
    And user of browser clicks "Rename" option in shares actions row menu in shares browser
    And user of browser sees that "Rename share" modal has appeared
    And user of browser writes "renamed_share_dir1" into text field in modal "Rename share"
    And user of browser clicks on "Rename" button in modal "Rename share"

    Then user of browser sees that there is no "share_dir1" share on shares view
    And user of browser sees that there is "renamed_share_dir1" share on shares view


  Scenario: User sees new files in single share view in full Onezone interface after adding them to shared directory
    Given using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space

    # upload file to shared directory
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1/dir1"
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir

    And user of browser opens shares view of "space1"
    And user of browser clicks "share_dir1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks and presses enter on item named "dir1" in file browser
    Then user of browser sees that item named "20B-0.txt" has appeared in file browser on single share view


  Scenario: User does not see files in single share view in full Onezone interface after removing them from shared directory
    Given using REST, user space-owner-user creates "share_dir2" share of "space1/dir2" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir2" single share view of "dir2" using "Shared" tag
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser sees only items named ["dir3", "file1", "file2"] in file browser

    # delete file1
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser opens "share_dir2" single share view of space "space1" using sidebar
    And user of browser clicks and presses enter on item named "dir2" in file browser
    Then user of browser sees only items named ["dir3", "file2"] in file browser


  Scenario: User can change working directory using breadcrumbs
    Given using REST, user space-owner-user creates "share_dir2" share of "space1/dir2" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir2" single share view of "dir2" using "Shared" tag

    And user of browser sees that absolute share path visible in share's info header is as follows: space1/dir2
    And user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2
    And user of browser clicks and presses enter on item named "dir2" in file browser
    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2
    And user of browser clicks and presses enter on item named "dir3" in file browser
    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2/dir3
    And user of browser clicks and presses enter on item named "dir4" in file browser
    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2/dir3/dir4
    And user of browser changes current working directory to /dir2 using breadcrumbs from share's file browser
    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2
    And user of browser changes current working directory to current share using breadcrumbs from share's file browser
    Then user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2


  Scenario: User can jump to files tab using breadcrumbs in single share view in full Onezone interface
    Given using REST, user space-owner-user creates "share_dir2_dir3" share of "space1/dir2/dir3" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser opens "share_dir2_dir3" single share view of "dir3" using "Shared" tag

    And user of browser sees that absolute share path visible in share's info header is as follows: space1/dir2/dir3
    And user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2_dir3
    And user of browser clicks and presses enter on item named "dir3" in file browser
    And user of browser sees that current working directory path visible in share's file browser is as follows: /dir3
    And user of browser clicks on /dir2 using breadcrumbs from share's info header

    Then user of browser sees "files" label of current page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees only items named ["dir3", "file1", "file2"] in file browser


  Scenario: User downloads files from shared directory on single share view in full Onezone interface
    Given using REST, user space-owner-user creates "share_dir2" share of "space1/dir2" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir2" single share view of "dir2" using "Shared" tag

    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user browser is idle for 5 seconds
    # Step below is a quick-fix caused by click and enter not working properly while downloading "file1.txt"
    Then user of browser downloads item "file1" by clicking and pressing enter and then sees that content of downloaded file is equal to: "11111"


  Scenario: User can remove share by removing shared directory
    Given using REST, user space-owner-user creates "share_dir2" share of "space1/dir2" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens "share_dir2" single share view of "dir2" using "Shared" tag

    And user of browser opens shares view of "space1"
    And user of browser sees that there is "share_dir2" share on shares view

    # delete dir2
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser opens shares view of "space1"
    Then user of browser sees there are no shares on shares view
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 0


  Scenario: Removing directory which contained shared directory removes only share's files but not share itself
    Given using REST, user space-owner-user creates "share_dir3" share of "space1/dir2/dir3" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser opens shares view of "space1"
    And user of browser sees that there is "share_dir3" share on shares view

    # delete dir2
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser opens shares view of "space1"
    Then user of browser sees that there is "share_dir3" share that points to deleted directory on shares view
    And user of browser clicks "share_dir3" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser sees "SHARED FILES HAVE BEEN DELETED" instead of file browser

    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees in the INFO section of Overview page that number of shares is 1


  Scenario: Share curl command can be used to get valid share info
    Given using REST, user space-owner-user creates "share_file1" share of "space1/dir2/file1" supported by "oneprovider-1" provider
    When user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser opens "share_file1" single share view of "file1" using "Shared" tag

    And user of browser clicks share link type selector on shares view
    And user of browser chooses "Public REST endpoint" share link type on shares view
    And user of browser copies public REST endpoint on shares view
    And user of browser runs curl command copied from shares page
    Then user of browser sees that curl result matches following config:
          name: share_file1
          file type: file