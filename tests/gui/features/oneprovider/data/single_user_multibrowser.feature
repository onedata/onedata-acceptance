Feature: Basic files operations in multibrowser with single user

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
                    - file1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user1] to [Onezone, Onezone] service

  Scenario: User deletes a file in one tab and then in another tab after refreshing can see appropriate error message
    When user of browser1 opens file browser for "space1" space

    And user of browser2 opens file browser for "space1" space

    And user of browser1 goes to "/dir1" in file browser

    And user of browser2 clicks on menu for "dir1" file in file browser
    And user of browser2 clicks "Delete" option in data row menu in file browser
    And user of browser2 clicks on "Yes" button in modal "Delete modal"

    Then user of browser1 sees "NO SUCH FILE OR DIRECTORY" sign in the file browser

    And user of browser1 refreshes site
    And user of browser1 sees file browser in files tab in Oneprovider page

    And user of browser1 clicks on "navigate to root directory" button
    And user of browser1 does not see any item(s) named "dir1" in file browser
