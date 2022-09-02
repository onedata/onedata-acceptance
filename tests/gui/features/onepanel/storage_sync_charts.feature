Feature: Onepanel features regarding storage sync (e.g. import/update)

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service

    And directory tree structure on local file system:
          browser2:
            dir1: 500
            dir2: 300


  Scenario: User configures storage sync and sees storage synchronization statistics
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is no "dir1", "dir2" in provider's storage mount point
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of browser1 with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
          imported storage: true

    When user of browser2 creates "space1" space in Onezone

    And user of browser2 sends support token for "space1" to user of browser1
    And user of browser1 opens "oneprovider-1" clusters submenu
    And user of browser1 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: new_storage (import-enabled)
          size: 1
          unit: GiB
          storage import:
            max depth: 3
            detect modifications: true
            detect deletions: true
            scan interval [s]: 1

    # wait more than 1 second for the mounting point's timestamp to change
    And user of browser2 is idle for 3 seconds

    And user of browser2 copies dir1 to provider's storage mount point

    # open chart tab
    And user of browser1 opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser1 clicks on storage import navigation tab in space "space1"

    # check charts after storage import of 500 files and 1 directory to 1 space
    Then user of browser1 clicks on last hour update view
    And user of browser1 sees that number of inserted files for "space1" shown on Synchronization files processing charts equals 501 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space1" shown on Synchronization files processing charts equals 1 in Spaces page in Onepanel

    And user of browser2 copies dir2 to provider's storage mount point

    # check charts after storage update - inserted 300 files and 1 directory to 1 space
    And user of browser1 sees that number of inserted files for "space1" shown on Synchronization files processing charts equals 802 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space1" shown on Synchronization files processing charts equals 2 in Spaces page in Onepanel

    And user of browser2 removes dir1 from provider's storage mount point

   # check charts after storage cleanup of 500 files and 1 directories
    And user of browser1 sees that number of deleted files for "space1" shown on Synchronization files processing charts equals 501 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space1" shown on Synchronization files processing charts equals 3 in Spaces page in Onepanel

    And user of browser2 removes dir2 from provider's storage mount point

    # check charts after storage cleanup of 800 files and 2 directories
    And user of browser1 sees that number of deleted files for "space1" shown on Synchronization files processing charts equals 802 in Spaces page in Onepanel
    And user of browser1 sees that number of updated files for "space1" shown on Synchronization files processing charts equals 4 in Spaces page in Onepanel

    And user of browser1 revokes "space1" space support in "oneprovider-1" provider in Onepanel
