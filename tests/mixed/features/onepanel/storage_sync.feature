Feature: Onepanel features regarding storage sync (e.g. import)


  Examples:
    | client1   | client2   |
    | web GUI   | REST      |
    | REST      | web GUI   |


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
            dir1: 5
            dir2:
              dir21:
                dir211:
                  dir2111: 4
                file2.txt:
                  content: 11111
              dir22: 10
              file1.txt:
                content: 22222

    And there are no spaces supported by oneprovider-1 in Onepanel
    And "new_storage" storage backend in "oneprovider-1" Oneprovider panel service used by user of onepanel with following configuration:
          storage type: POSIX
          mount point: /volumes/posix
          imported storage: true


  Scenario Outline: Files tree with specified depth is imported to space after changing max depth option
    When using <client1>, user1 creates space "space1" in "onezone" Onezone service
    And using docker, user1 copies dir2 to provider's storage mount point
    And using <client1>, user1 generates space support token for space named "space1" in "onezone" Onezone service and sends it to onepanel
    And using web GUI, onepanel refreshes site
    And using <client2>, onepanel supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
            continuous scan: true
            max depth: 2
            scan interval [s]: 1
            detect modifications: true
            detect deletions: false
    And using <client2>, onepanel sees that import strategy configuration for "space1" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 2
          Scan interval [s]: 1
          Detect modifications: true
          Detect deletions: false
    And using <client1>, user1 sees that list of supporting providers for space named "space1" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space1" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures import parameters for "space1" in "oneprovider-1" Oneprovider panel service as follow:
          continuous scan: true
          max depth: 3
    And using <client2>, onepanel sees that import strategy configuration for "space1" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 3
          Scan interval [s]: 1
          Detect modifications: true
          Detect deletions: false
    And user is idle for 5 seconds
    Then using <client1>, user1 sees that content for "space1" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user removes dir2 from provider's storage mount point
    And using REST, user1 removes space named "space1" in "onezone" Onezone service


  Scenario: Files tree with specified depth is imported to space after changing import depth and enable delete detection option
    When using <client1>, user1 creates space "space3" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space3" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using web GUI, onepanel refreshes site
    And using <client2>, onepanel supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
            continuous scan: true
            max depth: 2
            detect deletions: false
    And using <client2>, onepanel sees that import strategy configuration for "space3" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 2
          Detect deletions: false
    And using <client1>, user1 sees that list of supporting providers for space named "space3" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures import parameters for "space3" in "oneprovider-1" Oneprovider panel service as follow:
          continuous scan: true
          max depth: 3
          scan interval [s]: 1
          detect deletions: true
    And using <client2>, onepanel sees that import strategy configuration for "space3" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 3
          Scan interval [s]: 1
          Detect modifications: true
          Detect deletions: true
    And user is idle for 5 seconds
    Then using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21:
                  - dir211
                  - file2.txt: 11111
              - dir22: 10
              - file1.txt: 22222
    And using docker, user removes dir2/dir21 from provider's storage mount point
    And using docker, user removes dir2/file1.txt from provider's storage mount point
    And user is idle for 20 seconds
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2: 1
    And using <client1>, user1 sees that content for "space3" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir22: 10
    And using docker, user removes dir2 from provider's storage mount point
    And using REST, user1 removes space named "space3" in "onezone" Onezone service


  Scenario: Files tree with specified depth is imported to space after changing import depth and disable modification detection option
    When using <client1>, user1 creates space "space4" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space4" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using web GUI, onepanel refreshes site
    And using <client2>, onepanel supports "space4" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
            continuous scan: true
            max depth: 2
    And using <client2>, onepanel sees that import strategy configuration for "space4" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space4" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space4" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures import parameters for "space4" in "oneprovider-1" Oneprovider panel service as follow:
          continuous scan: true
          max depth: 3
          scan interval [s]: 1
          detect modifications: false
    And using <client2>, onepanel sees that import strategy configuration for "space4" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 3
          Scan interval [s]: 1
          Detect modifications: false
    And user is idle for 5 seconds
    Then using <client1>, user1 sees that content for "space4" in "oneprovider-1" Oneprovider service is as follow:
           - dir2:
               - dir21:
                   - dir211
                   - file2.txt: 11111
               - dir22: 10
               - file1.txt: 22222
    And using docker, user removes dir2 from provider's storage mount point
    And using REST, user1 removes space named "space4" in "onezone" Onezone service


  Scenario: Files tree with specified depth is imported to space after changing max depth, enabling delete and disabling modification detection
    When using <client1>, user1 creates space "space5" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space5" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using web GUI, onepanel refreshes site
    And using <client2>, onepanel supports "space5" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
            continuous scan: true
            max depth: 2
    And using <client2>, onepanel sees that import strategy configuration for "space5" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space5" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures import parameters for "space5" in "oneprovider-1" Oneprovider panel service as follow:
          continuous scan: true
          max depth: 3
          scan interval [s]: 1
          detect modifications: false
          detect deletions: true
    And using <client2>, onepanel sees that import strategy configuration for "space5" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 3
          Scan interval [s]: 1
          Detect modifications: false
          Detect deletions: true
    And user is idle for 10 seconds
    Then using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
           - dir2:
               - dir21:
                   - dir211
                   - file2.txt: 11111
               - dir22: 10
               - file1.txt: 22222
    And using docker, user removes dir2/dir21 from provider's storage mount point
    And using docker, user removes dir2/file1.txt from provider's storage mount point
    And user is idle for 10 seconds
    And using <client1>, user1 sees that content for "space5" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir22: 10
    And using docker, user removes dir2 from provider's storage mount point
    And using REST, user1 removes space named "space5" in "onezone" Onezone service


  Scenario: User does not see files tree changes after disabling continuous scan option
    When using <client1>, user1 creates space "space7" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "space7" in "onezone" Onezone service and sends it to onepanel
    And using docker, user1 copies dir2 to provider's storage mount point
    And using web GUI, onepanel refreshes site
    And using <client2>, onepanel supports "space7" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: "new_storage (import-enabled)"
          size: 1000000
          storage import:
            continuous scan: true
            max depth: 2
    And using <client2>, onepanel sees that import strategy configuration for "space7" in "oneprovider-1" is as follow:
          Continuous scan: true
          Max depth: 2
    And using <client1>, user1 sees that list of supporting providers for space named "space7" contains "oneprovider-1" in "onezone" Onezone service
    And using <client1>, user1 sees that content for "space7" in "oneprovider-1" Oneprovider service is as follow:
          - dir2:
              - dir21
              - dir22
              - file1.txt: 22222
    And using <client2>, onepanel configures import parameters for "space7" in "oneprovider-1" Oneprovider panel service as follow:
          continuous scan: false
    And using <client2>, onepanel sees that import strategy configuration for "space7" in "oneprovider-1" is as follow:
          Continuous scan: false
    And using docker, user1 copies dir1 to dir2 provider's storage mount point
    And user is idle for 3 seconds
    Then using <client1>, user1 sees that content for "space7" in "oneprovider-1" Oneprovider service is as follow:
           - dir2:
               - dir21
               - dir22
               - file1.txt: 22222
    And using docker, user removes dir2 from provider's storage mount point
    And using REST, user1 removes space named "space7" in "onezone" Onezone service
