Feature: Files remove metadata tests

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | web GUI    | oneclient1 |
  | oneclient1 | web GUI    |


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
            - file1


  # TODO: VFS-9477 reimplement mixed metadata tests after metadata move to file info modal
  # Scenario: User removes metadata
  #   When using <client1>, user1 sets new <fmt> metadata: <metadata> for "file1" file in space "space1" in oneprovider-1
  #   And using <client1>, user1 sees that <fmt> metadata for "file1" file is <metadata> in space "space1" in oneprovider-1
  #   And using <client2>, user1 removes all "file1" file metadata in space "space1" in oneprovider-1
  #   And if <client1> is web GUI, user1 refreshes site
  #   Then using <client1>, user1 sees that <fmt> metadata for "file1" file in space "space1" does not contain <metadata> in oneprovider-1

  #   Examples:
  #   | fmt   | metadata  |
  #   | basic | attr=val  |
  #   | JSON  | {"id": 1} |
  #   | RDF   | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>|
