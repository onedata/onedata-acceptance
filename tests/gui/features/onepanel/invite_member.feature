Feature: Inviting member to cluster

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service

  Scenario: User increases number of members in cluster
    When user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on "Invite user using token" button on cluster members page
    And user of browser2 clicks on "Copy" button on cluster members page
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 does not see "oneprovider-1" in clusters menu
    And user of browser1 clicks on Tokens in the main menu
    And user of browser1 clicks on "Consume token" button in tokens sidebar
    And user of browser1 pastes copied token into token text field
    And user of browser1 clicks on Join button on consume token page
    And user of browser2 refreshes site
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 sees "oneprovider-1" in clusters menu
    Then user of browser2 sees that number of direct users is equal 2 on cluster members page

