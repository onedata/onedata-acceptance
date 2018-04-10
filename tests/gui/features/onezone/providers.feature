Feature: Basic management of providers in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User opens provider popup by clicking on supporting provider in space's submenu
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space1" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser clicks on provider "oneprovider-1" in submenu of space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    Then user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map


  Scenario: User can go to Oneprovider by clicking on Go to your files in provider's popup
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space1" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser clicks on provider "oneprovider-1" in submenu of space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    And user of browser clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map
    And user of browser sees that Oneprovider session has started
    Then user of browser sees that URL matches: https?://[^/]*/#/onedata/data/.*


  Scenario: User sees that after clicking on provider's circle on world map, provider's popup appears
    When user of browser sees that there is no displayed provider popup next to 1st provider circle on Onezone world map
    And user of browser clicks on 1st provider circle on Onezone world map
    Then user of browser sees that provider popup has appeared next to 1st provider circle on Onezone world map


  # TODO clicking on other provider do when there will be other providers
  Scenario: User sees that provider popup can be closed with clicking the same or other provider circle
    When user of browser sees that there is no displayed provider popup next to 1st provider circle on Onezone world map
    And user of browser clicks on 1st provider circle on Onezone world map
    And user of browser sees that provider popup has appeared next to 1st provider circle on Onezone world map
    And user of browser clicks on 1st provider circle on Onezone world map
    Then user of browser sees that provider popup next to 1st provider circle on Onezone world map has disappeared


  # TODO now it is not possible to close by clicking outside map, try it when it will be possible
  Scenario: User sees that provider popup can be closed with clicking on map
    When user of browser sees that there is no displayed provider popup next to 1st provider circle on Onezone world map
    And user of browser clicks on 1st provider circle on Onezone world map
    And user of browser sees that provider popup has appeared next to 1st provider circle on Onezone world map
    And user of browser clicks on Onezone world map
    Then user of browser sees that provider popup next to 1st provider circle on Onezone world map has disappeared


  Scenario: User sees that spaces list in provider popup and provider record in "GO TO YOUR FILES" matches
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser expands submenu of provider "oneprovider-1" by clicking on cloud in provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser clicks on "oneprovider-1" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    Then user of browser sees that the list of spaces in provider popup and in expanded "GO TO YOUR FILES" Onezone panel are the same for provider named "oneprovider-1"


  Scenario: User sees that if space is displayed in provider submenu in GO TO YOUR FILES panel, that provider is also displayed in submenu of that space in DATA SPACE MANAGEMENT panel
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser sees that there is provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser expands submenu of provider "oneprovider-1" by clicking on cloud in provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that there is space named "space1" in submenu of provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space1" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    Then user of browser sees that there is provider "oneprovider-1" in submenu of space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel


  Scenario: User sees that home space of provider should have "cloud with home" icon
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser sees that there is provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser expands submenu of provider "oneprovider-1" by clicking on cloud in provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that spaces counter for "oneprovider-1" match number of displayed supported spaces in expanded submenu of given provider in expanded "GO TO YOUR FILES" Onezone panel
    Then user of browser sees that space named "space1" in submenu of provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel is set as home


  Scenario: User can set Provider as Home provider (icon changes), and when he relogins, he will be redirected to Home provider automatically
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser sees that there is provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sets provider "oneprovider-1" as home by clicking on home outline in that provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that provider "oneprovider-1" is set as home provider in expanded "GO TO YOUR FILES" Onezone panel

    # logout
    And user of browser expands account settings dropdown in "ACCOUNT MANAGE" Onezone top bar
    And user of browser clicks on LOGOUT item in expanded settings dropdown in "ACCOUNT MANAGE" Onezone top bar
    And user of browser should see that the page title contains "Onezone - Login"

    # login again
    And user of browser logs as user1 to Onezone service
    Then user of browser sees that Oneprovider session has started


  Scenario: User sees that after unsupporting space, number displayed in space counter for given provider decreases
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    And user of browser sees that there is provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that spaces counter for provider "oneprovider-1" displays 1 in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser expands submenu of provider "oneprovider-1" by clicking on cloud in provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that spaces counter for "oneprovider-1" match number of displayed supported spaces in expanded submenu of given provider in expanded "GO TO YOUR FILES" Onezone panel

    # unsupport space
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space1" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser clicks on unsupport space for provider "oneprovider-1" in submenu of space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that "Unsupport space" modal has appeared
    And user of browser selects "I understand the risk of data loss" option in displayed modal
    And user of browser sees that "Yes" item displayed in modal is enabled
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared

    # confirm results
    Then user of browser sees that spaces counter for provider "oneprovider-1" displays 0 in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser expands submenu of provider "oneprovider-1" by clicking on cloud in provider record in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser sees that spaces counter for "oneprovider-1" match number of displayed supported spaces in expanded submenu of given provider in expanded "GO TO YOUR FILES" Onezone panel


  Scenario: User sees that when no provider is working appropriate msg is shown
    Given there are no working provider(s) named "oneprovider-1"
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    Then user of browser sees that provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel is not working
    And user of browser sees alert with title "All your providers are offline" on world map in Onezone gui
