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


  Scenario: User can see that link to REST API docs in space menu works correctly
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser clicks on "documentation link" link in modal "REST API"
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/api/[\d+\.]*[\d+]/onezone\?anchor=operation/get_space
    And user of browser should see that the page title contains "Onedata | API"
    And user of browser sees that active sidebar label is "GET Get Space Details" in REST API documentation


  Scenario: User can see that link to REST API docs in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser clicks on "API" navigation tab in "Directory Details" modal
    And user of browser clicks on "documentation link" link in modal "Directory Details"
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/api/[\d+\.]*[\d+]/oneprovider\?anchor=operation/download_file_content
    And user of browser should see that the page title contains "Onedata | API"
    And user of browser sees that active sidebar label is "GET Download File Content" in REST API documentation


  Scenario: User can see that link to Metadata documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser clicks on "Question icon" button in metadata panel
    And user of browser clicks on "documentation link" link in "info" popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/documentation/[\d+\.]*[\d+]/user-guide/metadata.html
    And user of browser should see that the page title contains "Onedata | Documentation"
    And user of browser sees that active sidebar link is "Metadata" in documentation page


  Scenario: User can see that link to Permissions documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser clicks on "Question icon" button in edit permissions panel
    And user of browser clicks on "documentation link" link in "info" popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/documentation/[\d+\.]*[\d+]/user-guide/data\[data-access-control\].html
    And user of browser should see that the page title contains "Onedata | Documentation"
    And user of browser sees that active sidebar link is "Data" in documentation page


  Scenario: User can see that link to Quality of Service documentation in file details works correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Quality of Service" option in data row menu in file browser
    And user of browser clicks on "Question icon" button in qos panel
    And user of browser clicks on "documentation link" link in "info" popup
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/documentation/[\d+\.]*[\d+]/admin-guide/oneprovider/configuration/qos.html
    And user of browser should see that the page title contains "Onedata | Documentation"
    And user of browser sees that active sidebar link is "Quality of Service" in documentation page


  Scenario: User can see that link to Tokens documentation in tokens page works correctly
    When user of browser clicks on Tokens in the main menu
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser clicks on "Create custom token" option in "Create new token" view
    And user of browser clicks on "Show details" link in "Create new token" view
    And user of browser clicks on "documentation link" link in "Create new token" view
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/documentation/[\d+\.]*[\d+]/user-guide/tokens.html
    And user of browser should see that the page title contains "Onedata | Documentation"
    And user of browser sees that active sidebar link is "Tokens" in documentation page


  Scenario: User can see that link to DNS Config documentation in DNS Config in Clusters page works correctly
    When user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on DNS setup item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser clicks on "documentation" link in "dns setup" submenu in Onepanel
    And user of browser is redirected to newly opened tab
    Then user of browser sees that URL matches: https://onedata.org/#/home/documentation/[\d+\.]*[\d+]/admin-guide/onezone/configuration/dns-config.html
    And user of browser should see that the page title contains "Onedata | Documentation"
    And user of browser sees that active sidebar link is "Dns Config" in documentation page