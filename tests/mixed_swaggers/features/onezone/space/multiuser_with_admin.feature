Feature: Multiuser with admin
  Multiuser operations on spaces, where one user is admin, in Onezone
  using GUI and REST API

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |

  Background:
    Given initial users configuration in "z1" Onezone service:
            - user1
            - admin2:
                password: passwd
                user role: admin
    And initial spaces configuration in "z1" Onezone service:
        space1:
            owner: admin2
            providers:
                - p1:
                    storage: NFS
                    size: 1000000
    And opened browsers with [user1, admin2] logged to [z1 onezone, z1 onezone] service


  Scenario Outline: Admin user adds other user to space using <client1> and that user using <client2> sees that he has been added
    When using <client1>, admin2 adds user1 to "space1" in "z1" Onezone service
    Then using <client2>, user1 sees that space named "space1" has appeared in "z1" Onezone service


  Scenario Outline: Admin user removes other user from space using <client1> and that user using <client2> sees that he has been removed
    When using <client1>, admin2 adds user1 to "space1" in "z1" Onezone service
    And using <client2>, user1 sees that space named "space1" has appeared in "z1" Onezone service
    And using <client1>, admin2 removes user1 from space "space1" in "z1" Onezone service
    Then using <client2>, user1 sees that space named "space1" has disappeared from "z1" Onezone service
