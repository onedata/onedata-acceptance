Feature: Operations on newly created Local Ceph


  Background:
    Given directory tree structure on local file system:
            browser_oz_panel:
              file50.txt:
                size: 50 MiB
              file1.txt:
                content: 11111
              file2.txt:
                content: 22222


  Scenario: User supports space with newly created Local Ceph with 2 pools
    Given users opened [browser_oz_panel, browser_op_panel] browsers' windows
    And users of [browser_oz_panel, browser_op_panel] opened [onezone zone panel, oneprovider-1 provider panel] page
    And users of [browser_oz_panel, browser_op_panel] created admin accounts "admin:password"

    When user of browser_oz_panel clicks on Create Onezone cluster button in welcome page in Onepanel
    And user of browser_oz_panel sets options for .*onezone.* host in step 1 of deployment process with following configuration:
          zone: onezone
          options:
            - Database
            - Cluster Worker
            - Cluster Manager
            - Primary Cluster Manager

    And user of browser_op_panel clicks on Create Oneprovider cluster button in welcome page in Onepanel
    And user of browser_op_panel sets options for .*oneprovider.* host in step 1 of deployment process with following configuration:
          options:
            - Database
            - Cluster Worker
            - Cluster Manager
            - Primary Cluster Manager
            - Ceph

    And user of browser_op_panel deploys Ceph with following configuration:
          Manager And Monitor: True
          OSDs:
            - 1.5 GiB

    # wait for finish of deployment
    And user of browser_oz_panel waits 180 seconds for cluster deployment to finish
    And user of browser_op_panel waits 180 seconds for cluster deployment to finish

    # setup IP step in zone panels
    And user of browser_oz_panel clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in zone panel
    And user of browser_oz_panel performs DNS check in deployment setup DNS step and proceeds

    # web cert in zone panel
    And user of browser_oz_panel deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_oz_panel clicks on Next step button in web cert step of deployment process in Onepanel

    # send registration token
    And user of browser_oz_panel logs as admin, copies provider cluster registration token and sends it to user of browser_op_panel

    # step2 in provider panel
    And user of browser_op_panel types received registration token in step 2 of deployment process in Onepanel
    And user of browser_op_panel clicks proceed button in step 2 of deployment process in Onepanel

    And user of browser_op_panel registers provider in step 2 of deployment process in Onepanel with following config:
          provider: oneprovider-1
          request a subdomain: False
          email: admin@admin.email

    # setup IP step in provider panel
    And user of browser_op_panel sees that IP address of "oneprovider-1" host is that of "oneprovider-1" in deployment setup IP step
    And user of browser_op_panel clicks on "Setup IP addresses" button in deployment setup IP step

    # setup DNS in provider panels
    And user of browser_op_panel clicks on "Perform check" button in deployment setup DNS step
    And user of browser_op_panel clicks on Proceed button in deployment setup DNS step

    # web cert in provider panel
    And user of browser_op_panel deactivates lets encrypt toggle in web cert step of deployment process in Onepanel
    And user of browser_op_panel clicks on Next step button in web cert step of deployment process in Onepanel

    And user of browser_op_panel adds storage in step 5 of deployment process in Onepanel with following config:
          storage type: Local Ceph
          name: test_ceph

    And user of browser_op_panel expands "test_ceph" record on storages list in step 5 of deployment process in Onepanel
    And user of browser_op_panel sees that "test_ceph" Storage type is Local Ceph in step 5 of deployment process in Onepanel

    And user of browser_op_panel clicks on Finish button in step 5 of deployment process in Onepanel
    And user of browser_op_panel clicks on link to go to Emergency Onepanel interface in last step of deployment process in Onepanel

    # add second pool
    And user of browser_op_panel clicks on Clusters in the main menu
    And user of browser_op_panel clicks on Ceph item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_op_panel clicks on Pools tab on Ceph page

    And user of browser_op_panel clicks on "Create pool" button on Ceph page
    And user of browser_op_panel types "test_ceph2" to Storage name field in Local Ceph form in storages page in Onepanel
    And user of browser_op_panel clicks on Add button in add storage form in storages page in Onepanel

    And user of browser_op_panel clicks on "test_ceph" on pools list on Ceph page
    And user of browser_op_panel sees that pool usage of "test_ceph" is 0 B on Ceph page

    And user of browser_op_panel clicks on "test_ceph2" on pools list on Ceph page
    And user of browser_op_panel sees that pool usage of "test_ceph2" is 0 B on Ceph page

    # create and support space
    And user of browser_oz_panel creates "space1" space in Onezone
    And user of browser_oz_panel sends support token for "space1" to user of browser_oz_panel
    And user of browser_oz_panel opens "oneprovider-1" clusters submenu
    And user of browser_oz_panel supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: test_ceph
          size: 1024

    And user of browser_op_panel clicks on Status tab on Ceph page
    Then user of browser_op_panel sees that OSDS usage is 1 GiB

    And user of browser_oz_panel creates "space2" space in Onezone
    And user of browser_oz_panel sends support token for "space2" to user of browser_oz_panel
    And user of browser_oz_panel opens "oneprovider-1" clusters submenu
    And user of browser_oz_panel supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: test_ceph2
          size: 1024

    # upload file and check if download works
    And user of browser_oz_panel opens file browser for "space1" space
    And user of browser_oz_panel uses upload button from file browser menu bar to upload local file "file1.txt" to remote current dir
    And user of browser_oz_panel uses upload button from file browser menu bar to upload local file "file50.txt" to remote current dir
    And user of browser_oz_panel double clicks on item named "file1.txt" in file browser
    And user of browser_oz_panel sees that content of downloaded file "file1.txt" is equal to: "11111"

    And user of browser_oz_panel opens file browser for "space2" space
    And user of browser_oz_panel uses upload button from file browser menu bar to upload local file "file2.txt" to remote current dir
    And user of browser_oz_panel uses upload button from file browser menu bar to upload local file "file50.txt" to remote current dir
    And user of browser_oz_panel double clicks on item named "file2.txt" in file browser
    And user of browser_oz_panel sees that content of downloaded file "file2.txt" is equal to: "22222"

    # check storage occupation
    And user of browser_op_panel clicks on Pools tab on Ceph page
    And user of browser_op_panel clicks on "test_ceph" on pools list on Ceph page
    And user of browser_op_panel sees that pool usage of "test_ceph" is about 50 MiB on Ceph page
    And user of browser_op_panel clicks on "test_ceph2" on pools list on Ceph page
    And user of browser_op_panel sees that pool usage of "test_ceph2" is about 50 MiB on Ceph page

