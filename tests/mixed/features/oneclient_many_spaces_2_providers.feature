Feature: Tests for oneclient interaction with spaces with the same name on 2 providers


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
                - oneprovider-2:
                    storage: posix
                    size: 1000000
    And opened browsers with [onepanel, user1] signed in to [emergency interface of Onepanel, onezone] service
    And oneclients [client1, client2, client3]
      mounted on client_hosts [oneclient-1, oneclient-1, oneclient-2] respectively,
      using [token, token, token] by [user1, user1, user1]


  Scenario: Using different oneclients user can see proper space contents and space names (of spaces with the same name) in mount point after removing one
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space named "helloworld" with alias "A" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "A" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "A" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    When using REST, user1 creates space named "helloworld" with alias "B" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "B" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "B" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient2, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point
    And using oneclient3, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    And using oneclient1, user1 creates file named "file1" in space with alias "A" in oneprovider-1
    And using oneclient1, user1 writes "TEST AAA" to file named "file1" in space with alias "A" in oneprovider-1

    And using oneclient2, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1
    And using oneclient3, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1

    And using REST, user1 removes space with alias "B" in "onezone" Onezone service
    And using oneclient2, user1 sees spaces "[helloworld]" in mount point
    And using oneclient3, user1 sees spaces "[helloworld]" in mount point


  Scenario: Using different oneclients user can see proper space contents and space names (of spaces with the same name) in mount point after renaming one
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space named "helloworld" with alias "A" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "A" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "A" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    When using REST, user1 creates space named "helloworld" with alias "B" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "B" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "B" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using oneclient2, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point
    And using oneclient3, user1 sees spaces "[helloworld, helloworld]" from "onezone" Onezone service, annotated with their ids in mount point

    And using oneclient1, user1 creates file named "file1" in space with alias "A" in oneprovider-1
    And using oneclient1, user1 writes "TEST AAA" to file named "file1" in space with alias "A" in oneprovider-1

    And using oneclient2, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1
    And using oneclient3, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1

    And using REST, user1 renames space with alias "B" to "helloworld2" in "onezone" Onezone service
    And using oneclient2, user1 sees spaces "[helloworld, helloworld2]" in mount point
    And using oneclient3, user1 sees spaces "[helloworld, helloworld2]" in mount point


  Scenario Outline: Using different oneclients user can see proper space contents (of spaces with the same name) after modifying contents by different onecliets
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When using REST, user1 creates space named "helloworld" with alias "A" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "A" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "A" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    When using REST, user1 creates space named "helloworld" with alias "B" in "onezone" Onezone service
    And using REST, user1 generates space support token for space with alias "B" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports space with alias "B" in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000

    Then using <client1>, user1 creates file named "file1" in space with alias "A" in oneprovider-1
    And using <client2>, user1 writes "TEST AAA" to file named "file1" in space with alias "A" in oneprovider-1
    And using <client2>, user1 creates file named "file2" in space with alias "A" in oneprovider-1
    And using <client1>, user1 writes "TEST BBB" to file named "file2" in space with alias "A" in oneprovider-1

    And using <client1>, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1
    And using <client3>, user1 reads "TEST AAA" from file named "file1" in space with alias "A" in oneprovider-1
    And using <client3>, user1 reads "TEST BBB" from file named "file2" in space with alias "A" in oneprovider-1
    And using <client1>, user1 reads "TEST BBB" from file named "file2" in space with alias "A" in oneprovider-1

  Examples:
    | client1    | client2    | client3    |
    # oneclients on the same provider modify space content
    | oneclient1 | oneclient2 | oneclient3 |
    # oneclients on different providers modify space content
    | oneclient3 | oneclient1 | oneclient2 |
