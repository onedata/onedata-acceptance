Feature: Datasets mixed tests

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
          storage:
            defaults:
              provider: oneprovider-1
            directory tree:
              - dir1
              - dir2:
                  - dir3:
                    - dir4:
                      - dir5
                    - file1: 150

    And opened browser with user1 signed in to "onezone" service


  Scenario Outline: Using <client1>, user creates dataset for item then using <client2> user sees that dataset was created
    When using <client1>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client2>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user removes dataset for item then using <client2> user does not see dataset
    When using <client1>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client2>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client2>, user1 removes dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client1>, user1 does not see dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user creates dataset with data and metadata write protection flags then using <client2> user sees data and metadata write protection flags
    When using <client1>, user1 creates dataset with data and metadata write protection flags for item "dir1" in space "space1" in oneprovider-1
    And using <client2>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client2>, user1 sees data and metadata write protection flags for dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user marks directories as dataset then using <client2> user sees dataset directory tree
    When using <client1>, user1 creates dataset for item "dir2" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset for item "dir2/dir3/dir4" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset for item "dir2/dir3/file1" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset for item "dir2/dir3/dir4/dir5" in space "space1" in oneprovider-1
    Then using <client2>, user1 sees that datasets structure in space "space1" in oneprovider-1 is as follow:
         - dir2:
           - dir4:
             - dir5
           - file1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user marks directories as dataset with data and metadata write protection flags then using <client2> user sees that file has effective protection flags from its parents
    When using <client1>, user1 creates dataset with metadata write protection flags for item "dir2" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset with data write protection flags for item "dir2/dir3" in space "space1" in oneprovider-1
    Then using <client2>, user1 sees that item "dir2/dir3/dir4/dir5" has effective data and metadata write protection flags in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user creates datasets, and using <client2> user sets data and metadata write protection flags then using <client1> user sees that datasets has protection flags
    When using <client1>, user1 creates dataset for item "dir2" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset for item "dir2/dir3" in space "space1" in oneprovider-1
    And using <client1>, user1 creates dataset for item "dir2/dir3/file1" in space "space1" in oneprovider-1
    And using <client2>, user1 sets data protection flag for dataset "dir2" in space "space1" in oneprovider-1
    And using <client2>, user1 sets metadata protection flags for dataset "dir2/dir3" in space "space1" in oneprovider-1
    Then using <client1>, user1 sees that dataset "dir2/dir3/file1" has effective data and metadata write protection flags in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: Using <client1>, user creates dataset, and using <client2> user detaches dataset than using <client1> user sees that dataset was detached
    When using <client1>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client2>, user1 detaches dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client1>, user1 sees that dataset for item "dir1" is detached in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


   Scenario Outline: Using <client1>, user detaches dataset than using <client1> user reattaches dataset
    When using <client2>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client1>, user1 detaches dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client2>, user1 reattaches dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client1>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1
  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |

