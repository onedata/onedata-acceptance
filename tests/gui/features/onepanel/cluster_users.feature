Feature: Adding and removing users of cluster using emergency interface


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And users opened [browser_standard, browser_admin] browsers' windows
    And users of [browser_standard, browser_admin] opened [Onezone, Onezone] page
    And user of [browser_standard, browser_admin] logged as [user1, admin] to [Onezone, Onezone] service


  Scenario: User successfully invites other user to cluster
    When user of browser_admin clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_admin clicks on Clusters in the main menu
    And user of browser_admin clicks on "Invite user using token" button on cluster members page
    And user of browser_admin clicks on "Copy" button on cluster members page
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard does not see "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Tokens in the main menu
    And user of browser_standard clicks on "Consume token" button in tokens sidebar
    And user of browser_standard pastes copied token into token text field
    And user of browser_standard clicks on Join button on consume token page
    Then user of browser_admin refreshes site
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard sees "oneprovider-1" in clusters menu
    And user of browser_admin sees that number of direct users is equal 2 on cluster members page
