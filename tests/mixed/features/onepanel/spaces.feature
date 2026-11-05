Feature: Basic spaces management utilities using onepanel


# TODO: uncomment after space support revoke fixes in 21.02 (VFS-6383)
#  Examples:
#  | client1 | client2   | client3   |
#  | REST    | web GUI   | REST      |
#  | web GUI | REST      | REST      |

  Background:
    Given initial users configuration in "onezone" Onezone service:
        - user1
    And opened browsers with [onepanel, user1] signed in to [emergency interface of Onepanel, onezone] service


  Scenario Outline: Support space
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using <client1>, user1 creates space "helloworld" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using <client1>, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using <client2>, user1 sees that list of supporting providers for space named "helloworld" contains "oneprovider-1" in "onezone" Onezone service
    And using <client3>, user1 removes space named "helloworld" in "onezone" Onezone service

# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
    Examples:
    | client1 | client2   | client3   |
    | REST    | web GUI   | REST      |
    | web GUI | REST      | REST      |


  Scenario Outline: Revoke space support
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using <client1>, user1 creates space "helloworld2" in "onezone" Onezone service
    And using <client1>, user1 generates space support token for space named "helloworld2" in "onezone" Onezone service and sends it to onepanel
    And using <client1>, onepanel supports "helloworld2" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using <client1>, user1 sees that list of supporting providers for space named "helloworld2" contains "oneprovider-1" in "onezone" Onezone service
    And using <client2>, onepanel revokes "oneprovider-1" provider space support for space named "helloworld2" in "oneprovider-1" Oneprovider panel service
    And using web GUI, user1 refreshes site
    Then using <client1>, user1 sees that provider "oneprovider-1" does not support space named "helloworld2" in "onezone" Onezone service
    And using <client3>, user1 removes space named "helloworld2" in "onezone" Onezone service

# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
    Examples:
    | client1 | client2   | client3   |
    | web GUI | REST      | REST      |