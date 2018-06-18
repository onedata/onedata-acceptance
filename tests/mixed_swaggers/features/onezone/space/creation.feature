Feature: Creation
  Space creation methods in Onezone using GUI and REST API

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And opened browser with user1 logged to "onezone onezone" service


  Scenario Outline: User creates space using <client1> and using <client2> he sees that it has appeared
    When using <client1>, user1 creates space "helloworld" in "onezone" Onezone service
    Then using <client2>, user1 sees that space named "helloworld" has appeared in "onezone" Onezone service

