Feature: ACL files pz

  Scenario Outline: Write metadata to file
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to write "file1" file basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                                         |
    | succeeds |  [metadata:read metadata, metadata:write metadata]  |
    | fails    |  all except [metadata:write metadata]               |
    | succeeds |  all except [metadata:read metadata]                 |


  Scenario Outline: Read files metadata
    When user of browser1 succeeds to write "file1" file basic metadata: "attr=val" in "space1"
    And user of browser1 sets selected items ACL <privileges> privileges for <subject_type> <subject_name>
    Then user of browser2 <result> to read "file1" file basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                           |
    | succeeds |  [metadata:read metadata]             |
    | fails    |  all except [metadata:read metadata]  |
