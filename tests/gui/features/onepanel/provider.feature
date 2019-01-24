Feature: Provider management in Onepanel GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And opened [browser1, browser2] with [admin, user1] logged to [emergency interface of Onepanel, onezone] service


  Scenario: User changes provider name and domain
    Given provider name set to name of "oneprovider-1" by user of browser1 in Onepanel

    When user of browser1 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 sees that Provider name attribute is equal to the name of "oneprovider-1" provider in Provider panel
    And user of browser1 sees that Domain attribute is equal to the hostname of "oneprovider-1" provider in Provider panel

    And user of browser2 opens oneprovider-1 Oneprovider view in web GUI
    And user of browser2 sees that provider name displayed in Oneprovider page is equal to the name of "oneprovider-1" provider

    # modify provider details
    And user of browser1 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Modify provider details button in provider page in Onepanel
    And user of browser1 types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser1 types test hostname of "oneprovider-1" to Domain input box in modify provider details form in Provider panel
    And user of browser1 clicks on Modify provider details button in provider details form in Provider panel
    And user of browser1 sees an info notify with text matching to: .*[Pp]rovider.*data.*modified.*
    And user of browser1 clicks on Discard button in the configure web cert modal
    And user of browser1 sees that Provider name attribute is equal to "pro1" in Provider panel
    And user of browser1 sees that Domain attribute is equal to test hostname of "oneprovider-1" in Provider panel

    # check if provider details were modified also in oz and op
    And user of browser2 is idle for 10 seconds
    And user of browser2 refreshes site
    And user of browser2 is idle for 2 seconds
    Then user of browser2 sees that provider name displayed in Oneprovider page is equal to "pro1"

    And user of browser2 opens Onezone page
    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "space1" in the sidebar
    And user of browser2 sees "pro1" is on the providers list
    And user of browser2 sees that hostname in displayed provider popup matches test hostname of provider "oneprovider-1"

    # restore provider details
    And user of browser1 clicks on Modify provider details button in provider page in Onepanel
    And user of browser1 types name of "oneprovider-1" provider to Provider name input box in modify provider details form in Provider panel
    And user of browser1 types hostname of "oneprovider-1" provider to Domain input box in modify provider details form in Provider panel
    And user of browser1 clicks on Modify provider details button in provider details form in Provider panel
    And user of browser1 sees an info notify with text matching to: .*[Pp]rovider.*data.*modified.*
    And user of browser1 is idle for 2 seconds


  Scenario: User deregisters provider, registers it again and sees that provider is working
    Given provider name set to name of "oneprovider-1" by user of browser1 in Onepanel

    And user of browser2 clicks on Data in the main menu
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "space1" in the sidebar
    And user of browser2 sees "oneprovider-1" is on the providers list
    And using web gui, admin deregisters provider in "oneprovider-1" Oneprovider panel service
    And user of browser2 is idle for 8 seconds

    # send registration token
    And user of browser2 clicks on add new provider cluster button in clusters menu
    And user of browser2 copies registration token from clusters page
    And user of browser2 sends copied token to user of browser1

    # step2 in provider panel
    And user of browser1 types received registration token in step 2 of deployment process in Onepanel
    And user of browser1 clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser1 types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser1 deactivates Request a subdomain toggle
    And user of browser1 types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser1 types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser1 clicks on Register button in step 2 of deployment process in Onepanel

    Then user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*oneprovider.* host in Nodes page in Onepanel
    And user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*oneprovider.* host in Nodes page in Onepanel
    # NOTE: meta-steps have been changed to "normal" steps (located in tests/gui/steps/onezone/space.py).
    Then user of browser2 opens Onezone page
    And user of browser2 sees that there is no supporting provider "oneprovider-1" for space named "space1"
    And user of browser2 creates space "helloworld"
    And user of browser2 generates space support token for space "helloworld" and sends it to user of browser1
    And using web gui, admin supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
            storage: posix
            size: 10000000

    # check that provider is working
    And user of browser2 sees that provider "oneprovider-1" in Onezone is working
    And user of browser2 opens oneprovider-1 Oneprovider view in web GUI
    And user of browser2 sees that Oneprovider session has started

