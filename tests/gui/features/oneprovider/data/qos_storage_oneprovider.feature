Feature: Quality of Service tests for 1 provider using multiple browsers in Oneprovider GUI


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
          storage:
            defaults:
              provider: oneprovider-1
            directory tree:
              - file1: 11111111

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service
    And user of browser_emergency clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And there are no additional params in QoS parameters form in storage edit page used by browser_emergency


  Scenario: A QoS requirement is met when parameter is added to storage after defining the requirement
    When user of browser_unified creates "type2=posix2" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_unified sees that no storage matches condition in QoS panel
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type2" value="posix2" in QoS parameters form in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified sees that 1 storage matches condition in QoS panel
    And user of browser_unified sees that matching storage is "posix provided by oneprovider-1"


  Scenario: A QoS requirement with "and" operator is met when all joined conditions are met
    When user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in QoS parameters form in storage edit page
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="geo" value="PL" in QoS parameters form in storage edit page
    And user of browser_unified creates "type=posix & geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    Then user of browser_unified sees that all QoS requirements are fulfilled


  # TODO: VFS-6004 Wait for implementation: Allow for changing storage qos parameters
  # Scenario: A QoS requirement is met after removing the parameter and adding it again
  #   When user of browser_unified creates "geo=PL" QoS requirement for "file1" in space "space1"
  #   And user of browser_unified clicks on QoS status tag for "file1" in file browser
  #   And user of browser_unified sees that all QoS requirements are impossible
  #   And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
  #   And user of browser_emergency adds key="geo" value="PL" in QoS parameters form in storage edit page
  #   And user of browser_unified sees that all QoS requirements are fulfilled
  #   And user of browser_emergency deletes all additional params in QoS parameters form in storage edit page
  #   And user of browser_unified sees that all QoS requirements are impossible
  #   And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
  #   And user of browser_emergency adds key="geo" value="PL" in QoS parameters form in storage edit page
  #   Then user of browser_unified sees that all QoS requirements are fulfilled


  Scenario: A QoS requirement with "or" operator is met when at least one of the conditions is met
    When user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in QoS parameters form in storage edit page
    And user of browser_unified creates "type=posix | geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    Then user of browser_unified sees that all QoS requirements are fulfilled

