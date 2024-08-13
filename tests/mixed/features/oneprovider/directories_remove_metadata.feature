Feature: Directory remove metadata tests


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
    And directory structure created by user1 in "space1" space on oneprovider-1 as follows:
            - dir1


  Scenario Outline: User removes metadata
    When using <client1>, user1 sets new <fmt> metadata: <metadata> for "dir1" directory in space "space1" in oneprovider-1
    And using <client1>, user1 sees that <fmt> metadata for "dir1" directory is <metadata> in space "space1" in oneprovider-1
    And using <client2>, user1 removes all "dir1" directory metadata in space "space1" in oneprovider-1
    Then using <client1>, user1 sees that <fmt> metadata for "dir1" directory in space "space1" does not contain <metadata> in oneprovider-1

    Examples:
    | fmt   | metadata  | client1    | client2    |
    | basic | attr=val  | REST       | web GUI    |
    | JSON  | {"id": 1} | REST       | web GUI    |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | REST       | web GUI    |
    | basic | attr=val  | web GUI    | REST       |
    | JSON  | {"id": 1} | web GUI    | REST       |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | web GUI    | REST       |
    | basic | attr=val  | oneclient1 | REST       |
    | JSON  | {"id": 1} | oneclient1 | REST       |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | oneclient1 | REST       |
    | basic | attr=val  | REST       | oneclient1 |
    | JSON  | {"id": 1} | REST       | oneclient1 |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | REST       | oneclient1 |
    | basic | attr=val  | web GUI    | oneclient1 |
    | JSON  | {"id": 1} | web GUI    | oneclient1 |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | web GUI    | oneclient1 |
    | basic | attr=val  | oneclient1 | web GUI    |
    | JSON  | {"id": 1} | oneclient1 | web GUI    |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | oneclient1 | web GUI    |

