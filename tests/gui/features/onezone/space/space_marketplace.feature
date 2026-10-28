Feature: Basic management of Space Marketplace

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - marketplace-user
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
    When user of browser clicks on "Data" in the main menu
    And user of browser clicks on "Marketplace" button in spaces sidebar
    And user of browser clicks on "Advertise your space" button in Space Marketplace subpage
    And user of browser chooses "space1" in spaces dropdown menu in modal "Advertise space"
    And user of browser clicks on "Configure..." button in modal "Advertise space"
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
        description: "# Example space\nExample of a space advertised in a Marketplace"

    # TODO: VFS-13985 Either uncomment it or add a new meta step to check if space configuration is correct before advertising
    # And user of browser sees tags "[archival, big-data, science]" in space configuration subpage
    And user of browser checks "Advertise in Marketplace" toggle on space configuration page
    And user of browser writes "example@gmail.com" into contact email text field in modal "Advertise space in the Marketplace"
    And user of browser accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
    And user of browser clicks on "Proceed" button in modal "Advertise space in the Marketplace"
    And user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page
    And user of browser sees "example@gmail.com" in marketplace contact e-mail address text field
    And user of browser sees that "space1" space is advertised in the marketplace in space sidebar
    And user of browser clicks "Overview" of "space1" space in the sidebar
    Then user of browser sees that the space is advertised in the Marketplace tile in space overview subpage
    And user of browser clicks "Show" link in the Marketplace tile in space overview subpage
    Then user of browser can see there are 1 spaces marketplace on the spaces marketplace list in the sidebar
    And user of browser sees "space1" space in Space Marketplace subpage with following details:
        access state: membership granted
        tags:
          - archival
          - big-data
          - science
        organization name: "onedata"
        creation time: current
        providers:
          - dev-oneprovider-krakow
    And user of browser sees "space1" advertised space description with "Example space" header and "Example of a space advertised in a Marketplace" paragraph


  Scenario: User does not see owned space in the Marketplace after he withdraws it
    Given using REST, user space-owner-user configures "space1" space in "onezone" Onezone service as follows:
        organizationName: "onedata"
        description: "Example of a space advertised in a Marketplace"
        advertisedInMarketplace: true
        marketplaceContactEmail: "example@gmail.com"

    When user of browser clicks on "Data" in the main menu
    And user of browser clicks on "Marketplace" button in spaces sidebar
    Then user of browser sees "space1" space in Space Marketplace subpage with following details:
        access state: membership granted
        organization name: "onedata"
        creation time: current
        providers:
          - dev-oneprovider-krakow
        description: "Example of a space advertised in a Marketplace"
    And user of browser sees "Visit space" link for "space1" space in Space Marketplace subpage
    And user of browser sees "Configure" link for "space1" space in Space Marketplace subpage

    When user of browser clicks "Configure" link for "space1" space in Space Marketplace subpage
    Then user of browser sees that opened space name is "space1"
    And user of browser sees "space configuration" label of current page
    And user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page
    When user of browser unchecks "Advertise in Marketplace" toggle on space configuration page
    And user of browser clicks on "Proceed" button in modal "Warning"
    Then user of browser sees that "Advertise in Marketplace" toggle is not checked on space configuration page
    When user of browser clicks on "Marketplace" button in spaces sidebar
    Then user of browser does not see "space1" space in Space Marketplace subpage


  Scenario: Users see live changes to an advertised space in the Marketplace
    Given using REST, user space-owner-user configures "space1" space in "onezone" Onezone service as follows:
        organizationName: "Onedata"
        description: "Original marketplace description"
        advertisedInMarketplace: true
        marketplaceContactEmail: "example@gmail.com"
    And opened [space_owner_browser, marketplace_browser] with [space-owner-user, marketplace-user] signed in to [Onezone, Onezone] service

    When user of space_owner_browser clicks on "Data" in the main menu
    And user of space_owner_browser clicks "Configuration" of "space1" space in the sidebar
    And user of marketplace_browser clicks on "Data" in the main menu
    And user of marketplace_browser clicks on "Marketplace" button in spaces sidebar
    Then user of marketplace_browser sees "space1" space with a "Request access" button in Space Marketplace subpage

    When user of space_owner_browser sets space configuration as follows:
        space name: "space1-updated"
        organization name: "Onedata Research"
        tags:
          general:
            - archival
            - big-data
        description: "Updated marketplace description"

    Then user of marketplace_browser sees "space1-updated" space in Space Marketplace subpage with following details:
        access state: request access
        tags:
          - archival
          - big-data
        organization name: "Onedata Research"
        description: "Updated marketplace description"


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
    And user of browser sees Space Details tile in space overview subpage with following information:
        # space name is not displayed here, but it is required in configuration view
        organization name: "onedata"
        tags:
          - dynamic
        description: "Example of a space advertised in a Marketplace"
