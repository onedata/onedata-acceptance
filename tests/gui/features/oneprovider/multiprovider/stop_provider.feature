Feature: Operations when current provider stops

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees space's size stats per provider after clicking show statistics, then oneprovider-2 is stopped and user sees error message
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar

    And user of browser opens size statistics per provider view using breadcrumbs menu in "space1"
    Then user of browser sees that logical_size for oneprovider-1 is "5 B"
    And user of browser sees that logical_size for oneprovider-2 is "5 B"
    And user of browser sees that physical_size for oneprovider-1 is "5 B"
    And user of browser sees that physical_size for oneprovider-2 is "0 B"
    And user of browser sees that oneprovider-1 content is "1 file, 1 directory"
    And user of browser sees that oneprovider-2 content is "1 file, 1 directory"

    And user of browser assures that provider named "oneprovider-2" is stopped
    And user of browser sees that error message for oneprovider-2 is "Proxy error: no connection to peer Oneprovider."

    # And user of browser assures that ["oneprovider-1", "oneprovider-2"] providers are online

    # And user of browser navigates to "Providers" page and waits until "oneprovider-2" is online


  Scenario: User switches to oneprovider-2 after oneprovider-1 has been stopped
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser assures that provider named "oneprovider-1" is stopped

    Then user of browser sees "SELECTED ONEPROVIDER IS CURRENTLY OFFLINE" error on spaces page
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page

    # And user of browser assures that ["oneprovider-1", "oneprovider-2"] providers are online

    # And user of browser navigates to "Providers" page and waits until "oneprovider-1" is online


  Scenario: User replicates file to another provider, then stops the provider and sees the error message in the physical location field
    When user of browser opens file browser for "space1" space
    And user of browser goes to "/dir1" in file browser

    And user of browser replicates "file1" to provider "oneprovider-2"
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish

    And user of browser assures that provider named "oneprovider-2" is stopped

    And user of browser opens file browser for "space1" space
    And user of browser goes to "/dir1" in file browser
    And user of browser opens "File details" modal on "Info" tab for "file1" file using context menu
    And user of browser clicks on button "Show more physical locations" in details modal
    Then user of browser sees "Proxy error: no connection to peer Oneprovider." as error message in physical location section for "oneprovider-2" provider in details modal

    # And user of browser assures that ["oneprovider-1", "oneprovider-2"] providers are online
    # And user of browser navigates to "Providers" page and waits until "oneprovider-2" is online
