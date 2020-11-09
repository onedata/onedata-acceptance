Feature: Local Ceph deployment process using panel of zone and provider


  Scenario: User deploys cluster with Local Ceph and checks its configuration
    Given users opened [browser_oz_panel, browser_op_panel] browsers' windows
    And users of [browser_oz_panel, browser_op_panel] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of [browser_oz_panel, browser_op_panel] created admin accounts "admin:password"

    # step1 in zone and provider panels
    When user of browser_oz_panel clicks on Create Onezone cluster button in welcome page in Onepanel
    And user of browser_oz_panel enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*onezone.* host in step 1 of deployment process in Onepanel
    And user of browser_oz_panel types name of "onezone" zone to Zone name field in step 1 of deployment process in Onepanel
    And user of browser_oz_panel types hostname of "onezone" zone to Zone domain name field in step 1 of deployment process in Onepanel
    And user of browser_oz_panel clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser_oz_panel sees that cluster deployment has started

    And user of browser_op_panel clicks on Create Oneprovider cluster button in welcome page in Onepanel
    And user of browser_op_panel enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager, Ceph] options for .*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser_op_panel clicks on Deploy button in step 1 of deployment process in Onepanel

    # Ceph configuration
    And user of browser_op_panel enables "Manager & Monitor" toggle in Ceph configuration step of deployment process in Onepanel
    And user of browser_op_panel clicks on Add OSD button in Ceph configuration step of deployment process in Onepanel
    And user of browser_op_panel types "1.5" to first OSD size input box in Ceph configuration step of deployment process in Onepanel
    And user of browser_op_panel sets "GiB" as size unit of first OSD in Ceph configuration step of deployment process in Onepanel

    And user of browser_op_panel clicks on Deploy button in Ceph configuration step of deployment process in Onepanel
    And user of browser_op_panel sees that cluster deployment has started

    # wait for finish of deployment
    And user of browser_oz_panel waits 180 seconds for cluster deployment to finish
    And user of browser_op_panel waits 180 seconds for cluster deployment to finish

    # setup IP step in zone panels
    And user of browser_oz_panel clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in zone panel
    And user of browser_oz_panel clicks on "Perform check" button in deployment setup DNS step
    And user of browser_oz_panel clicks on Proceed button in deployment setup DNS step
    And user of browser_oz_panel clicks on Yes button in warning modal in deployment setup DNS step

    # web cert in zone panel
    And user of browser_oz_panel deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_oz_panel clicks on Next step button in web cert step of deployment process in Onepanel

    # send registration token
    And user of browser_oz_panel clicks on Manage cluster via onezone button in last step of deployment process in Onepanel
    And user of browser_oz_panel logs as admin to Onezone service
    And user of browser_oz_panel clicks on add new provider cluster button in clusters menu
    And user of browser_oz_panel copies registration token from clusters page
    And user of browser_oz_panel sends copied token to user of browser_op_panel

    # step2 in provider panel
    And user of browser_op_panel types received registration token in step 2 of deployment process in Onepanel
    And user of browser_op_panel clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser_op_panel types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser_op_panel deactivates Request a subdomain toggle
    And user of browser_op_panel types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser_op_panel types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser_op_panel clicks on Register button in step 2 of deployment process in Onepanel
    And user of browser_op_panel is idle for 10 seconds

    # setup IP step in provider panel
    And user of browser_op_panel sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser_op_panel clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in provider panels
    And user of browser_op_panel clicks on "Perform check" button in deployment setup DNS step
    And user of browser_op_panel clicks on Proceed button in deployment setup DNS step

    # web cert in provider panel
    And user of browser_op_panel deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_op_panel clicks on Next step button in web cert step of deployment process in Onepanel


    # step5 in provider panel
    And user of browser_op_panel selects Local Ceph from storage selector in step 5 of deployment process in Onepanel
    And user of browser_op_panel types "test_ceph" to Storage name field in Local Ceph form in step 5 of deployment process in Onepanel
    And user of browser_op_panel clicks on Add button in add storage form in step 5 of deployment process in Onepanel
    And user of browser_op_panel sees an info notify with text matching to: .*[Ss]torage.*added.*

    And user of browser_op_panel expands "test_ceph" record on storages list in step 5 of deployment process in Onepanel
    And user of browser_op_panel sees that "test_ceph" Storage type is Local Ceph in step 5 of deployment process in Onepanel

    And user of browser_op_panel clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser_op_panel clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel

    # check config in zone and provider panels
    And user of browser_oz_panel clicks on Clusters in the main menu
    And user of browser_oz_panel clicks on "onezone" in clusters menu
    And user of browser_oz_panel clicks Nodes of "onezone" in the sidebar
    And user of browser_oz_panel sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*onezone.* host in Nodes page in Onepanel
    And user of browser_oz_panel sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*onezone.* host in Nodes page in Onepanel

    And user of browser_op_panel clicks on Nodes item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    Then user of browser_op_panel sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager, Ceph] options are enabled for .*oneprovider.* host in Nodes page in Onepanel
    And user of browser_op_panel sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager, Ceph] options cannot be changed for .*oneprovider.* host in Nodes page in Onepanel

    # check Ceph configuration
    And user of browser_op_panel clicks on Ceph item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_op_panel sees that OSDS limit is 1.5 GiB

    And user of browser_op_panel clicks on Configuration tab on Ceph page
    And user of browser_op_panel sees that cluster name is "ceph" on Ceph page
    And user of browser_op_panel opens Ceph nodes list on Ceph page
    And user of browser_op_panel sees that Manager & Monitor is enabled for Ceph node on Ceph page
    And user of browser_op_panel sees that ceph node has 1 OSD on Ceph page

    And user of browser_op_panel clicks on Pools tab on Ceph page
    And user of browser_op_panel clicks on "test_ceph" on pools list on Ceph page
    And user of browser_op_panel sees that pool usage of "test_ceph" is 0 B on Ceph page
 