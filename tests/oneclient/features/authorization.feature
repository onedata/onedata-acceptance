Feature: Authorization

  Scenario: Successful authorization
    Given oneclient mounted using token by user1
    Then last operation by user1 succeeds
    And [space1, space2] are mounted for user1

    
  Scenario: Bad authorization
    Given oneclient mounted using bad token by user1
    Then last operation by user1 fails
