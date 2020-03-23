Feature: Oneprovider functionality using multiple providers and multiple browsers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              users:
                  - user2
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
                  - oneprovider-2:
                      storage: posix
                      size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User uploads file on one provider, sees it's distribution, downloads on other provider and again sees it's distribution
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 sees that item named "20B-0.txt" has appeared in file browser

    And user of browser1 is idle for 90 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 clicks on menu for "20B-0.txt" file in file browser
    And user of browser1 clicks "Data distribution" option in data row menu in file browser
    And user of browser1 sees that "Data distribution" modal has appeared
    Then user of browser1 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser1 sees that chunk bar for provider "oneprovider-2" is never synchronized
    And user of browser1 clicks "Close" confirmation button in displayed modal

    And user of browser2 refreshes site
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space1" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page

    And user of browser2 clicks on Choose other Oneprovider on file browser page
    And user of browser2 clicks on "oneprovider-2" provider on file browser page

    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 clicks on menu for "20B-0.txt" file in file browser
    And user of browser2 clicks "Data distribution" option in data row menu in file browser
    And user of browser2 sees that "Data distribution" modal has appeared
    And user of browser2 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser2 sees that chunk bar for provider "oneprovider-2" is never synchronized
    And user of browser2 clicks "Close" confirmation button in displayed modal
    And user of browser2 double clicks on item named "20B-0.txt" in file browser
    And user of browser2 sees that content of downloaded file "20B-0.txt" is equal to: "00000000000000000000"
    And user of browser2 clicks on menu for "20B-0.txt" file in file browser
    And user of browser2 clicks "Data distribution" option in data row menu in file browser
    And user of browser2 sees that "Data distribution" modal has appeared
    And user of browser2 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser2 sees that chunk bar for provider "oneprovider-2" is entirely filled

    And user of browser1 is idle for 90 seconds
    And user of browser1 clicks on menu for "20B-0.txt" file in file browser
    And user of browser1 clicks "Data distribution" option in data row menu in file browser
    And user of browser1 sees that "Data distribution" modal has appeared
    And user of browser1 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser1 sees that chunk bar for provider "oneprovider-2" is entirely filled
    And user of browser1 clicks "Close" confirmation button in displayed modal
