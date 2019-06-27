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
    When using <client1>, user1 creates space "space2" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space2" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client2>, onepanel supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
        mount in root: True
        storage import:
          max depth: 2
          strategy: Simple scan
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
    And using <client1>, user1 sees that content for "space2" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space2" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space2" in "onezone" Onezone service


  Scenario Outline: User supports space with storage sync with no options enabled
    When using <client1>, user1 creates space "space1" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space1" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
    And using <client2>, onepanel copies Id of "space1" space in Spaces page in Onepanel
    And using docker, user1 copies dir2 to the root directory of "space1" space
    And using <client2>, onepanel configures IMPORT parameters for "space1" in "oneprovider-1" Oneprovider panel service as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space1" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space1" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space1" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space1" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space1" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client1>, user1 sees that content for "space1" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space1" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space1" in "onezone" Onezone service


  Scenario: User supports space with storage sync and enabled options: Delete
    When using <client1>, user1 creates space "space3" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space3" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
    And using <client2>, onepanel copies Id of "space3" space in Spaces page in Onepanel
    And using docker, user1 copies dir2 to the root directory of "space3" space
    And using <client2>, onepanel configures IMPORT parameters for "space3" in "oneprovider-1" Oneprovider panel service as follow:
          Import strategy: Simple scan
          Max depth: 2
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
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2/dir21 from the root directory of "space3" space
    And using docker, user1 removes dir2/file1.txt from the root directory of "space3" space
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 1
          - dir2:
              - dir22: 10
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space3" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space3" in "onezone" Onezone service

  Scenario: User supports space with storage sync and enabled options: Write once
    When using <client1>, user1 creates space "space4" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space4" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space4" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
    And using <client2>, onepanel copies Id of "space4" space in Spaces page in Onepanel
    And using docker, user1 copies dir2 to the root directory of "space4" space
    And using <client2>, onepanel configures IMPORT parameters for "space4" in "oneprovider-1" Oneprovider panel service as follow:
            Import strategy: Simple scan
            Max depth: 2
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
    And using <client1>, user1 sees that content for "space4" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space4" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space4" in "onezone" Onezone service


  Scenario: User supports space with storage sync and enabled options: Delete and Write once
    When using <client1>, user1 creates space "space5" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space5" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space5" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
    And using <client2>, onepanel copies Id of "space5" space in Spaces page in Onepanel
    And using docker, user1 copies dir2 to the root directory of "space5" space
    And using <client2>, onepanel configures IMPORT parameters for "space5" in "oneprovider-1" Oneprovider panel service as follow:
            Import strategy: Simple scan
            Max depth: 2
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
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user1 removes dir2/dir21 from the root directory of "space5" space
    And using docker, user1 removes dir2/file1.txt from the root directory of "space5" space
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 1
          - dir2:
              - dir22: 10
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space5" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space5" in "onezone" Onezone service


  Scenario: User disables files update
    When using <client1>, user1 creates space "space6" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space6" in "onezone" Onezone service and sends it to onepanel
    And using <client2>, onepanel supports "space6" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: "posix"
        size: 1000000
    And using <client2>, onepanel copies Id of "space6" space in Spaces page in Onepanel
    And using docker, user1 copies dir2 to the root directory of "space6" space
    And using <client2>, onepanel configures IMPORT parameters for "space6" in "oneprovider-1" Oneprovider panel service as follow:
            Import strategy: Simple scan
            Max depth: 2
    And using <client2>, onepanel sees that IMPORT strategy configuration for "space6" in "oneprovider-1" is as follow:
          Import strategy: Simple scan
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space6" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space6" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space6" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space6" in "oneprovider-1" is as follow:
          Update strategy: Simple scan
          Max depth: 3
          Scan interval [s]: 1
          Write once: false
          Delete enabled: false
    And using <client1>, user1 sees that content for "space6" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using <client2>, onepanel configures UPDATE parameters for "space6" in "oneprovider-1" Oneprovider panel service as follow:
          Update strategy: Disabled
    And using <client2>, onepanel sees that UPDATE strategy configuration for "space6" in "oneprovider-1" is as follow:
          Update strategy: Disabled
    And using docker, user1 copies dir1 to dir2 regular directory of "space6" space
    And using <client1>, user1 sees that content for "space6" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 3
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "space6" in "oneprovider-1" Oneprovider panel service
    And using <client3>, user1 removes space named "space6" in "onezone" Onezone service
