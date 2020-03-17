Feature: Basic share management in Oneprovider GUI


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
                    - dir1
                    - dir2:
                        - file1: 11111
                        - file2: 22222
                        - dir3:
                            - file3: 33333
                            - dir4

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

  Scenario: User sees share icon on directory after sharing it
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser

    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"

    And user of browser sees that item named "dir1" is shared 1 time in modal
    And user of browser clicks on "Close" button in modal "Share directory"

    Then user of browser sees that item named "dir1" is shared in file browser


  Scenario: User shares a directory and views information about it (clicks "Share icon" in "Share directory" modal)

    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"

    And user of browser clicks on browser share icon in modal "Share directory"
    And user of browser sees file browser in data tab in Oneprovider page

    Then user of browser sees that item named "dir1" has appeared in file browser on shares page
    And user of browser sees that selected share is named "share_dir1"


  Scenario: User renames share (clicks shares menu in Shares page)
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
#    change page to shares_page
    And user of browser clicks on browser share icon in modal "Share directory"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that selected share is named "share_dir1"
#  rename share
    And user of browser clicks on menu on shares_page
    And user of browser clicks "Rename" option in shares actions row menu in file browser
    And user of browser sees that "Rename share" modal has appeared
    And user of browser writes "renamed_share_dir1" into share name text field in modal "Rename share"
    And user of browser clicks on "Rename" button in modal "Rename share"
    Then user of browser sees that selected share is named "renamed_share_dir1"


  Scenario: User removes share (clicks on Remove option of shares row menu on Shares page, one share only)
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
#    change page to shares_page
    And user of browser clicks on browser share icon in modal "Share directory"
    And user of browser sees file browser in data tab in Oneprovider page
#    remove share
    And user of browser clicks on menu on shares_page
    And user of browser clicks "Remove" option in shares actions row menu in file browser
    And user of browser sees that "Remove share" modal has appeared
    And user of browser clicks on "Remove" button in modal "Remove share"
    Then user of browser sees there are no shares on Shares page



  #new

  Scenario: User removes share (two shares of one directory)
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
#      another share
    And user of browser clicks on "Create another share" button in modal "Share directory"
    And user of browser writes "share2_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser sees that item named "dir1" is shared 2 times in modal
#    change page to shares Page
    And user of browser clicks on browser share icon in modal "Share directory"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that selected share is named "share2_dir1"
#    remove share
    And user of browser clicks on menu on shares_page
    And user of browser clicks "Remove" option in shares actions row menu in file browser
    And user of browser sees that "Remove share" modal has appeared
    And user of browser clicks on "Remove" button in modal "Remove share"

    Then user of browser sees that there is no "share2_dir1" share on Shares Page
    And user of browser sees that there is "share_dir1" share on Shares Page


  Scenario: User removes share from shares browser in Shares page
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
#      another share
    And user of browser clicks on "Create another share" button in modal "Share directory"
    And user of browser writes "share2_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser sees that item named "dir1" is shared 2 times in modal
    And user of browser clicks on "Close" button in modal "Share directory"
#       share page
    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    And user of browser sees that there is "share_dir1" share on Shares Page
    And user of browser sees that there is "share2_dir1" share on Shares Page

    And user of browser clicks on menu for "share_dir1" share in shares browser
    And user of browser clicks "Remove share" option in shares actions row menu in shares browser
    And user of browser sees that "Remove share" modal has appeared
    And user of browser clicks on "Remove" button in modal "Remove share"

    Then user of browser sees that there is no "share_dir1" share on Shares Page
    And user of browser sees that there is "share2_dir1" share on Shares Page




      #new

  Scenario: User renames share from shares browser in Shares page
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

#      share dir1
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir1" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on "Close" button in modal "Share directory"
#       share page
    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    And user of browser sees that there is "share_dir1" share on Shares Page
#       rename share
    And user of browser clicks on menu for "share_dir1" share in shares browser
    And user of browser clicks "Rename" option in shares actions row menu in shares browser
    And user of browser sees that "Rename share" modal has appeared
    And user of browser writes "renamed_share_dir1" into share name text field in modal "Rename share"
    And user of browser clicks on "Rename" button in modal "Rename share"

    Then user of browser sees that there is no "share_dir1" share on Shares Page
    And user of browser sees that there is "renamed_share_dir1" share on Shares Page


  Scenario: User sees new files after adding them to shared directory
   When user of browser clicks "space1" on the spaces list in the sidebar
   And user of browser clicks Data of "space1" in the sidebar
   And user of browser sees file browser in data tab in Oneprovider page
#      share dir1
   And user of browser clicks on menu for "dir1" directory in file browser
   And user of browser clicks "Share" option in data row menu in file browser
   And user of browser sees that "Share directory" modal has appeared
   And user of browser writes "share_dir1" into share name text field in modal "Share directory"
   And user of browser clicks on "Create" button in modal "Share directory"
   And user of browser clicks on "Close" button in modal "Share directory"
#  upload file to shared directory
   And user of browser double clicks on item named "dir1" in file browser
   And user of browser sees that current working directory displayed in breadcrumbs is /dir1
   And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir

   And user of browser clicks Shares of "space1" in the sidebar
   And user of browser sees shares browser in data tab in Oneprovider page
   And user of browser sees that there is "share_dir1" share on Shares Page
   And user of browser clicks "share_dir1" share in shares browser on Shares Page
   And user of browser sees file browser on Shares page
   And user of browser double clicks on item named "dir1" in file browser
   Then user of browser sees that item named "20B-0.txt" has appeared in file browser on shares page



  Scenario: User does not see files in file browser in share view after removing them from shared directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#    share dir2
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir2" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on "Close" button in modal "Share directory"
#       shares page
    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    And user of browser sees that there is "share_dir2" share on Shares Page
    And user of browser clicks "share_dir2" share in shares browser on Shares Page
    And user of browser sees file browser on Shares page
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser sees items named ["dir3", "file1", "file2"] in file browser in given order
#       delete file1
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    And user of browser sees that there is "share_dir2" share on Shares Page
    And user of browser clicks "share_dir2" share in shares browser on Shares Page
    And user of browser sees file browser on Shares page
    And user of browser double clicks on item named "dir2" in file browser
    Then user of browser sees items named ["dir3", "file2"] in file browser in given order


#TODO: wait until gui bug fixed
#Scenario: User can change working directory using breadcrumbs
#    When user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks Data of "space1" in the sidebar
#    And user of browser sees file browser in data tab in Oneprovider page
##    share dir2
#    And user of browser clicks on menu for "dir2" directory in file browser
#    And user of browser clicks "Share" option in data row menu in file browser
#    And user of browser sees that "Share directory" modal has appeared
#    And user of browser writes "share_dir2" into share name text field in modal "Share directory"
#    And user of browser clicks on "Create" button in modal "Share directory"
#    And user of browser clicks on "Close" button in modal "Share directory"
#
#    And user of browser clicks Shares of "space1" in the sidebar
#    And user of browser sees shares browser in data tab in Oneprovider page
#    And user of browser sees that there is "share_dir2" share on Shares Page
#    And user of browser clicks "share_dir2" share in shares browser on Shares Page
#    And user of browser sees file browser on Shares page
#    And user of browser sees that absolute share path visible in share's info header is as follows: /dir2
#    And user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2
#    And user of browser double clicks on item named "dir2" in file browser
#    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2
#    And user of browser double clicks on item named "dir3" in file browser
#    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2/dir3
#    And user of browser double clicks on item named "dir4" in file browser
#    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2/dir3/dir4
#    And user of browser changes current working directory to /dir2 using breadcrumbs from share's file browser
#    Then user of browser sees that current working directory path visible in share's file browser is as follows: /dir2
#    And user of browser changes current working directory to current share using breadcrumbs in shares page
#    Then user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2


Scenario: User can jump to data tab by clicking on dir in breadcrumbs from shared tab
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#    share dir2/dir3
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks on menu for "dir3" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir2_dir3" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on browser share icon in modal "Share directory"
#    on shares page
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that selected share is named "share_dir2_dir3"
    And user of browser sees that absolute share path visible in share's info header is as follows: /dir2/dir3
    And user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2_dir3
    And user of browser double clicks on item named "dir3" in file browser
    And user of browser sees that current working directory path visible in share's file browser is as follows: /dir3
    And user of browser clicks on /dir2 using breadcrumbs from share's info header

    Then user of browser sees "data" icon
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees items named ["dir3", "file1", "file2"] in file browser in given order


Scenario: User downloads files from shared directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
#    share dir2
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir2" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on "Close" button in modal "Share directory"

    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    And user of browser sees that there is "share_dir2" share on Shares Page
    And user of browser clicks "share_dir2" share in shares browser on Shares Page
    And user of browser sees file browser on Shares page
    And user of browser sees that absolute share path visible in share's info header is as follows: /dir2
    And user of browser sees that current working directory path visible in share's file browser is as follows: share_dir2
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser sees that current working directory path visible in share's file browser is as follows: /dir2
    And user of browser double clicks on item named "file1" in file browser

    Then user of browser sees that content of downloaded file "file1" is equal to: "11111"


Scenario: User can remove directory which contains shared directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    #    share dir2/dir3
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks on menu for "dir3" directory in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser sees that "Share directory" modal has appeared
    And user of browser writes "share_dir3" into share name text field in modal "Share directory"
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on browser share icon in modal "Share directory"
#    on shares page
    And user of browser sees files browser in data tab in Oneprovider page
    And user of browser sees that selected share is named "share_dir3"
#    return to data tab
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks on menu for "dir3" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
#    to shares page
    And user of browser clicks Shares of "space1" in the sidebar
    And user of browser sees shares browser in data tab in Oneprovider page
    Then user of browser sees there are no shares on Shares page

