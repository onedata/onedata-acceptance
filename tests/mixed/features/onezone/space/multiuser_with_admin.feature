Feature: Multiuser with admin
  Multiuser operations on spaces, where one user is admin, in Onezone
  using GUI and REST API

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - admin2:
                password: password
                user role: admin
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: admin2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browsers with [user1, admin2] logged to [onezone, onezone] service


  Scenario: Admin user adds other user to space using <client1> and that user using <client2> sees that he has been added
    When using REST, admin2 adds user1 to "space1" in "onezone" Onezone service
    Then using web GUI, user1 sees that space named "space1" has appeared in "onezone" Onezone service


  Scenario: Admin user removes other user from space using <client1> and that user using <client2> sees that he has been removed
    When using REST, admin2 adds user1 to "space1" in "onezone" Onezone service
    And using web GUI, user1 sees that space named "space1" has appeared in "onezone" Onezone service
    And using REST, admin2 removes user1 from space "space1" in "onezone" Onezone service
    Then using web GUI, user1 sees that space named "space1" has disappeared from "onezone" Onezone service
