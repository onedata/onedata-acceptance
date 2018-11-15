Feature: Extended_attributes

  Background:
    Given user1 mounts oneclient in /home/user1/onedata using token


  Scenario Outline: Check extended attribute exists
    When user1 creates regular files [space1/file1]
    Then user1 sees file1 in space1
    Then user1 sets on space1/file1 extended attribute <name> with value <value>
    And user1 checks that space1/file1 has extended attribute <name>
    Then user1 removes extended attribute <name> from space1/file1
    And user1 checks that space1/file1 does not have extended attribute <name>

    Examples:
    | name | value |
    | user.xattr1 | WHATEVER |


  Scenario Outline: Check string extended attribute has correct value
    When user1 creates regular files [space1/file1]
    Then user1 sees file1 in space1
    Then user1 sets on space1/file1 extended attribute <name> with value <value>
    And user1 checks that space1/file1 has string extended attribute <name> with value <value>
    
    Examples:
    | name | value |
    | user.withspaces | EXTENDED ATTRIBUTE VALUE |
    | user.unicode | महसुस |
    | user.notjson | {{{{{ "a": 1 }} |


  Scenario Outline: Check numeric extended attribute has correct value
    When user1 creates regular files [space1/file1]
    Then user1 sees file1 in space1
    Then user1 sets on space1/file1 extended attribute <name> with value <value>
    And user1 checks that space1/file1 has numeric extended attribute <name> with value <value>
    
    Examples:
    | name | value |
    | user.int | 987654 |
    | user.negative | -123.9 |
    | user.zero | -0.00 |
    | user.exp | 6.0865000001e-03 |


  Scenario Outline: Check JSON extended attribute has correct value
    When user1 creates regular files [space1/file1]
    Then user1 sees file1 in space1
    Then user1 sets on space1/file1 extended attribute <name> with value <value>
    And user1 checks that space1/file1 has JSON extended attribute <name> with value <value>
    
    Examples:
    | name | value |
    | user.emptyobject | {} |
    | user.simpleobject | {"abcd": 4} |
    | user.list | [1, 2, 3, {"a": [1, 2, 3]}] |
