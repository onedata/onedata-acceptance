Feature: Files metadata tests
  
  Examples:
  | client1   | client2   | host1         | host2            |
  | web GUI   | REST      | oneprovider-1 | oneprovider-1    |
  | REST      | web GUI   | oneprovider-1 | oneprovider-1    |
  | REST      | oneclient | oneprovider-1 | client1          |
  | oneclient | REST      | client1       | oneprovider-1    |
  | web GUI   | oneclient | oneprovider-1 | client1          |
  | oneclient | web GUI   | client1       | oneprovider-1    |

  
  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user1 mounts oneclient in /home/user1/onedata using token
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
                    - file1
    And opened browser with user1 logged to "onezone onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1


  Scenario: User sets metadata
    When using <client1>, user1 sets new <fmt> metadata: <metadata> for "file1" in space "space1" in <host1>
    Then using <client2>, user1 sees that <fmt> metadata for "file1" is <metadata> in space "space1" in <host2>

    Examples:
    | fmt   | metadata  |
    | basic | attr=val  |
    | JSON  | {"id": 1} |
    | RDF   | <rdf:XML xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"></rdf:XML>|


  Scenario: User removes metadata
    When using <client1>, user1 sets new <fmt> metadata: <metadata> for "file1" in space "space1" in <host1>
    And using <client1>, user1 sees that <fmt> metadata for "file1" is <metadata> in space "space1" in <host1>
    And using <client2>, user1 removes all "file1" metadata in space "space1" in <host2>
    Then using <client1>, user1 sees that <fmt> metadata for "file1" in space "space1" does not contain <metadata> in <host1>

    Examples:
    | fmt   | metadata  |
    | basic | attr=val  |
    | JSON  | {"id": 1} |
    | RDF   | <rdf:XML xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"></rdf:XML>|
