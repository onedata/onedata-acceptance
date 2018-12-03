Feature: Files multiclient tests

  Examples:
  | client1   | client2   | host1         | host2         |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1 |
  | web GUI	  | REST	  | oneprovider-1 | oneprovider-1 |
  | oneclient | REST      | client1       | oneprovider-1 |
  | REST      | oneclient | oneprovider-1 | client2       |
  | oneclient | web GUI   | client1       | oneprovider-1 |
  | web GUI   | oneclient | oneprovider-1 | client2       |


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            users:
              - user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And [user1, user2] mount oneclients [client1, client2] in
      [/home/user1/onedata, /home/user2/onedata] on client_hosts
      [oneclient-1, oneclient-2] respectively,
      using [token, token]
    And opened browser with [user1, user2] logged to [onezone, onezone] service
    And opened [oneprovider-1, oneprovider-1] Oneprovider view in web GUI by [user1, user2]

    
  Scenario Outline: User1 creates file using <client1> and user2 removes it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user2 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user2 removes file named "file1" in "space1" in <host2>
    Then using <client2>, user2 fails to see item named "file1" in "space1" in <host2>
    And using <client1>, user1 fails to see item named "file1" in "space1" in <host1>


  Scenario Outline: User1 creates file using <client1> and user2 renames it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in <host1>
    And using <client2>, user2 succeeds to see item named "file1" in "space1" in <host2>
    And using <client2>, user2 renames item named "file1" to "file2" in "space1" in <host2>
    Then using <client2>, user2 fails to see item named "file1" in "space1" in <host2>
    And using <client1>, user1 fails to see item named "file1" in "space1" in <host1>
    And using <client2>, user2 succeeds to see item named "file2" in "space1" in <host2>
    And using <client1>, user1 succeeds to see item named "file2" in "space1" in <host1>
