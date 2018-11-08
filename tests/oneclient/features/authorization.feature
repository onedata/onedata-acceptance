Feature: Authorization

  Scenario: Successful authorization
    Given user1 mounts oneclient in /home/user1/onedata using token
    Then last operation by user1 succeeds
    And [space1, space2] are mounted for user1

    
  Scenario: Bad authorization
    Given user1 mounts oneclient in /home/user1/onedata using bad token
    Then last operation by user1 fails
