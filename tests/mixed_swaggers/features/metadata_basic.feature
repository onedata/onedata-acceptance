Feature: Metadata basic tests using REST client and web GUI 
    
  Examples:
  | client1 | client2   | item  |
  | web GUI | REST      | file1 |
  | REST    | web GUI   | file1 |
  | web GUI | REST      | dir1  |
  | REST    | web GUI   | dir1  |

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
                    - file1
                    - dir1

    And opened browser with user1 logged to "onezone onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1

  Scenario: User sets metadata
    When using <client1>, user1 sets new <fmt> metadata: <metadata> for <item> in space "space1" in oneprovider-1 Oneprovider
    Then using <client2>, user1 sees that <fmt> metadata for <item> is <metadata> in space "space1" in oneprovider-1 Oneprovider

    Examples:
    | fmt   | metadata  |
    | basic | attr=val  |
    | JSON  | {"id": 1} |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>|

  Scenario: User removes metadata        
    When using <client1>, user1 sets new <fmt> metadata: <metadata> for <item> in space "space1" in oneprovider-1 Oneprovider
    And using <client1>, user1 sees that <fmt> metadata for <item> is <metadata> in space "space1" in oneprovider-1 Oneprovider
    And using <client2>, user1 removes all <item> metadata in space "space1" in oneprovider-1 Oneprovider
    Then using <client1>, user1 sees that <fmt> metadata for <item> in space "space1" does not contain <metadata> in oneprovider-1 Oneprovider
                
    Examples:
    | fmt   | metadata  |
    | basic | attr=val  |
    | JSON  | {"id": 1} |
    | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>|
