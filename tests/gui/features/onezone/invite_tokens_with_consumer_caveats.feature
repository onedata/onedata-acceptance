Feature: Management of invite tokens with consumer caveats in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
          - user2
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: admin
          space2:
            owner: user1

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User fails to consume group to space invite token with consumer caveat set not for them
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: user
                by: id
                consumer name: user2
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 clicks on "Consume token" button in tokens sidebar
    And user of browser2 pastes received token into token text field
    And user of browser2 chooses "group1" group from dropdown on tokens page
    And user of browser2 clicks on Join button on consume token page
    Then user of browser2 sees that error modal with text "Consuming token failed" appeared

    And user of browser1 removes all tokens


  Scenario: User successfully consumes group to space invite token with consumer caveat set for them
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                Remove space: False
                View privileges: True
            Transfer management:
              granted: False
          caveats:
            consumer:
              - type: user
                by: id
                consumer name: user1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 clicks on "Consume token" button in tokens sidebar
    And user of browser2 pastes received token into token text field
    And user of browser2 chooses "group1" group from dropdown on tokens page
    And user of browser2 clicks on Join button on consume token page
    Then user of browser2 sees an success notify with text matching to: .*joined.*
    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser2 sees that space space1 has following privilege configuration for group group1:
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                Remove space: False
                View privileges: True
            User management:
              granted: False

    And user of browser1 removes all tokens


   Scenario: User successfully consumes group to space invite token with consumer caveat set for Any user
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          caveats:
            consumer:
              - type: user
                by: name
                consumer name: Any user
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 succeeds to consume token for "group1" group

    And user of browser1 removes all tokens


  Scenario: Group succeeds to join space using invite token with consumer caveat set for it
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                View privileges: True
            Group management:
              granted: True
          caveats:
            consumer:
              - type: group
                by: id
                consumer name: group1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    Then user of browser2 succeeds to consume token for "group1" group
    And user of browser2 sees that space space1 has following privilege configuration for group group1:
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                View privileges: True
            Group management:
              granted: True

    And user of browser1 removes all tokens


  Scenario: Group fails to join space using invite token with consumer caveat set not for it
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: group
                by: id
                consumer name: group2
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 fails to consume token for "group1" group

    And user of browser1 removes all tokens


  Scenario: Group succeeds to join space invite token with consumer caveat set for Any group
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          caveats:
            consumer:
              - type: group
                by: name
                consumer name: Any group
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 succeeds to consume token for "group1" group

    And user of browser1 removes all tokens


  Scenario: Provider succeeds to support space with invite token with consumer caveat set for them
    # unused_space is used only to introduce "oneprovider-1" for use of user1
    # thanks to this "oneprovider-1" is listed in consumer caveats popup
    Given additional spaces configuration in "onezone" Onezone service:
          unused_space:
            owner: user1
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
    When user of browser2 creates and checks token with following configuration:
          type: invite
          invite type: Support space
          invite target: space2
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 opens "oneprovider-1" clusters submenu
    Then user of browser1 succeeds to support "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB


  Scenario: Provider succeeds to support space using invite token with consumer caveat set for Any Oneprovider
    # unused_space is used only to introduce "oneprovider-1" for use of user1
    # thanks to this "oneprovider-1" is listed in consumer caveats popup
    Given additional spaces configuration in "onezone" Onezone service:
            unused_space:
              owner: user1
              providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    When user of browser2 creates and checks token with following configuration:
          type: invite
          invite type: Support space
          invite target: space2
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: Any Oneprovider
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 opens "oneprovider-1" clusters submenu
    Then user of browser1 succeeds to support "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB


  Scenario: Provider fails to support space using invite token with consumer caveat set not for them
    # unused_space is used only to introduce "oneprovider-1" for use of user1
    # thanks to this "oneprovider-1" is listed in consumer caveats popup
    Given additional spaces configuration in "onezone" Onezone service:
            unused_space:
              owner: user1
              providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    When user of browser2 creates and checks token with following configuration:
          type: invite
          invite type: Support space
          invite target: space2
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-2" in clusters menu
    Then user of browser1 fails to support "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB






