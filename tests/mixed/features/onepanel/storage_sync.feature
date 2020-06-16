Feature: Onepanel features regarding storage sync (e.g. import/update)


  Examples:
    | client1   | client2   | client3   |
    | web GUI   | REST      | REST      |
    | REST      | web GUI   | REST      |


  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1:
              password: password
              user role: onezone admin
              cluster privileges:
                  - oz_spaces_list
                  - oz_providers_list
    And opened browsers with [onepanel, user1] signed in to [emergency interface of Onepanel, onezone] service
    And directory tree structure on local file system:
          user1:
              - dir1: 5
              - dir2:
                  - dir21:
                      - dir211:
                          - dir2111: 4
                      - file2.txt: 11111
                  - dir22: 10
                  - file1.txt: 22222


  Scenario Outline: User supports space with storage sync and enabled options: Mount in root
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space2" in "onezone" Onezone service
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client1>, user1 generates space support token for space named "space2" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          mount in root: True
          storage import:
                strategy: Simple scan
                max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space2" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space2" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space2" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space2" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space2" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space2" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space2" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space2" in "onezone" Onezone service


  Scenario Outline: User supports space with storage sync with no options enabled
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space_2" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space_2" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space_2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
              max depth: 2
              strategy: Simple scan
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space_2" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space_2" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space_2" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space_2" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space_2" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space_2" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space_2" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space_2" in "onezone" Onezone service


  Scenario: User supports space with storage sync and enabled options: Delete
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space3" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space3" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
                strategy: Simple scan
                max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space3" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space3" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space3" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: true
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space3" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: true
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2/dir21 from provider's storage mount point
    And using docker, user1 removes dir2/file1.txt from provider's storage mount point
    And using web GUI, user1 is idle for 1 seconds
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 1
          - dir2:
              - dir22: 10
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space3" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space3" in "onezone" Onezone service


  Scenario: User supports space with storage sync and enabled options: Write once
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space4" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space4" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space4" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
                strategy: Simple scan
                max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space4" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space4" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space4" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space4" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space4" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: false
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space4" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space4" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space4" in "onezone" Onezone service


  Scenario: User supports space with storage sync and enabled options: Delete and Write once
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space5" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space5" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space5" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
                strategy: Simple scan
                max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space5" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space5" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space5" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: true
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space5" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: true
          Delete enabled: true
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2/dir21 from provider's storage mount point
    And using docker, user1 removes dir2/file1.txt from provider's storage mount point
    And using web GUI, user1 is idle for 1 seconds
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 1
          - dir2:
              - dir22: 10
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space5" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space5" in "onezone" Onezone service


  Scenario: User disables files update
    Given there are no spaces supported by oneprovider-1 in Onepanel
    And there is "new_storage" storage in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
          imported storage: true
    When using <client1>, user1 creates space "space7" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space7" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space7" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
                strategy: Simple scan
                max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space7" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space7" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space7" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space7" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space7" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using web GUI, user1 is idle for 5 seconds
    And using <client1>, user1 sees that content for "space7" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space7" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Disabled
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space7" in "oneprovider-1" is as follow:
          Update strategy: Disabled
    And using docker, user1 copies dir1 to dir2 provider's storage mount point
    And using web GUI, user1 is idle for 1 seconds
    And using <client1>, user1 sees that content for "space7" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 3
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2 from provider's storage mount point
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space7" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space7" in "onezone" Onezone service
