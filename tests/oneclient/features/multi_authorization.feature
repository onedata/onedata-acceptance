Feature: Multi_authorization

  Scenario: Successful authorization - 1 client per user
    Given [user1, user2] mount oneclients [client11, client22] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [token, token]
    Then last operation by user1 succeeds
    And last operation by user2 succeeds
    And [space1] are mounted for user1 on [client11]
    And [space2] are mounted for user2 on [client22]


  Scenario: Successful authorization - 2 clients of one user
    Given [user1, user1] mount oneclients [client11, client12] in
      [/home/user1/onedata, /home/user1/onedata2] on client_hosts
      [oneclient-1, oneclient-1] respectively,
      using [token, token]
    Then last operation by user1 succeeds
    And [space1, space2] are mounted for user1 on [client11, client12]


  Scenario: Successful authorization - 2 clients of one user on different hosts
    Given [user1, user1] mount oneclients [client11, client21] in
      [/home/user1/onedata, /home/user1/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [token, token]
    Then last operation by user1 succeeds
    And [space1, space2] are mounted for user1 on [client11, client21]


  Scenario: Bad and good authorization
    Given [user1, user2] mount oneclients [client11, client22] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [bad token, token]
    Then last operation by user1 fails
    And last operation by user2 succeeds
    And [space1, space2] are mounted for user2 on [client22]


   Scenario: Bad authorization
    Given [user1, user2] mount oneclients [client11, client22] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [bad token, bad token]
    Then last operation by user1 fails
    And last operation by user2 fails