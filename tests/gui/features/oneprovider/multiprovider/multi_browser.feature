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
    And users of [browser1, browser2] logged as [user1, user2] to Onezone service
    And opened [oneprovider-1, oneprovider-2] Oneprovider view in web GUI by users of [browser1, browser2]


  Scenario: User uploads file on one provider, sees it's distribution, downloads on other provider and again sees it's distribution
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 sees that current working directory displayed in breadcrumbs is space1
    And user of browser1 uses upload button in toolbar to upload file "20B-0.txt" to current dir
    And user of browser1 sees an info notify with text matching to: .*[Cc]ompleted upload.*1.*
    And user of browser1 sees that item named "20B-0.txt" has appeared in file browser

    And user of browser1 is idle for 90 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 clicks once on item named "20B-0.txt" in file browser
    And user of browser1 clicks the button from top menu bar with tooltip "Show data distribution"
    And user of browser1 sees that "data distribution" modal has appeared
    Then user of browser1 sees that chunk bar for provider "oneprovider-1" is entirely filled
    # TODO: uncomment when empty chunk bar will be displayed in GUI
    # And user of browser1 sees that chunk bar for provider "oneprovider-2" is entirely empty
    And user of browser1 clicks "Close" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    And user of browser2 refreshes site
    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees that current working directory displayed in breadcrumbs is space1
    And user of browser2 clicks once on item named "20B-0.txt" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Show data distribution"
    And user of browser2 sees that "data distribution" modal has appeared
    And user of browser2 sees that chunk bar for provider "oneprovider-1" is entirely filled
    # TODO: uncomment when empty chunk bar will be displayed in GUI
    # And user of browser2 sees that chunk bar for provider "oneprovider-2" is entirely empty
    And user of browser2 clicks "Close" confirmation button in displayed modal
    And user of browser2 sees that the modal has disappeared
    And user of browser2 double clicks on item named "20B-0.txt" in file browser
    And user of browser2 sees that content of downloaded file "20B-0.txt" is equal to: "00000000000000000000"

    And user of browser2 clicks once on item named "20B-0.txt" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Show data distribution"
    And user of browser2 sees that "data distribution" modal has appeared
    And user of browser2 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser2 sees that chunk bar for provider "oneprovider-2" is entirely filled

    And user of browser1 is idle for 90 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 clicks once on item named "20B-0.txt" in file browser
    And user of browser1 clicks the button from top menu bar with tooltip "Show data distribution"
    And user of browser1 sees that "data distribution" modal has appeared
    And user of browser1 sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser1 sees that chunk bar for provider "oneprovider-2" is entirely filled
    And user of browser1 clicks "Close" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared
