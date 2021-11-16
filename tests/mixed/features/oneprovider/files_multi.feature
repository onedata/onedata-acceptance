Feature: Files multiclient tests

  Examples:
  | client1    | client2    | client3    |
  | REST       | web GUI    | REST       |
  | REST       | REST       | web GUI    |
  | oneclient1 | REST       | oneclient1 |
  | REST       | oneclient2 | REST       |
  | oneclient1 | web GUI    | oneclient1 |
  | oneclient1 | oneclient2 | web GUI    |


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
    And oneclients [client1, client2]
      mounted on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [user1, user2]
    And opened browser with [user1, user2] signed in to [onezone, onezone] service

    
  Scenario Outline: User1 creates file using <client1> and user2 removes it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to remove file named "file1" in "space1" in oneprovider-1
    Then using <client2>, user2 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client3>, user1 fails to see item named "file1" in "space1" in oneprovider-1


  Scenario Outline: User1 creates file using <client1> and user2 renames it using <client2>
    When using <client1>, user1 succeeds to create file named "file1" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user2 renames item named "file1" to "file2" in "space1" in oneprovider-1
    Then using <client2>, user2 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client1>, user1 fails to see item named "file1" in "space1" in oneprovider-1
    And using <client2>, user2 succeeds to see item named "file2" in "space1" in oneprovider-1
    And using <client3>, user1 succeeds to see item named "file2" in "space1" in oneprovider-1
