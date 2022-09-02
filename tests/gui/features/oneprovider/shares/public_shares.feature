Feature: Basic operations on public shares in file browser


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
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1
    And user of browser1 clicks and presses enter on item named "dir2" in file browser
    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: /dir1/dir2
    And user of browser1 clicks and presses enter on item named "file2" in file browser
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

    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees "NO SUCH FILE OR DIRECTORY" sign in the file browser
    And user of browser1 refreshes site

    Then user of browser1 sees "Share not found" error


  Scenario: User sees new files in share's public interface after owner added them to shared directory
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 does not see any item(s) named "20B-0.txt" in file browser

    # upload dir1/20B-0.txt
    And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 clicks "Refresh" button from file browser menu bar
    And user of browser1 sees file browser on share's public interface
    Then user of browser1 sees item(s) named "20B-0.txt" in file browser


  Scenario: User does not see file in share's public interface after owner removed them from shared directory
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees item(s) named "file1" in file browser


  Scenario: Share's public interface still works after the only space member left the space containing share
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of space_owner_browser leaves "space1" space in Onezone page

    And user of browser1 refreshes site
    Then user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees item(s) named "file1" in file browser


  Scenario: Public share curl command can be used to get valid share info
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 clicks share link type selector on share's public interface
    And user of browser1 chooses "Public REST endpoint" share link type on share's public interface
    And user of browser1 copies public REST endpoint on share's public interface
    And user of browser1 runs curl command copied from public shares page
    Then user of browser1 sees that curl result matches following config:
           name: share_dir1
           file type: dir


  # TODO: VFS-9761 reimplement gui permissions tests after move to file info modal 
  # Scenario: User fails to download a file in shared directory when the file has "000" POSIX permissions
  #   When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
  #   And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
  #   And user of space_owner_browser sees file browser in files tab in Oneprovider page
  #   And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser

  #   # Space owner user set posix of file1 to 000
  #   And user of space_owner_browser clicks on menu for "file1" file in file browser
  #   And user of space_owner_browser clicks "Permissions" option in data row menu in file browser
  #   And user of space_owner_browser sees that "Edit permissions" modal has appeared
  #   And user of space_owner_browser selects "POSIX" permission type in edit permissions modal
  #   And user of space_owner_browser sets "000" permission code in edit permissions modal
  #   And user of space_owner_browser clicks "Save" confirmation button in displayed modal

  #   # Space owner user hands over shared directory
  #   And user of space_owner_browser changes current working directory to space root using breadcrumbs
  #   And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

  #   # User fails to download file1
  #   And user of browser1 opens received URL
  #   And user of browser1 sees that public share is named "share_dir1"
  #   And user of browser1 sees file browser on share's public interface
  #   And user of browser1 clicks and presses enter on item named "dir1" in file browser
  #   And user of browser1 clicks and presses enter on item named "file1" in file browser
  #   Then user of browser1 sees that error modal with text "Starting file download failed" appeared
