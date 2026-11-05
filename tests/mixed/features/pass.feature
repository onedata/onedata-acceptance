Feature: Pass test

  Background:
    # this step ensures that deleting users at the end of the tests succeed
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2


  Scenario: Pass
    When pass