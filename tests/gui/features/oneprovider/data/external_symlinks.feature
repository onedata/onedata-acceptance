Feature: Basic files tab operations on external symlinks in file browser


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
                    - dir2:
                      - dir3:
                        - file1: 1111
                - dir4:
                    - file2: 111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And directory tree structure on local file system:
          browser:
              file3.txt:
                size: 1


  Scenario: User opens directory on space using external symlink modal for symlink pointing outside archive created without "Follow symbolic links"
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks on menu for "dir4" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "dir4" to "symlink_dir4" in "space1"
    And user of browser changes current working directory to space root using breadcrumbs

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        follow symbolic links: False
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in archive file browser
    And user of browser clicks and presses enter on item named "symlink_dir4" in archive file browser
    Then user of browser sees that path where symbolic link points is "space1/dir4" in external symbolic link modal
    And user of browser clicks on "Open" button in modal "External Symbolic Link"
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is /dir4
    And user of browser sees item(s) named file2 in file browser


  Scenario Outline: User navigates inside archive using symlink pointing to location in archive with "Follow symbolic links" set to <follow_sym_links>
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser goes to "/dir1/dir2" in file browser
    And user of browser clicks on menu for "dir3" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser changes current working directory to /dir1 using breadcrumbs
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "dir3" to "symlink_dir3" in "spacec1"
    And user of browser changes current working directory to space root using breadcrumbs

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration and follow symbolic links set as <follow_sym_links>:
        description: first archive
        layout: plain
        follow symbolic links: True
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in archive file browser
    And user of browser clicks and presses enter on item named "symlink_dir3" in archive file browser
    Then user of browser sees item(s) named file1 in archive file browser
    And user of browser sees that current working directory displayed in breadcrumbs on archive file browser is /{current archive}/dir1/symlink_dir3

    Examples:
      | follow_sym_links  |
      | True              |
      | False             |


  Scenario: User downloads file from space using external symlink modal for symlink pointing outside archive created without "Follow symbolic links"
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser uses upload button from file browser menu bar to upload local file "file3.txt" to remote current dir
    And user of browser clicks on menu for "file3.txt" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "file3.txt" to "symlink_file3" in "space1"
    And user of browser changes current working directory to space root using breadcrumbs

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        follow symbolic links: False
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in archive file browser
    And user of browser clicks and presses enter on item named "symlink_file3" in archive file browser
    Then user of browser sees that path where symbolic link points is "space1/file3.txt" in external symbolic link modal
    And user of browser clicks on "Download" button in modal "External Symbolic Link"
    And user of browser sees that content of downloaded file "file3.txt" is equal to: "1"

