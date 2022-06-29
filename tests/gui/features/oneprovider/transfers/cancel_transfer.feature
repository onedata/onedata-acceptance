Feature: Cancel transfer test

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial "new_storage" storage configuration in "oneprovider-1" Onezone service:
        type: "nulldevice"
        importedStorage: true
        lumaFeed: "auto"
        simulatedFilesystemParameters: "0-1:20485760000"
        skipStorageDetection: true
        storagePathType: "canonical"
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: new_storage
                    size: 100000000000
                - oneprovider-2:
                    storage: SlowNullStorage
                    size: 100000000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User reruns directory transfer to remote provider after canceling it
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
    And user of browser replicates "0" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser cancels transfer in waiting transfers
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: "0"
            destination: oneprovider-2
            transferred: <= 19.1 GB
            type: replication
            status: cancelled
    Then user of browser reruns transfer in ended transfers
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: "0"
            destination: oneprovider-2
            transferred: <= 19.1 GB
            type: replication
            status: completed
