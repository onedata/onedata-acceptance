Feature: Operations on newly created Local Ceph


  Background:
    Given directory tree structure on local file system:
          browser_onezone:
              file1.txt:
                size: 50 MiB
              file3.txt:
                content: 11111
              file2.txt:
                size: 50 MiB
              file4.txt:
                content: 22222


  Scenario: User supports space with newly created Local Ceph with 2 pools
    Given users opened [browser_onezone, browser_provider] browsers' windows
    And users of [browser_onezone, browser_provider] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of [browser_onezone, browser_provider] created admin accounts "admin:password"

    # step1 in zone and provider panels
    When user of browser_onezone clicks on Create Onezone cluster button in welcome page in Onepanel
    And user of browser_onezone enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options for .*onezone.* host in step 1 of deployment process in Onepanel
    And user of browser_onezone types name of "onezone" zone to Zone name field in step 1 of deployment process in Onepanel
    And user of browser_onezone types hostname of "onezone" zone to Zone domain name field in step 1 of deployment process in Onepanel
    And user of browser_onezone clicks on Deploy button in step 1 of deployment process in Onepanel
    And user of browser_onezone sees that cluster deployment has started

    And user of browser_provider clicks on Create Oneprovider cluster button in welcome page in Onepanel
    And user of browser_provider enables [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager, Ceph] options for .*oneprovider.* host in step 1 of deployment process in Onepanel
    And user of browser_provider clicks on Deploy button in step 1 of deployment process in Onepanel

    # ceph configuration
    And user of browser_provider enables "Manager & Monitor" toggle in ceph configuration step of deployment process in Onepanel
    And user of browser_provider clicks on Add OSD button in ceph configuration step of deployment process in Onepanel
    And user of browser_provider types "3" to first OSD size input box in ceph configuration step of deployment process in Onepanel
    And user of browser_provider sets "GiB" as size unit of first OSD in ceph configuration step of deployment process in Onepanel

    And user of browser_provider clicks on Deploy button in ceph configuration step of deployment process in Onepanel
    And user of browser_provider sees that cluster deployment has started

    # wait for finish of deployment
    And user of browser_onezone waits 180 seconds for cluster deployment to finish
    And user of browser_provider waits 180 seconds for cluster deployment to finish

    # setup IP step in zone panels
    And user of browser_onezone clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in zone panel
    And user of browser_onezone clicks on "Perform check" button in deployment setup DNS step
    And user of browser_onezone clicks on Proceed button in deployment setup DNS step
    And user of browser_onezone clicks on Yes button in warning modal in deployment setup DNS step

    # web cert in zone panel
    And user of browser_onezone deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_onezone clicks on Next step button in web cert step of deployment process in Onepanel

    # send registration token
    And user of browser_onezone clicks on Manage cluster via onezone button in last step of deployment process in Onepanel
    And user of browser_onezone logs as admin to Onezone service
    And user of browser_onezone clicks on add new provider cluster button in clusters menu
    And user of browser_onezone copies registration token from clusters page
    And user of browser_onezone sends copied token to user of browser_provider

    # step2 in provider panel
    And user of browser_provider types received registration token in step 2 of deployment process in Onepanel
    And user of browser_provider clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser_provider types name of "oneprovider-1" provider to Provider name field in step 2 of deployment process in Onepanel
    And user of browser_provider deactivates Request a subdomain toggle
    And user of browser_provider types hostname of "oneprovider-1" provider to domain field in step 2 of deployment process in Onepanel
    And user of browser_provider types "admin@admin.email" to admin email field in step 2 of deployment process in Onepanel
    And user of browser_provider clicks on Register button in step 2 of deployment process in Onepanel
    And user of browser_provider is idle for 10 seconds

    # setup IP step in provider panel
    And user of browser_provider sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser_provider clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in provider panels
    And user of browser_provider clicks on "Perform check" button in deployment setup DNS step
    And user of browser_provider clicks on Proceed button in deployment setup DNS step

    # web cert in provider panel
    And user of browser_provider deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_provider clicks on Next step button in web cert step of deployment process in Onepanel


    # step5 in provider panel
    And user of browser_provider selects Local Ceph from storage selector in step 5 of deployment process in Onepanel
    And user of browser_provider types "test_ceph" to Storage name field in Local Ceph form in step 5 of deployment process in Onepanel
    And user of browser_provider clicks on Add button in add storage form in step 5 of deployment process in Onepanel
    And user of browser_provider sees an info notify with text matching to: .*[Ss]torage.*added.*

    And user of browser_provider expands "test_ceph" record on storages list in step 5 of deployment process in Onepanel
    And user of browser_provider sees that "test_ceph" Storage type is Local Ceph in step 5 of deployment process in Onepanel

    And user of browser_provider clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser_provider clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel

    # add second pool
    And user of browser_provider clicks on Clusters in the main menu
    And user of browser_provider clicks on Ceph item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_provider clicks on Pools tab on Ceph page

    And user of browser_provider clicks on "Create pool" button on Ceph page
    And user of browser_provider types "test_ceph2" to Storage name field in Local Ceph form in storages page in Onepanel
    And user of browser_provider clicks on Add button in add storage form in storages page in Onepanel

    And user of browser_provider clicks on "test_ceph" on pools list on Ceph page
    And user of browser_provider sees that pool usage of "test_ceph" is 0 B on Ceph Page

    And user of browser_provider clicks on "test_ceph2" on pools list on Ceph page
    And user of browser_provider sees that pool usage of "test_ceph2" is 0 B on Ceph Page

    # create and support space
    And user of browser_onezone creates "space1" space in Onezone
    And user of browser_onezone sends support token for "space1" to user of browser_onezone
    And user of browser_onezone opens "oneprovider-1" clusters submenu
    And user of browser_onezone supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: test_ceph
          size: 1024

    And user of browser_provider clicks on Status tab on Ceph page
    Then user of browser_provider sees that OSDS usage is 1 GiB

    And user of browser_onezone creates "space2" space in Onezone
    And user of browser_onezone sends support token for "space2" to user of browser_onezone
    And user of browser_onezone opens "oneprovider-1" clusters submenu
    And user of browser_onezone supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: test_ceph2
          size: 1024

    # upload file and check if download works
    And user of browser_onezone opens file browser for "space1" space
    And user of browser_onezone uses upload button from file browser menu bar to upload local file "file1.txt" to remote current dir
    And user of browser_onezone uses upload button from file browser menu bar to upload local file "file3.txt" to remote current dir
    And user of browser_onezone double clicks on item named "file3.txt" in file browser
    And user of browser_onezone sees that content of downloaded file "file3.txt" is equal to: "11111"

    And user of browser_onezone opens file browser for "space2" space
    And user of browser_onezone uses upload button from file browser menu bar to upload local file "file2.txt" to remote current dir
    And user of browser_onezone uses upload button from file browser menu bar to upload local file "file4.txt" to remote current dir
    And user of browser_onezone double clicks on item named "file4.txt" in file browser
    And user of browser_onezone sees that content of downloaded file "file4.txt" is equal to: "22222"

    # check storage occupation
    And user of browser_provider clicks on Pools tab on Ceph page
    And user of browser_provider clicks on "test_ceph" on pools list on Ceph page
    And user of browser_provider sees that pool usage of "test_ceph" is about 50 MiB on Ceph Page
    And user of browser_provider clicks on "test_ceph2" on pools list on Ceph page
    And user of browser_provider sees that pool usage of "test_ceph2" is about 50 MiB on Ceph Page

