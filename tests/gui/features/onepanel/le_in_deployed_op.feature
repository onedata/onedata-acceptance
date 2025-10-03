Feature: Enabling Let`s Encrypt and subdomain delegation in deployed zone and provider cluster


  Scenario: Enabling Lets Encrypt and subdomain delegation in existing cluster
    Given users opened [browser1] browsers' windows
    And user of [browser1] opened [Onezone] page
    And user of [browser1] logged as [admin] to [Onezone] service

    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "onezone" in clusters menu
    And user of browser1 clicks on DNS setup item in submenu of "onezone" item in CLUSTERS sidebar in Onepanel
    And user of browser1 checks "Use built-in DNS server" toggle in DNS SETUP view in Onepanel
    And user of browser1 checks "Enable subdomain delegation" toggle in DNS SETUP view in Onepanel

    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Provider configuration item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Edit settings button in provider page in Onepanel

    And user of browser1 checks "Request a subdomain" toggle in modify provider details form in Provider panel
    And user of browser1 types name of "oneprovider-1" provider to Subdomain input box in modify provider details form in Provider panel
    And provider "oneprovider-1" with onezone domain host entry is added to /etc/hosts
    And user of browser1 saves changes in provider details form in Provider panel

    And user of browser1 clicks on Web certificate item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 checks "Use Lets Encrypt" toggle in Web certificate view in Onepanel

    # check web cert
    Then user of browser1 sees that "Use Lets Encrypt" toggle is checked in Web certificate view in Onepanel
    And user of browser1 sees that "Certificate path" is "/etc/op_panel/certs/web_cert.pem" in Web certificate view in Onepanel
    And user of browser1 sees that "Key path" is "/etc/op_panel/certs/web_key.pem" in Web certificate view in Onepanel
    And user of browser1 sees that "Certificate chain path" is "/etc/op_panel/certs/web_chain.pem" in Web certificate view in Onepanel
