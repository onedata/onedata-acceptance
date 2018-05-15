Feature: Basic spaces management utilities using onepanel

  Examples:
  | client1 | client2   | client3   |
  | REST    | web GUI   | REST      |
  | web GUI | REST      | REST      |

  Background:
    Given initial users configuration in "z1" Onezone service:
        - admin2:
            password: passwd
            user role: admin
        - user1
    And opened browsers with [admin, user1] logged to [p1 provider panel, z1 onezone] service


  Scenario Outline: Support space
    When using <client1>, user1 creates space "helloworld" in "z1" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld" in "z1" Onezone service and sends it to admin
    And using <client1>, admin supports "helloworld" space in "p1" Oneprovider panel service with following configuration:
        storage: NFS
        size: 1000000
    Then using <client2>, user1 sees that list of supporting providers for space named "helloworld" contains "p1" in "z1" Onezone service
    And using <client3>, user1 removes space named "helloworld" in "z1" Onezone service


  Scenario Outline: Revoke space support
    When using <client1>, user1 creates space "helloworld" in "z1" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld" in "z1" Onezone service and sends it to admin
    And using <client1>, admin supports "helloworld" space in "p1" Oneprovider panel service with following configuration:
        storage: NFS
        size: 1000000
    And using <client1>, user1 sees that list of supporting providers for space named "helloworld" contains "p1" in "z1" Onezone service
    And using <client2>, admin revokes "p1" provider space support for space named "helloworld" in "p1" Oneprovider panel service
    Then using <client1>, user1 sees that provider "p1" does not support space named "helloworld" in "z1" Onezone service
    And using <client3>, user1 removes space named "helloworld" in "z1" Onezone service
