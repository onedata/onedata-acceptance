Feature: Deployment process using panel of zone and provider

  Scenario: Cluster deployment with 2 hosts
    Given users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of [browser1, browser2] created admin accounts "admin:password"

    # step1 in zone and provider panels
    When user of browser1 clicks on Create Onezone cluster button in welcome page in Onepanel
    And user of browser1 enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*onezone.* host in step 1 of deployment process in Onepanel
    And user of browser1 types name of "onezone" zone to Zone name field in step 1 of deployment process in Onepanel
    And user of browser1 types hostname of "onezone" zone to Zone domain name field in step 1 of deployment process in Onepanel
    And user of browser1 clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser1 sees that cluster deployment has started

    And user of browser2 clicks on Create Oneprovider cluster button in welcome page in Onepanel
    And user of browser2 clicks on Add new host button in step 1 of deployment process in Onepanel
    And user of browser2 types second host to hostname field in step 1 of deployment process in Onepanel
    And user of browser2 clicks on Add host button in step 1 of deployment process in Onepanel
    And user of browser2 enables [Database, Cluster Worker] options for .*1.*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser2 enables [Cluster Manager, Primary Cluster Manager] options for .*0.*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser2 clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser2 sees that cluster deployment has started

    # wait for finish of deployment
    And user of browser1 waits 180 seconds for cluster deployment to finish
    And user of browser2 waits 180 seconds for cluster deployment to finish

    # setup IP step in zone panels
    And user of browser1 clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in zone panel
    And user of browser1 clicks on "Perform check" button in deployment setup DNS step
    And user of browser1 clicks on Proceed button in deployment setup DNS step
    And user of browser1 clicks on Yes button in warning modal in deployment setup DNS step

    # web cert in zone panel
    And user of browser1 deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser1 clicks on Next step button in web cert step of deployment process in Onepanel

    # send registration token
    And user of browser1 clicks on Manage cluster via onezone button in last step of deployment process in Onepanel
    And user of browser1 logs as admin to Onezone service
    And user of browser1 clicks on add new provider cluster button in clusters menu
    And user of browser1 copies registration token from clusters page
    And user of browser1 sends copied token to user of browser2

    # step2 in provider panel
    And user of browser2 types received registration token in step 2 of deployment process in Onepanel
    And user of browser2 clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser2 types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser2 deactivates Request a subdomain toggle
    And user of browser2 types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser2 types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser2 clicks on Register button in step 2 of deployment process in Onepanel
    And user of browser2 is idle for 10 seconds

    # setup IP step in provider panel
    And user of browser2 sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser2 clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in provider panels
    And user of browser2 clicks on "Perform check" button in deployment setup DNS step
    And user of browser2 clicks on Proceed button in deployment setup DNS step

    # web cert in provider panel
    And user of browser2 deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser2 clicks on Next step button in web cert step of deployment process in Onepanel

    # step5 in provider panel
    And user of browser2 selects Null Device from storage selector in step 5 of deployment process in Onepanel
    And user of browser2 types "storage" to Storage name field in POSIX form in step 5 of deployment process in Onepanel

    And user of browser2 clicks on Add button in add storage form in step 5 of deployment process in Onepanel
    And user of browser2 sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser2 expands "storage" record on storages list in step 5 of deployment process in Onepanel
    And user of browser2 sees that "storage" Storage type is null device in step 5 of deployment process in Onepanel

    And user of browser2 clicks on Finish button in step 5 of deployment process in Onepanel

    # check config in zone and provider panels
    Then user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "onezone" in clusters menu
    And user of browser1 clicks Nodes of "onezone" in the sidebar
    And user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*onezone.* host in Nodes page in Onepanel
    And user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*onezone.* host in Nodes page in Onepanel

    And user of browser2 clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel
    And user of browser2 clicks on Nodes item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 sees that [Database, Cluster Worker] options are enabled for .*1.*oneprovider.* host in Nodes page in Onepanel
    And user of browser2 sees that [Cluster Manager, Primary Cluster Manager] options are enabled for .*0.*oneprovider.* host in Nodes page in Onepanel
    And user of browser2 sees that [Database, Cluster Worker] options cannot be changed for .*1.*oneprovider.* host in Nodes page in Onepanel
    And user of browser2 sees that [Cluster Manager, Primary Cluster Manager] options cannot be changed for .*0.*oneprovider.* host in Nodes page in Onepanel
