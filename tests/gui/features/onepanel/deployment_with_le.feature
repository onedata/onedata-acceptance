Feature: Deployment with Let`s Encrypt and enabled subdomain delegation process using panel of zone and provider


  Scenario: Cluster deployment with Lets Encrypt and enabled subdomain delegation
    Given users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of browser2 created admin accounts "admin:password"

    # send registration token
    When user of browser1 clicks open in onezone in Onepanel login page
    And user of browser1 logs as admin to Onezone service
    And user of browser1 clicks on DNS setup item in submenu of "onezone" item in CLUSTERS sidebar in Onepanel
    And user of browser1 checks "Use built-in DNS server" toggle in DNS SETUP view in Onepanel
    And user of browser1 checks "Enable subdomain delegation" toggle in DNS SETUP view in Onepanel
    And user of browser1 clicks on add new provider cluster button in clusters menu
    And user of browser1 copies registration token from clusters page
    And user of browser1 sends copied token to user of browser2

    # step1 in provider panel
    And user of browser2 clicks on Create Oneprovider cluster button in welcome page in Onepanel
    And user of browser2 enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser2 clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser2 sees that cluster deployment has started

    # wait for finish of deployment
    And user of browser2 waits 180 seconds for cluster deployment to finish

    # step2 in provider panel
    And user of browser2 types received registration token in step 2 of deployment process in Onepanel
    And user of browser2 clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser2 types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser2 activates Request a subdomain toggle
    And user of browser2 types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser2 clicks on Register button in step 2 of deployment process in Onepanel
    And user of browser2 is idle for 10 seconds

    # setup IP step in provider panel
    And user of browser2 sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser2 clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in provider panel
    And user of browser2 clicks on "Perform check" button in deployment setup DNS step
    And user of browser2 clicks on Proceed button in deployment setup DNS step
    And provider "oneprovider-1" with onezone domain host entry is added to /etc/hosts

    # web cert in provider panel
    And user of browser2 activates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser2 clicks on Next step button in web cert step of deployment process in Onepanel
    # after enabling lets encrypt page will reload
    And user of browser2 waits till login page of emergency interface of Onepanel appears
    And user of browser2 logs as admin to emergency interface of Onepanel service

    # step5 in provider panel
    And user of browser2 selects POSIX from storage selector in step 5 of deployment process in Onepanel
    And user of browser2 types "posix" to Storage name field in POSIX form in step 5 of deployment process in Onepanel

    And user of browser2 types "/volumes/posix" to Mount point field in POSIX form in step 5 of deployment process in Onepanel
    And user of browser2 clicks on Add button in add storage form in step 5 of deployment process in Onepanel

    And user of browser2 expands "posix" record on storages list in step 5 of deployment process in Onepanel
    And user of browser2 sees that "posix" Storage type is posix in step 5 of deployment process in Onepanel
    And user of browser2 sees that "posix" Mount point is /volumes/posix in step 5 of deployment process in Onepanel

    And user of browser2 clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser2 clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel

    # check config in provider panel
    Then user of browser2 clicks on Nodes item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*oneprovider.* host in Nodes page in Onepanel
    And user of browser2 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*oneprovider.* host in Nodes page in Onepanel
    # check web cert
    And user of browser2 clicks on Web certificate item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 sees that "Use Lets Encrypt" toggle is checked in Web certificate view in Onepanel
    And user of browser1 sees that oneprovider-1 provider domain is included in "DNS names" in Web certificate view in Onepanel
    And user of browser2 sees that "Certificate path" ends with "/certs/web_cert.pem" in Web certificate view in Onepanel
    And user of browser2 sees that "Key path" ends with "/certs/web_key.pem" in Web certificate view in Onepanel
    And user of browser2 sees that "Certificate chain path" ends with "/certs/web_chain.pem" in Web certificate view in Onepanel
