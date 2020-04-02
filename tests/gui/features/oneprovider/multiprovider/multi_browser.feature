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
    And opened oneprovider-1 Oneprovider file browser for "space1" space in web GUI by users of browser1


  Scenario: User uploads file on one provider, sees it's distribution, downloads on other provider and again sees it's distribution
    When user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 sees that item named "20B-0.txt" has appeared in file browser

    And user of browser1 is idle for 90 seconds
    Then user of browser1 sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 double clicks on item named "20B-0.txt" in file browser
    And user of browser2 sees that content of downloaded file "20B-0.txt" is equal to: "00000000000000000000"
    And user of browser2 sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    And user of browser1 is idle for 90 seconds
    And user of browser2 sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
