Feature: Multiuser
  Multiuser operations on spaces in Onezone using GUI and REST API

  Examples:
  | client1 | client2   | client3   |
  | web GUI | web GUI   | REST      |
  | REST    | REST      | web GUI   |
  | web GUI | REST      | REST      |
  | REST    | web GUI   | web GUI   |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browsers with [user1, user2] signed in to [onezone, onezone] service

  Scenario Outline: User invites other user to space using <client1>, that user joins to space using <client2> and using <client3> he sees that he has joined to new space
    When using <client1>, user2 invites user1 to space named "space1" in "onezone" Onezone service
    And using <client2>, user1 joins to space using received space invitation token in "onezone" Onezone service
    Then using <client3>, user1 sees that space named "space1" has appeared in "onezone" Onezone service
    And using <client1>, user2 sees that user1 is member of "space1" in "onezone" Onezone service
