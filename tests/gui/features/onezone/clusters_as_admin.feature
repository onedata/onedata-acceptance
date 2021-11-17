Feature: Management of clusters entries as an admin user in Onezone GUI

  Background:
    Given user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service

  Scenario: User deregisters dead duplicated provider
    When user of browser sees only one "oneprovider-1" record in clusters menu
    And user of browser remembers "oneprovider-1" cluster id

    # oneprovider-1 menu has to be closed for proper checking on clusters list
    And user of browser clicks on Data in the main menu
    And user of browser kills "oneprovider-1" provider
    And user of browser clicks on Clusters in the main menu
    And user of browser sees that "oneprovider-1" cluster is not working in clusters menu

    # Kubernetes provides provider's restart and registration
    Then user of browser waits for another "oneprovider-1" record to appear in clusters menu
    And user of browser sees that new "oneprovider-1" cluster is working

    # assert new provider working
    And user of browser clicks on "oneprovider-1" with new cluster id in clusters menu
    And user of browser sees Overview page of "oneprovider-1" cluster
    And user of browser sees that old "oneprovider-1" is not working in clusters sidebar

    # oneprovider-1 menu has to be closed for proper checking on clusters list
    And user of browser clicks on Data in the main menu

    # deregister old cluster
    And user of browser clicks on "oneprovider-1" with old cluster id in clusters menu
    And user of browser sees that "No connection to Onepanel" error modal appeared
    And user of browser closes "Error" modal
    And user of browser clicks deregistration link in clusters page
    And user of browser checks the understand notice in clusters page
    And user of browser clicks on confirm deregistration button in clusters page

    And user of browser is idle for 2 seconds

    # oneprovider-1 menu has to be closed for proper checking on clusters list
    And user of browser clicks on Data in the main menu
    And user of browser sees only one "oneprovider-1" record in clusters menu
    And user of browser sees that "oneprovider-1" cluster is working in clusters menu
