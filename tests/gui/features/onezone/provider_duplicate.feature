Feature: Basic management of duplicate providers in Onezone GUI

  Background:
    Given user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service

  Scenario: User deletes dead duplicate provider
    When user of browser sees only one "oneprovider-1" record in clusters menu
    And user of browser remembers "oneprovider-1" cluster id

    # oneprovider-1 menu has to be closed for proper checking on clusters list
    And user of browser clicks on Data in the main menu
    And user of browser kills "oneprovider-1" provider
    And user of browser refreshes site
    And user of browser sees that "oneprovider-1" cluster is not working in clusters menu

    # Kubernetes provides provider's restart and registration
    Then user of browser waits for another "oneprovider-1" record to appear in clusters menu
    And user of browser sees that new "oneprovider-1" cluster is working
    And user of browser clicks on "oneprovider-1" with old cluster id in clusters menu

    # deregister old cluster
    And user of browser sees that "No connection to Onepanel" error modal appeared
    And user of browser closes "Error" modal
    And user of browser clicks deregistration link in clusters page
    And user of browser checks the understand notice in clusters page
    And user of browser clicks on confirm deregistration button in clusters page

    And user of browser is idle for 2 seconds
    And user of browser clicks on Data in the main menu
    And user of browser sees only one "oneprovider-1" record in clusters menu
    And user of browser sees that "oneprovider-1" cluster is working in clusters menu
