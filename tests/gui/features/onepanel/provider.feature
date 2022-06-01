Feature: Provider management in Onepanel GUI


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


    And opened [browser_emergency, space_owner_browser] with [admin, space-owner-user] signed in to [emergency interface of Onepanel, onezone] service


  Scenario: User changes provider name and domain
    Given provider name set to name of "oneprovider-1" by user of browser_emergency in Onepanel

    When user of browser_emergency clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency sees that Provider name attribute is equal to the name of "oneprovider-1" provider in Provider panel
    And user of browser_emergency sees that Domain attribute is equal to the hostname of "oneprovider-1" provider in Provider panel

    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser sees current provider named "oneprovider-1" on file browser page

    # modify provider details
    And user of browser_emergency clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency clicks on Modify provider details button in provider page in Onepanel
    And user of browser_emergency types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser_emergency types test hostname of "oneprovider-1" to Domain input box in modify provider details form in Provider panel
    And user of browser_emergency clicks on Modify provider details button in provider details form in Provider panel
    And user of browser_emergency sees an info notify with text matching to: .*[Pp]rovider.*data.*modified.*
    And user of browser_emergency clicks on Discard button in the configure web cert modal
    And user of browser_emergency sees that Provider name attribute is equal to "pro1" in Provider panel
    And user of browser_emergency sees that Domain attribute is equal to test hostname of "oneprovider-1" in Provider panel

    # check if provider details were modified also in oz and op
    Then user of space_owner_browser sees that current provider is "pro1" on file browser page

    And user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Providers" of "space1" space in the sidebar
    And user of space_owner_browser sees "pro1" is on the providers list
    And user of space_owner_browser sees that hostname in displayed provider popup matches test hostname of provider "oneprovider-1"

    # restore provider details
    And user of browser_emergency clicks on Modify provider details button in provider page in Onepanel
    And user of browser_emergency types name of "oneprovider-1" provider to Provider name input box in modify provider details form in Provider panel
    And user of browser_emergency types hostname of "oneprovider-1" provider to Domain input box in modify provider details form in Provider panel
    And user of browser_emergency clicks on Modify provider details button in provider details form in Provider panel
    And user of browser_emergency sees an info notify with text matching to: .*[Pp]rovider.*data.*modified.*
    And user of browser_emergency is idle for 2 seconds


  Scenario: User deregisters provider, registers it again and sees that provider is working
    Given provider name set to name of "oneprovider-1" by user of browser_emergency in Onepanel

    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Providers" of "space1" space in the sidebar
    And user of space_owner_browser sees "oneprovider-1" is on the providers list
    And user of browser_emergency deregisters provider in "oneprovider-1" Oneprovider panel service
    And user of space_owner_browser is idle for 8 seconds

    # send registration token
    And user of space_owner_browser clicks on add new provider cluster button in clusters menu
    And user of space_owner_browser copies registration token from clusters page
    And user of space_owner_browser sends copied token to user of browser_emergency

    # step2 in provider panel
    And user of browser_emergency types received registration token in step 2 of deployment process in Onepanel
    And user of browser_emergency clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser_emergency types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser_emergency deactivates Request a subdomain toggle
    And user of browser_emergency types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser_emergency types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser_emergency clicks on Register button in step 2 of deployment process in Onepanel

    And user of space_owner_browser is idle for 5 seconds
    And user of browser_emergency selects POSIX from storage selector in step 5 of deployment process in Onepanel
    And user of browser_emergency types "posix" to Storage name field in POSIX form in step 5 of deployment process in Onepanel

    And user of browser_emergency types "/volumes/persistence/storage" to Mount point field in POSIX form in step 5 of deployment process in Onepanel
    And user of browser_emergency clicks on Add button in add storage form in step 5 of deployment process in Onepanel
    And user of browser_emergency sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser_emergency clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser_emergency clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel

    # NOTE: meta-steps have been changed to "normal" steps (located in tests/gui/steps/onezone/space.py).
    Then user of space_owner_browser opens Onezone page
    And user of space_owner_browser sees that there is no supporting provider "oneprovider-1" for space named "space1"
    And user of space_owner_browser creates space "helloworld"
    And user of space_owner_browser generates space support token for space "helloworld" and sends it to user of browser_emergency
    And user of browser_emergency supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
            storage: posix
            size: 10000000

    # check that provider is working
    And user of space_owner_browser sees that provider "oneprovider-1" in Onezone is working

    And user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "helloworld" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Files" of "helloworld" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser sees current provider named "oneprovider-1" on file browser page

