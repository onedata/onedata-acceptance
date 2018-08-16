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

    And opened [browser1, browser2] with [admin, user1] logged to [oneprovider-1 provider panel, onezone] service

  Scenario: User changes provider name and domain
    When user of browser1 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 sees that Provider name attribute is equal to the name of "oneprovider-1" provider in Provider panel
    And user of browser1 sees that Domain attribute is equal to the hostname of "oneprovider-1" provider in Provider panel

    And user of browser2 sees "space1" has appeared on spaces
    And user of browser2 clicks "space1" on spaces on left sidebar menu
    And user of browser2 clicks Providers of "space1" on left sidebar menu
    And user of browser2 opened oneprovider-1 Oneprovider view in web GUI
    And user of browser2 sees that provider name displayed in Oneprovider page is equal to the name of "oneprovider-1" provider

    # modify provider details
    And user of browser1 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Modify provider details button in provider page in Onepanel
    And user of browser1 types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser1 types test hostname of "oneprovider-1" to Domain input box in modify provider details form in Provider panel
    And user of browser1 clicks on Modify provider details button in provider details form in Provider panel
    And user of browser1 sees an info notify with text matching to: .*[Pp]rovider.*data.*modified.*
    And user of browser1 should be redirected to /login page
    And user of browser1 logs as admin to Onepanel service
    And user of browser1 sees that Provider name attribute is equal to "pro1" in Provider panel
    And user of browser1 sees that Domain attribute is equal to test hostname of "oneprovider-1" in Provider panel

    # check if provider details were modified also in oz and op
    And user of browser2 is idle for 10 seconds
    And user of browser2 refreshes site
    And user of browser2 is idle for 2 seconds
    Then user of browser2 sees that provider name displayed in Oneprovider page is equal to "pro1"

    And user of browser2 opens onezone page
    And user of browser2 sees "space1" has appeared on spaces
    And user of browser2 clicks "space1" on spaces on left sidebar menu
    And user of browser2 clicks Providers of "space1" on left sidebar menu
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
    When user of browser2 clicks "space1" on spaces on left sidebar menu
    And user of browser2 clicks Providers of "space1" on left sidebar menu
    And user of browser2 sees that list of supporting providers for space named "space1" contains only: "oneprovider-1"
    And using web gui, admin deregisters provider in "oneprovider-1" Oneprovider panel service
    And user of browser2 is idle for 8 seconds

    And using web gui, admin registers provider in "onezone" Onezone service with following configuration:
          provider name:
              of provider: oneprovider-1
          domain:
              of provider: oneprovider-1
          zone domain:
              of zone: onezone
          storages:
              posix:
                type: posix
                mount point: /volumes/storage
          admin email: admin@onedata.org                

    Then user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*oneprovider.* host in Nodes page in Onepanel
    And user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*oneprovider.* host in Nodes page in Onepanel
    # NOTE: meta-steps have been changed to "normal" steps(located in tests/gui/steps/onezone/space.py).
    And user of browser2 opens onezone page
    And user of browser2 sees that there is no supporting provider "oneprovider-1" for space named "space1"
    And user of browser2 creates space "helloworld"
    And user of browser2 generates space support token for space "helloworld" and sends it to user of browser1
    And using web gui, admin supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
            storage: posix
            size: 10000000

    # check that provider is working
    And user of browser2 refreshes site
    And user of browser2 sees that provider "oneprovider-1" in Onezone panel is working
    And user of browser2 opened oneprovider-1 Oneprovider view in web GUI
    And user of browser2 sees that Oneprovider session has started

