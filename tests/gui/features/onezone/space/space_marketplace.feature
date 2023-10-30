Feature: Basic management of Space Marketplace

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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees own space in the Marketplace after configuring it
    When user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees that Space is not advertised in marketplace in space overview page
    And user of browser clicks "Configure advertisement" link in marketplace in space overview page
    And user of browser sees that "Advertise in Marketplace" toggle is not checked on space configuration page
    And user of browser sets space configuration as follows:
        space name: "space1"
        organization name: "onedata"
        tags:
          general:
            - archival
            - big-data
          domains:
            - science
        description: "Example of a space advertised in a Marketplace"

    And user of browser checks "Advertise in Marketplace" toggle on space configuration page
    And user of browser writes "example@gmail.com" into contact email text field in modal "Advertise space in the Marketplace"
    And user of browser accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
    And user of browser clicks on "Proceed" button in modal "Advertise space in the Marketplace"
    And user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page
    And user of browser sees "example@gmail.com" in marketplace contact e-mail address text field
    And user of browser sees that "space1" space is advertised in the marketplace in space sidebar
    And user of browser clicks "Overview" of "space1" space in the sidebar
    Then user of browser sees that Space is advertised in marketplace in space overview page
    And user of browser clicks "Show" link in marketplace in space overview page
    And user of browser sees advertised space on Space Marketplace subpage with following parameters:
        space name: "space1"
        tags:
          - archival
          - big-data
          - science
        organization name: "onedata"
        creation time: current
        providers:
          - dev-oneprovider-krakow
        description: "Example of a space advertised in a Marketplace"


  Scenario: User is asked about unsaved changes in space configuration subpage and can save them
    When user of browser clicks "Configuration" of "space1" space in the sidebar
    And user of browser provides space configuration without saving as follows:
        space name: "space1"
        organization name: "onedata"
        tags:
          general:
            - dynamic
        description: "Example of a space advertised in a Marketplace"

    And user of browser clicks "space1" on the spaces list in the sidebar
    Then user of browser sees that "There are unsaved changes" modal has appeared
    And user of browser clicks on "Save" button in modal "There are unsaved changes"
    And user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees tile Space Details on Space Overview subpage with following information:
        # space name is not displayed here, but it is required in configuration view
        organization name: "onedata"
        tags:
          - dynamic
        description: "Example of a space advertised in a Marketplace"
