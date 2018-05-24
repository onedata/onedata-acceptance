Feature: Provider management in Onepanel

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                password: password
                user role: admin
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browsers with [admin, user1] logged to [oneprovider-1 provider panel, onezone onezone] service


  Scenario Outline: User changes provider name and domain using <client2> and he sees in <client1> that they have changed
    When using <client2>, user1 sees provider "oneprovider-1" with hostname matches that of "oneprovider-1" provider in "onezone" Onezone service
    And using <client1>, admin modifies provider "oneprovider-1" changing his name to "pro1" and domain to test domain in "oneprovider-1" Oneprovider panel service
    And using <client2>, user1 is idle for 8 seconds
    Then using <client2>, user1 sees provider named "pro1" with test hostname of provider "oneprovider-1" in "onezone" Onezone service
    And using <client1>, admin modifies provider named "pro1" changing his name and domain to match that of "oneprovider-1" provider in "oneprovider-1" Oneprovider panel service


  Scenario Outline: User deregisters provider and registers it again
    When using <client2>, user1 sees provider "oneprovider-1" with hostname matches that of "oneprovider-1" provider in "onezone" Onezone service
    And using <client1>, admin deregisters provider in "oneprovider-1" Oneprovider panel service
    And using <client2>, user1 is idle for 8 seconds
    Then using <client2>, user1 sees that provider "oneprovider-1" has been deregistered in "onezone" Onezone service
    And using <client1>, admin registers provider in "onezone" Onezone service with following configuration:
          provider name:
              of provider: oneprovider-1
          domain:
              of provider: oneprovider-1
          zone domain:
              of zone: onezone
          storages:
              posix:
                type: posix
                mount point: /volumes/storage
          admin email: admin@onedata.org
