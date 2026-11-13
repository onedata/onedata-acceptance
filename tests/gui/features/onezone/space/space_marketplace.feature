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


  Scenario: User opens advertisement configuration from the Marketplace tile of an unadvertised space
    When user of browser clicks "Overview" of "space1" space in the sidebar
    And user of browser sees that the space is not advertised in the Marketplace tile in space overview subpage
    And user of browser clicks "Configure advertisement" link in the Marketplace tile in space overview subpage
    Then user of browser sees "space configuration" label of current page
    And user of browser sees that "Advertise in Marketplace" toggle is not checked on space configuration page


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
    And user of browser writes "example@onedata.test" into contact email text field in modal "Advertise space in the Marketplace"
    And user of browser accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
    And user of browser clicks on "Proceed" button in modal "Advertise space in the Marketplace"
    And user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page
    And user of browser sees "example@onedata.test" in marketplace contact e-mail address text field
    And user of browser sees that "space1" space is advertised in the marketplace in space sidebar
    And user of browser clicks "Overview" of "space1" space in the sidebar
    Then user of browser sees that the space is advertised in the Marketplace tile in space overview subpage
    And user of browser clicks "Show" link in the Marketplace tile in space overview subpage
    Then user of browser sees that there is 1 space in the Marketplace
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


  # TODO: VFS-13985 This scenario should pass after fixing synchronization problems on the space configuration page in the frontend
  # Scenario: User can advertise and withdraw a space multiple times
  #   When user of browser clicks on "Data" in the main menu
  #   And user of browser clicks "Configuration" of "space1" space in the sidebar
  #   And user of browser sets space configuration as follows:
  #       space name: "space1"
  #       organization name: "onedata"
  #       tags:
  #         general:
  #           - archival
  #           - big-data
  #         domains:
  #           - science
  #       description: "# Example space\nExample of a space advertised in a Marketplace"

  #   And user of browser checks "Advertise in Marketplace" toggle on space configuration page
  #   And user of browser writes "example@onedata.test" into contact email text field in modal "Advertise space in the Marketplace"
  #   And user of browser accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
  #   And user of browser clicks on "Proceed" button in modal "Advertise space in the Marketplace"
  #   Then user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page

  #   When user of browser unchecks "Advertise in Marketplace" toggle on space configuration page
  #   And user of browser clicks on "Proceed" button in modal "Warning"
  #   Then user of browser sees that "Advertise in Marketplace" toggle is not checked on space configuration page

  #   When user of browser checks "Advertise in Marketplace" toggle on space configuration page
  #   And user of browser writes "example@onedata.test" into contact email text field in modal "Advertise space in the Marketplace"
  #   And user of browser accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
  #   And user of browser clicks on "Proceed" button in modal "Advertise space in the Marketplace"
  #   Then user of browser sees that "Advertise in Marketplace" toggle is checked on space configuration page

  #   When user of browser unchecks "Advertise in Marketplace" toggle on space configuration page
  #   And user of browser clicks on "Proceed" button in modal "Warning"
  #   Then user of browser sees that "Advertise in Marketplace" toggle is not checked on space configuration page


  Scenario: User does not see owned space in the Marketplace after he withdraws it
    Given using REST, user space-owner-user configures "space1" space in "onezone" Onezone service as follows:
        organizationName: "onedata"
        description: "Example of a space advertised in a Marketplace"
        advertisedInMarketplace: true
        marketplaceContactEmail: "example@onedata.test"

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
        marketplaceContactEmail: "example@onedata.test"
    And opened marketplace_browser with marketplace-user signed in to Onezone service

    When user of browser clicks on "Data" in the main menu
    And user of browser clicks "Configuration" of "space1" space in the sidebar
    And user of marketplace_browser clicks on "Data" in the main menu
    And user of marketplace_browser clicks on "Marketplace" button in spaces sidebar
    And user of marketplace_browser sees "space1" space in Space Marketplace subpage with following details:
        access state: request access
        organization name: "Onedata"
        description: "Original marketplace description"

    And user of browser sets space configuration as follows:
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


  Scenario: User sees spaces in Marketplace that conform to filtering options
    Given using REST, space-owner-user creates and advertises 50 spaces with "Hello" prefix in "onezone" Onezone service as follows:
        organizationName: "Onedata"
        description: "Lorem ipsum"
        marketplaceContactEmail: "space-owner@example.com"
    And using REST, space-owner-user creates and advertises 50 spaces with "World" prefix in "onezone" Onezone service as follows:
        organizationName: "Onedata"
        description: "Lorem ipsum"
        marketplaceContactEmail: "space-owner@example.com"
    And using REST, user space-owner-user configures "World00" space in "onezone" Onezone service as follows:
        description: "Test"
        tags:
          - archival
          - demo
    And using REST, user space-owner-user configures "World01" space in "onezone" Onezone service as follows:
        organizationName: "AGH"
    And using REST, user space-owner-user configures "World02" space in "onezone" Onezone service as follows:
        organizationName: "UJ"
    And using REST, user space-owner-user configures "Hello01" space in "onezone" Onezone service as follows:
        tags:
          - archival
    And using REST, user space-owner-user configures "Hello02" space in "onezone" Onezone service as follows:
        tags:
          - demo
    When user of browser clicks on "Data" in the main menu
    And user of browser clicks on "Marketplace" button in spaces sidebar

    And user of browser sets Marketplace filters as follows:
        search: "1"
    Then user of browser sees 28 Marketplace spaces and all their names contain "1"

    And user of browser sets Marketplace filters as follows:
        search: "AGH"
    Then user of browser sees only Marketplace spaces named ["World01"]

    And user of browser sets Marketplace filters as follows:
        search: "Test"
    Then user of browser sees only Marketplace spaces named ["World00"]

    And user of browser sets Marketplace filters as follows:
        search: ""
        tags:
          general:
            - archival
            - demo
    Then user of browser sees only Marketplace spaces named ["Hello01", "Hello02", "World00"]

    And user of browser sets Marketplace filters as follows:
        search: "01"
    Then user of browser sees only Marketplace spaces named ["Hello01"]
