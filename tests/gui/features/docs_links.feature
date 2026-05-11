Feature: Onezone links to documentation

  Background:
    Given admin user does not have access to any space
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as admin to Onezone service

  Scenario: User can see that all links to REST API docs in space API modal works correctly
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    Then user of browser sees that all links to REST API documentation works correctly for each selected operation in space menu API section

  Scenario: User can see that all links to REST API docs in file details API section works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser clicks on "API" navigation tab in "Directory Details" modal
    Then user of browser sees that all links to REST API documentation works correctly for each selected operation in file details API section

  Scenario: User can see that link to Metadata documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser clicks on clicks on question mark beside the metadata type selector
    And user of browser clicks on "metadata documentation" link in info popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees "User Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees "Metadata" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Permissions documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser clicks on clicks on question mark beside the edit permissions type selector
    And user of browser clicks on "file permissions documentation" link in info popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees "User Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees "Data" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Quality of Service documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Quality of Service" option in data row menu in file browser
    And user of browser clicks on clicks on question mark beside the Quality of Service requirements label
    And user of browser clicks on "QoS documentation" link in info popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Oneprovider", "Configuration"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "Rule-based replication (QoS)" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Tokens documentation in tokens page works correctly
    When user of browser clicks on Tokens in the main menu
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser clicks on "documentation" link in "Create new token" view
    And user of browser is redirected to newly opened tab
    Then user of browser sees "User Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees "Tokens" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Tokens documentation in create custom token section in tokens page works correctly
    When user of browser clicks on Tokens in the main menu
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser clicks on "Create custom token" option in "Create new token" view
    And user of browser clicks on "Show details" link in "Create new token" view
    And user of browser clicks on "tokens documentation" link in "Create new token" view
    And user of browser is redirected to newly opened tab
    Then user of browser sees "User Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees "Tokens" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Tokens documentation in create custom token section with read only caveat works correctly
    When user of browser clicks on Tokens in the main menu
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser clicks on "Create custom token" option in "Create new token" view
    And user of browser clicks on "Show inactive caveats" label in "Create new token" view
    And user of browser sets read only token caveat
    And user of browser clicks on "Show details" link in "Create new token" view
    And user of browser clicks on "data access caveats documentation" link in "Create new token" view
    And user of browser is redirected to newly opened tab
    Then user of browser sees "User Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees "Tokens" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to DNS Config documentation in Oneprovider DNS Config in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on DNS setup item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser clicks on "DNS setup documentation" link in DNS SETUP view in Onepanel
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Onezone", "Configuration"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "DNS config" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to DNS Config documentation in Onezone DNS Config in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "onezone" in clusters menu
    And user of browser clicks on DNS setup item in submenu of "onezone" item in CLUSTERS sidebar in Onepanel
    And user of browser clicks on "DNS setup documentation" link in DNS SETUP view in Onepanel
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Onezone", "Configuration"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "DNS config" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to DNS Config documentation in Onezone DNS Config at subdomain delegation section in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "onezone" in clusters menu
    And user of browser clicks on DNS setup item in submenu of "onezone" item in CLUSTERS sidebar in Onepanel
    And user of browser clicks on "DNS setup documentation" link at subdomain delegation section in DNS SETUP view in Onepanel
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Onezone", "Configuration"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "DNS config" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to file popularity documentation in File popularity tab in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser opens "space1" record on spaces list in Spaces page in Onepanel
    And user of browser clicks on File popularity navigation tab in space "space2"
    And user of browser enables file-popularity in "space1" space in Onepanel
    And user of browser opens advanced settings in file popularity tab in Onepanel
    And user of browser clicks on "file popularity documentation" link in file popularity tab in Onepanel
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Oneprovider", "Configuration"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "File popularity" name in title, header and active sidebar link in "Docs" subpage in documentation

  Scenario: User can see that link to Onedatify documentation in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on add new provider cluster button in clusters menu
    And user of browser clicks on "Onedatify documentation" link in clusters page
    And user of browser is redirected to newly opened tab
    Then user of browser sees "Admin Guide" active chapter in "Docs" subpage in documentation
    And user of browser sees that ["Oneprovider", "Installation"] sidebar folders are expanded in "Docs" subpage in documentation
    And user of browser sees "Onedatify CLI wizard" name in title, header and active sidebar link in "Docs" subpage in documentation