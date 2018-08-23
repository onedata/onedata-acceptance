Feature: Deployment process using panel of zone and provider


  Scenario: Cluster deployment
    Given users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of [browser1, browser2] created admin accounts "admin:password"

    # step1 in zone and provider panels
    When user of browser1 clicks on Create new cluster button in welcome page in Onepanel
    And user of browser1 enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*onezone.* host in step 1 of deployment process in Onepanel
    And user of browser1 types name of "onezone" zone to Zone name field in step 1 of deployment process in Onepanel
    And user of browser1 types hostname of "onezone" zone to Zone domain name field in step 1 of deployment process in Onepanel
    And user of browser1 clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser1 sees that cluster deployment has started

    And user of browser2 clicks on Create new cluster button in welcome page in Onepanel
    And user of browser2 enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser2 clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser2 sees that cluster deployment has started

    # wait for finish of deployment
    And user of browser1 waits 180 seconds for cluster deployment to finish
    And user of browser2 waits 180 seconds for cluster deployment to finish

    # step2 in provider panel
    And user of browser2 types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser2 deactivates Request a subdomain toggle
    And user of browser2 types hostname of "onezone" zone to Onezone domain field in step 2 of deployment process in Onepanel
    And user of browser2 types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser2 types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser2 clicks on Register button in step 2 of deployment process in Onepanel
    And user of browser2 sees an info notify with text matching to: .*registered.*successfully.*

    # setup IP step in provider and zone panels
    And user of browser1 clicks on "Setup IP addresses" button in deployment setup IP step
    And user of browser2 sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser2 clicks on "Setup IP addresses" button in deployment setup IP step

    # web cert in zone panel
    And user of browser1 deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser1 clicks on Next step button in web cert step of deployment process in Onepanel

    # check config in zone panel
    And user of browser1 clicks on Manage the cluster button in last step of deployment process in Onepanel
    Then user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*onezone.* host in Nodes page in Onepanel
    And user of browser1 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*onezone.* host in Nodes page in Onepanel

    # web cert in provider panel
    And user of browser2 deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser2 clicks on Next step button in web cert step of deployment process in Onepanel

    # step5 in provider panel
    And user of browser2 selects POSIX from storage selector in step 5 of deployment process in Onepanel
    And user of browser2 types "posix" to Storage name field in POSIX form in step 5 of deployment process in Onepanel

    And user of browser2 types "/volumes/storage" to Mount point field in POSIX form in step 5 of deployment process in Onepanel
    And user of browser2 clicks on Add button in add storage form in step 5 of deployment process in Onepanel
    And user of browser2 sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser2 expands "posix" record on storages list in step 5 of deployment process in Onepanel
    And user of browser2 sees that "posix" Storage type is posix in step 5 of deployment process in Onepanel
    And user of browser2 sees that "posix" Mount point is /volumes/storage in step 5 of deployment process in Onepanel

    And user of browser2 clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser2 sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of browser2 clicks on Manage the cluster button in last step of deployment process in Onepanel
    And user of browser2 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*oneprovider.* host in Nodes page in Onepanel
    And user of browser2 sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*oneprovider.* host in Nodes page in Onepanel
