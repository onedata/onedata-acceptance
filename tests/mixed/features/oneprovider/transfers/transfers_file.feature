Feature: Oneprovider transfers files functionality, using mixed interfaces GUI and REST

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
                - oneprovider-2:
                    storage: posix
                    size: 100000000
    And opened browser with user1 signed in to Onezone service
    And directory tree structure on local file system:
          user1:
            large_file.txt:
              size: 50 MiB


Scenario Outline: User of <client1> sets file replication to provider and using <client2> sees it finished successfully
  When using web GUI, user1 uploads file "large_file.txt" to oneprovider-1 Oneprovider file browser in space "space1"
  And using <client1>, user1 replicates file "large_file.txt" in space "space1" to provider oneprovider-2
  And using <client1>, user1 waits for last transfer to finish in space "space1" in provider oneprovider-1
  Then using <client2>, user1 sees details about last transfer of file in space "space1" in provider oneprovider-1:
      name: large_file.txt
      replicated: 50 MiB
      type: replication
      status: completed

  Examples:
  | client1 | client2 |
  | REST    | web GUI |
  | web GUI | REST    |


Scenario Outline: User of <client1> sets file migration and using <client2> sees it finished successfully
  When using web GUI, user1 uploads file "large_file.txt" to oneprovider-1 Oneprovider file browser in space "space1"
  And using <client1>, user1 migrates file "large_file.txt" in space "space1" to provider oneprovider-2 from oneprovider-1
  And using <client1>, user1 waits for last transfer to finish in space "space1" in provider oneprovider-1
  Then using <client2>, user1 sees details about last transfer of file in space "space1" in provider oneprovider-1:
      name: large_file.txt
      replicated: 50 MiB
      type: migration
      status: completed

  Examples:
  | client1 | client2 |
  | REST    | web GUI |
  | web GUI | REST    |


Scenario Outline: User of <client1> sets file eviction from provider and using <client2> sees it finished successfully
  When using web GUI, user1 uploads file "large_file.txt" to oneprovider-1 Oneprovider file browser in space "space1"
  # replicate file in order to make data redundant and possible to eviction
  And using <client1>, user1 replicates file "large_file.txt" in space "space1" to provider oneprovider-2
  And using <client1>, user1 waits for last transfer to finish in space "space1" in provider oneprovider-1
  And using <client1>, user1 evicts file "large_file.txt" in space "space1" from provider oneprovider-1
  And using <client1>, user1 waits for last transfer to finish in space "space1" in provider oneprovider-1
  Then using <client2>, user1 sees details about last transfer of file in space "space1" in provider oneprovider-1:
      name: large_file.txt
      replicated: 0 B
      type: eviction
      status: completed

  Examples:
  | client1 | client2 |
  | REST    | web GUI |
  | web GUI | REST    |
