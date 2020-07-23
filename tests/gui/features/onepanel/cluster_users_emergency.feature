Feature: Adding and removing users of cluster using emergency interface


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: Invite member to cluster
    When user of browser_emergency clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency clicks on "Invite user using token" button on cluster members page
    And user of browser_emergency clicks on "Copy" button on cluster members page
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified does not see "oneprovider-1" in clusters menu
    And user of browser_unified clicks on Tokens in the main menu
    And user of browser_unified clicks on "Consume token" button in tokens sidebar
    And user of browser_unified pastes copied token into token text field
    And user of browser_unified clicks on Join button on consume token page
    Then user of browser_emergency refreshes site
    And user of browser_unified clicks on Clusters in the main menu
    And user of browser_unified sees "oneprovider-1" in clusters menu
    And user of browser_emergency sees that number of direct users is equal 2 on cluster members page

