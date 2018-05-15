Feature: Provider management in Onepanel

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      |

  Background:
    Given initial users configuration in "z1" Onezone service:
            - user1:
                password: password
                user role: admin
    And initial spaces configuration in "z1" Onezone service:
        space1:
            owner: user1
            providers:
                - p1:
                    storage: NFS
                    size: 1000000
    And opened browsers with [admin, user1] logged to [p1 provider panel, z1 onezone] service


  Scenario Outline: User changes provider name and domain using <client2> and he sees in <client1> that they have changed
    When using <client2>, user1 sees provider named "p1" with hostname matches that of "p1" provider in "z1" Onezone service
    And using <client1>, admin modifies provider "p1" changing his name to "pro1" and domain to "node1.p1.local.test" in "p1" Oneprovider panel service
    And using <client2>, user1 is idle for 8 seconds
    Then using <client2>, user1 sees provider named "pro1" with hostname "node1.p1.local.test" in "z1" Onezone service
    And using <client1>, admin modifies provider "pro1" changing his name to "p1" and domain to match that of "p1" provider in "p1" Oneprovider panel service


  Scenario Outline: User deregisters provider and registers it again
    When using <client2>, user1 sees provider named "p1" with hostname matches that of "p1" provider in "z1" Onezone service
    And using <client1>, admin deregisters provider in "p1" Oneprovider panel service
    And using <client2>, user1 is idle for 8 seconds
    Then using <client2>, user1 sees that provider "p1" has been deregistered in "z1" Onezone service
    And using <client1>, admin registers provider in "z1" Onezone service with following configuration:
          provider name: p1
          domain:
              of provider: oneprovider-1
          zone domain:
              of zone: z1
          storages:
              NFS:
                type: posix
                mount point: /volumes/storage
          admin email: admin@onedata.org
