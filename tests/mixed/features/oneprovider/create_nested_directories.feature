Feature: Tests for creating nested directories

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


  Scenario Outline: User create directory structure using <client1> and using <client2> sees that it has appeared
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - 20B-0.txt
            - dir1:
                - dir2:
                    - dir3
                    - dir4:
                        - 20B-0.txt
                        - 20B-1.txt
                        - dir5:
                            - dir6:
                                - dir7
                - dir8
                - 20B-0.txt
                - 20B-1.txt
                - dir9:
                    - 20B-0.txt
            - dir0
    Then using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |
  | web GUI    | oneclient1 |


  Scenario Outline: User create directory structure using <client1> and using <client2> sees that it has appeared v2
    When using <client1>, user1 creates directory structure in "space1" space on oneprovider-1 as follow:
            - 20B-0.txt
            - dir1:
                - dir2:
                    - dir3:
                        - 20B-0.txt
                    - 20B-0.txt
                - 20B-0.txt
            - dir0
    Then using <client2>, user1 sees that directory structure in "space1" space in oneprovider-1 is as previously created

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |
  | web GUI    | oneclient1 |
