Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, Onezone] service


  Scenario: User supports space by two providers and sees that there are two provider in file browser
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When user of browser1 sends support token for "space1" to user of browser2
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-2" in clusters menu
    And user of browser2 supports "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of browser1 sends support token for "space1" to user of browser2
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    Then user of browser1 sees current provider named "oneprovider-1" on file browser page
    And user of browser1 clicks on Choose other Oneprovider on file browser page
    And user of browser1 sees provider named "oneprovider-2" on file browser page
    And user of browser1 clicks on "oneprovider-2" provider on file browser page
