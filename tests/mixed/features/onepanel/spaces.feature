Feature: Basic spaces management utilities using onepanel

  Examples:
  | client1 | client2   | client3   |
  | REST    | web GUI   | REST      |
  | web GUI | REST      | REST      |

  Background:
    Given initial users configuration in "onezone" Onezone service:
        - admin2:
            password: password
            user role: admin
        - user1
    And opened browsers with [admin, user1] logged to [oneprovider-1 provider panel, onezone] service


  Scenario Outline: Support space
    When using <client1>, user1 creates space "helloworld" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to admin
    And using <client1>, admin supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using <client2>, user1 sees that list of supporting providers for space named "helloworld" contains "oneprovider-1" in "onezone" Onezone service
    And using <client3>, user1 removes space named "helloworld" in "onezone" Onezone service


  Scenario Outline: Revoke space support
    When using <client1>, user1 creates space "helloworld" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to admin
    And using <client1>, admin supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using <client1>, user1 sees that list of supporting providers for space named "helloworld" contains "oneprovider-1" in "onezone" Onezone service
    And using <client2>, admin revokes "oneprovider-1" provider space support for space named "helloworld" in "oneprovider-1" Oneprovider panel service
    Then using <client1>, user1 sees that provider "oneprovider-1" does not support space named "helloworld" in "onezone" Onezone service
    And using <client3>, user1 removes space named "helloworld" in "onezone" Onezone service
