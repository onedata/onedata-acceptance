Feature: Directories movement tests


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
    And oneclient mounted using token by user1
    And opened browser with user1 signed in to "onezone" service


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

    Examples:
    | client1    | client2    |
    | web GUI    | oneclient1 |
    | REST       | oneclient1 |
    | web GUI    | REST       |
    | oneclient1 | REST       |


  Scenario Outline: User moves non-empty directory using <client2> and using <client1> sees that its content has not changed
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - dir1:
                - dir2:
                    - dir3
            - dir4:
                - dir5
    And using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created
    And using <client2>, user1 succeeds to move "space1/dir4" to "space1/dir1/dir2/dir3/dir4" in oneprovider-1
    And if <client1> is web GUI, user1 is idle for 10 seconds
    Then using <client1>, user1 sees that directory structure in "space1" space in oneprovider-1 is as follow:
            - dir1:
                - dir2:
                    - dir3:
                        - dir4:
                            - dir5

    Examples:
    | client1    | client2    |
    | web GUI    | oneclient1 |
    | REST       | oneclient1 |
    | web GUI    | REST       |
    | oneclient1 | REST       |


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

    Examples:
    | client1    | client2    |
    | web GUI    | oneclient1 |
    | REST       | oneclient1 |
    | web GUI    | REST       |
    | oneclient1 | REST       |


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

   Examples:
    | client1    | client2    |
    | web GUI    | oneclient1 |
    | REST       | oneclient1 |
    | web GUI    | REST       |
    | oneclient1 | REST       |


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

    Examples:
    | client1    | client2    |
    | web GUI    | oneclient1 |
    | REST       | oneclient1 |
    | web GUI    | REST       |
    | oneclient1 | REST       |
