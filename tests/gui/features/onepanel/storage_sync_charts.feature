Feature: Onepanel features regarding storage sync (e.g. import/update)

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service

    And directory tree structure on local file system:
          browser2:
              - dir1: 500
              - dir2: 300


  Scenario: User configures storage sync and sees storage synchronization statistics
    Given there are no spaces supported in Onepanel used by user of browser1
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
            storage type: POSIX
            mount point: /volumes/persistence/storage
            imported storage: true

    # create space
    When user of browser2 creates "space7" space in Onezone

    And user of browser2 sends support token for "space7" to user of browser1
    And user of browser1 supports "space7" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
                strategy: Simple scan
                max depth: 3

    And user of browser2 copies dir1 to provider's storage mount point
    And user of browser1 is idle for 30 seconds

    # open chart tab
    And user of browser1 clicks on "space7" record in spaces list
    And user of browser1 clicks on storage synchronization tab in space overview page

    # check charts after storage import
    Then user of browser1 clicks on last hour update view
    And user of browser1 sees that number of inserted files for "space7" shown on Synchronization files processing charts equals 501 in Spaces page in Onepanel

    And user of browser1 clicks settings in Storage synchronization in Spaces page
    And user of browser1 sets update configuration in Storage synchronization tab as following:
        storage update:
              strategy: Simple scan
              max depth: 3
              scan interval [s]: 1
              write once: false
              delete enabled: true


    And user of browser2 copies dir2 to provider's storage mount point
    And user of browser1 is idle for 30 seconds

    # check charts after storage update
    And user of browser1 refreshes site
    And user of browser1 clicks on last hour update view
    Then user of browser1 sees that number of inserted files for "space7" shown on Synchronization files processing charts equals 802 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space7" shown on Synchronization files processing charts equals 2 in Spaces page in Onepanel

    And user of browser2 removes dir1 from provider's storage mount point
    And user of browser2 removes dir2 from provider's storage mount point
    And user of browser1 is idle for 30 seconds

    # check charts after storage cleanup
    And user of browser1 refreshes site
    And user of browser1 clicks on last hour update view
    Then user of browser1 sees that number of deleted files for "space7" shown on Synchronization files processing charts equals 802 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space7" shown on Synchronization files processing charts equals 3 in Spaces page in Onepanel

    And user of browser1 revokes "space7" space support in "oneprovider-1" provider in Onepanel
