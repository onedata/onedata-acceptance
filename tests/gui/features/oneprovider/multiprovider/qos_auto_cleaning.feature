Feature: Quality of Service tests for 2 providers using multiple browsers in Oneprovider GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-2 in Onepanel
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1: 11111111

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: User successfully enables auto-cleaning with QoS requirement set
    # enable auto cleaning
    When user of browser_emergency clicks on Spaces item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser_emergency clicks on File popularity navigation tab in space "space1"
    And user of browser_emergency enables file-popularity in "space1" space in Onepanel
    And user of browser_emergency is idle for 8 seconds
    And user of browser_emergency clicks on "Auto cleaning" navigation tab in space "space1"
    And user of browser_emergency enables auto-cleaning in "space1" space in Onepanel

    # upload files
    And user of browser_unified uploads "20B-0.txt" to the root directory of "space1"
    And user of browser_unified uses upload button from file browser menu bar to upload file "large_file.txt" to current dir
    And user of browser_unified clicks on Data in the main menu
    And user of browser_unified creates 2 replicas of "anyStorage" QoS requirement for "large_file.txt" in space "space1"
    And user of browser_unified replicates "20B-0.txt" to provider "oneprovider-2"
    And user of browser_emergency is idle for 8 seconds

    # set soft quota
    And user of browser_emergency clicks change soft quota button in auto-cleaning tab in Onepanel
    And user of browser_emergency types "0.1" to soft quota input field in auto-cleaning tab in Onepanel
    And user of browser_emergency confirms changing value of soft quota in auto-cleaning tab in Onepanel

    # set hard quota
    And user of browser_emergency clicks change hard quota button in auto-cleaning tab in Onepanel
    And user of browser_emergency types "0.2" to hard quota input field in auto-cleaning tab in Onepanel
    And user of browser_emergency confirms changing value of hard quota in auto-cleaning tab in Onepanel

    # start auto-cleaning
    And user of browser_emergency clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
    And user of browser_emergency is idle for 25 seconds

    Then user of browser_emergency sees 20 B released size in cleaning report in Onepanel
    And user of browser_unified sees file chunks for file "large_file.txt" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled
    And user of browser_unified sees file chunks for file "20B-0.txt" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely empty
