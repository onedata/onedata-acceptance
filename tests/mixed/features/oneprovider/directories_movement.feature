Feature: Directories movement tests

  Examples:
  | client1    | client2    |
  | web GUI    | oneclient1 |
  | REST       | oneclient1 |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And effective support for user in provider:
        oneprovider-1:
            - user1
    And oneclient mounted in /home/user1/onedata using token by user1
    And opened browser with user1 logged to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario Outline: User moves directory using <client2> and using <client1> sees that it has been moved
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - dir3
            - dir4
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 succeeds to move "space1/dir1/dir2/dir3" to "space1/dir4/dir3" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
            - dir1:
                - dir2
            - dir4:
                - dir3


  Scenario Outline: User moves non-empty directory using <client2> and using <client1> sees that its content has not changed
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - dir3
            - dir4:
                - dir5
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 succeeds to move "space1/dir4" to "space1/dir1/dir2/dir3/dir4" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
            - dir1:
                - dir2:
                    - dir3:
                        - dir4:
                            - dir5


  Scenario Outline: User fails to move directory to its subtree using <client2> and using <client1> sees that it has not been moved
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
        - dir1:
            - dir2:
                - dir3
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 fails to move "space1/dir1" to "space1/dir1/dir2/dir3/dir1" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
        - dir1:
            - dir2:
                - dir3


 Scenario Outline: User copies directory using <client2> and using <client1> sees that it has been copied
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - dir3
            - dir4
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 copies directory named "space1/dir4" to "space1/dir1/dir2/dir3/dir4" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
            - dir1:
                - dir2:
                    - dir3:
                        - dir4
            - dir4


  Scenario Outline: User copies non-empty directory using <client2> and using <client1> sees that it has not changed
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - dir3
            - dir4:
                - dir5
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 copies directory named "space1/dir4" to "space1/dir1/dir2/dir3/dir4" in oneprovider-1
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
        - dir1:
            - dir2:
                - dir3:
                    - dir4:
                        - dir5
        - dir4:
            - dir5
