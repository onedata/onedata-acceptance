Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - space-owner-user

    # unused_space is used only to introduce "oneprovider-1" for use of space-owner-user
    # thanks to this "oneprovider-1" is listed in consumer caveats popup
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
          unused_space:
            owner: space-owner-user
            providers:
            - oneprovider-1:
                storage: posix
                size: 1000000

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And user of [space_owner_browser, browser1] logged as [space-owner-user, admin] to [Onezone, Onezone] service


  Scenario: User supports space by two providers and sees that there are two provider in file browser
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When user of space_owner_browser sends support token for "space1" to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-2" in clusters menu
    And user of browser1 supports "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of space_owner_browser sends support token for "space1" to user of browser1
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of space_owner_browser clicks Data of "space1" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser clicks on Choose other Oneprovider on file browser page
    Then user of space_owner_browser sees provider named "oneprovider-1" on file browser page
    And user of space_owner_browser sees provider named "oneprovider-2" on file browser page
    And user of space_owner_browser clicks on "oneprovider-2" provider on file browser page


  Scenario: Provider fails to support space using invite token with consumer caveat set not for them
    When user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Support space
          invite target: space1
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-2" in clusters menu
    Then user of browser1 fails to support "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
