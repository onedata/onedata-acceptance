Feature: Tests for oneclient interaction with spaces with the same name


  Background:
    Given initial users configuration in "onezone" Onezone service:
        - user1
        - user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
        space2:
            owner: user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browsers with [onepanel, user1] signed in to [emergency interface of Onepanel, onezone] service
    And oneclient mounted using token by user1
    And oneclient mounted using token by user2


  Scenario: Using oneclient user can see 2 spaces with the same name annotated with their ids in mount point, then after removing one space user can see the other without id
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using oneclient1, user1 sees spaces "[helloworld]" in mount point

    And using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using oneclient1, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    # this step removes one of the spaces with that name
    And using REST, user1 removes space named "helloworld" in "onezone" Onezone service
    # Due to VFS-10923, space id is still visible
    And using oneclient1, user1 sees spaces "[helloworld]" from "onezone" Onezone service, annotated with their ids in mount point


  Scenario: Using oneclient user can see 2 spaces with the same name annotated with their ids in mount point, then after renaming one space user can see them without id
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user1 creates space "helloworld2" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld2" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld2" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient1, user1 sees spaces "[helloworld, helloworld2]" in mount point

    And using REST, user1 renames space named "helloworld2" to "helloworld" in "onezone" Onezone service
    And using oneclient1, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    # this step renames one of the spaces with that name
    And using REST, user1 renames space named "helloworld" to "helloworld2" in "onezone" Onezone service
    And using oneclient1, user1 sees spaces "[helloworld, helloworld2]" in mount point


  Scenario: Using oneclient user can properly write and read from spaces with the same name
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space named "helloworld" with test alias "A" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with test alias "A" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with test alias "A" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user1 creates space named "helloworld" with test alias "B" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with test alias "B" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with test alias "B" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user1 creates space named "helloworld" with test alias "C" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with test alias "C" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with test alias "C" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    And using oneclient1, user1 creates file named "file1" in space with test alias "A" in oneprovider-1
    And using oneclient1, user1 writes "TEST AAA" to file named "file1" in space with test alias "A" in oneprovider-1

    And using oneclient1, user1 creates file named "file1" in space with test alias "B" in oneprovider-1
    And using oneclient1, user1 writes "TEST BBB" to file named "file1" in space with test alias "B" in oneprovider-1

    And using oneclient1, user1 creates file named "file1" in space with test alias "C" in oneprovider-1
    And using oneclient1, user1 writes "TEST CCC" to file named "file1" in space with test alias "C" in oneprovider-1

    Then using oneclient1, user1 reads "TEST AAA" from file named "file1" in space with test alias "A" in oneprovider-1
    And using oneclient1, user1 reads "TEST BBB" from file named "file1" in space with test alias "B" in oneprovider-1
    And using oneclient1, user1 reads "TEST CCC" from file named "file1" in space with test alias "C" in oneprovider-1

    And using REST, user1 removes space with test alias "B" in "onezone" Onezone service
    And using REST, user1 renames space with test alias "C" to "helloworld2" in "onezone" Onezone service

    And using oneclient1, user1 sees spaces "[helloworld, helloworld2]" in mount point

    And using oneclient1, user1 creates file named "file2" in space with test alias "A" in oneprovider-1
    And using oneclient1, user1 writes "TEST DDD" to file named "file2" in space with test alias "A" in oneprovider-1
    And using oneclient1, user1 reads "TEST DDD" from file named "file2" in space with test alias "A" in oneprovider-1


  Scenario: Using oneclient user can see a space he joined into in mount point
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user2 creates space "space_helloworld2" in "onezone" Onezone service
    And using REST, user2 generates space support token for space named "space_helloworld2" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space_helloworld2" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient1, user1 sees spaces "[helloworld]" in mount point, waiting up to 60s

    And using REST, user2 creates token with following configuration:
          name: invite token
          type: invite
          invite type: Invite user to space
          invite target: space_helloworld2
          usage limit: 1
    And user2 sends token to user1
    And using REST, user1 successfully joins space space_helloworld2 with received token

    And using oneclient1, user1 sees spaces "[helloworld, space_helloworld2]" in mount point, waiting up to 60s
    And using REST, user1 leaves space named "space_helloworld2" in "onezone" Onezone service
    And using oneclient1, user1 sees spaces "[helloworld]" in mount point, waiting up to 60s


  Scenario: Using oneclient user can see a space (with the same name he already has) he joined into in mount point
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "space_helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "space_helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space_helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user2 creates space "space_helloworld" in "onezone" Onezone service
    And using REST, user2 generates space support token for space named "space_helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space_helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient1, user1 sees spaces "[space_helloworld]" in mount point, waiting up to 60s

    And using REST, user2 creates token with following configuration:
          name: invite token
          type: invite
          invite type: Invite user to space
          invite target: space_helloworld
          usage limit: 1
    And user2 sends token to user1
    And using REST, user1 successfully joins space space_helloworld with received token

    And using oneclient1, user1 sees spaces "[space_helloworld, space_helloworld]" from "onezone" Onezone service, annotated with their ids in mount point, waiting up to 60s
    And using REST, user1 leaves space named "space_helloworld" in "onezone" Onezone service
    # Due to VFS-10923, space id is still visible
    And using oneclient1, user1 sees spaces "[space_helloworld]" from "onezone" Onezone service, annotated with their ids in mount point, waiting up to 60s


  Scenario: Using oneclient user can see 2 spaces with the same name annotated with their ids in mount point, then after removing one space (when provider is offline) can see the other without id
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using oneclient1, user1 sees spaces "[helloworld]" in mount point

    And using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using oneclient1, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    And user1 stops network on oneprovider oneprovider-krakow
    # this step removes one of the spaces with that name
    And using REST, user1 removes space named "helloworld" in "onezone" Onezone service
    And user1 starts network on oneprovider oneprovider-krakow
    # Due to VFS-10923, space id is still visible
    And using oneclient1, user1 sees spaces "[helloworld]" from "onezone" Onezone service, annotated with their ids in mount point, waiting up to 60s


  Scenario: Using oneclient user can see 2 spaces with the same name annotated with their ids in mount point, then after renaming one space (when provider is offline) can see them without id
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user1 creates space "helloworld2" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld2" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld2" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient1, user1 sees spaces "[helloworld, helloworld2]" in mount point

    And using REST, user1 renames space named "helloworld2" to "helloworld" in "onezone" Onezone service
    And using oneclient1, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    And user1 stops network on oneprovider oneprovider-krakow
    # this step renames one of the spaces with that name
    And using REST, user1 renames space named "helloworld" to "helloworld2" in "onezone" Onezone service
    And user1 starts network on oneprovider oneprovider-krakow
    And using oneclient1, user1 sees spaces "[helloworld, helloworld2]" in mount point, waiting up to 90s


  Scenario: Using oneclient different users can properly write and read from spaces with the same name
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space "space_helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "space_helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space_helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user2 creates space "space_helloworld" in "onezone" Onezone service
    And using REST, user2 generates space support token for space named "space_helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space_helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient1, user1 sees spaces "[space_helloworld]" in mount point
    And using oneclient1, user2 sees spaces "[space_helloworld]" in mount point

    And using oneclient1, user1 succeeds to create file named "file1" in "space_helloworld" in oneprovider-1
    And using oneclient1, user1 writes "TEST AAA" to file named "file1" in "space_helloworld" in oneprovider-1
    And using oneclient1, user1 reads "TEST AAA" from file named "file1" in "space_helloworld" in oneprovider-1

    And using oneclient1, user2 succeeds to create file named "file1" in "space_helloworld" in oneprovider-1
    And using oneclient1, user2 writes "TEST BBB" to file named "file1" in "space_helloworld" in oneprovider-1
    And using oneclient1, user2 reads "TEST BBB" from file named "file1" in "space_helloworld" in oneprovider-1


