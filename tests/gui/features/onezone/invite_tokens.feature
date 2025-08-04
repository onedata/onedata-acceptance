Feature: Management of invite tokens in Onezone GUI, with admin user

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1

    And admin user does not have access to any space
    And admin user does not have access to any group
    And user admin has no harvesters

    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
          space2:
            owner: admin
          space3:
            owner: admin

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: admin
          group3:
            owner: admin

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, Onezone] service


  Scenario: User successfully consumes harvester to space invite token until usage limit is not expired
    Given using REST, user admin creates ["harvester1", "harvester2", "harvester3"] harvesters in "onezone" Onezone service

    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite harvester to space
          invite target: space1
          usage limit: 2
    And user of browser1 sees that token usage count is "0/2"
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    Then user of browser2 succeeds to consume token for "harvester1" harvester

    And user of browser1 refreshes site
    And user of browser1 sees that token usage count is "1/2"

    And user of browser2 sees that "space1" has appeared on the spaces list of "harvester1" harvester
    Then user of browser2 succeeds to consume token for "harvester2" harvester

    And user of browser1 refreshes site
    And user of browser1 sees that token usage count is "2/2"

    And user of browser2 sees that "space1" has appeared on the spaces list of "harvester2" harvester
    Then user of browser2 fails to consume token for "harvester3" harvester
    And user of browser2 removes all tokens


  Scenario: User successfully cleans up obsolete tokens
    Given using REST, user admin creates "harvester1" harvester in "onezone" Onezone service
    When user of browser2 removes all tokens
    And user of browser2 creates and checks token with following configuration:
          type: invite
          name: ToSurvive
          invite type: Invite user to space
          invite target: space2
          usage limit: 1
    And user of browser2 creates and checks token with following configuration:
          name: ToRemove
          type: invite
          invite type: Invite group to harvester
          invite target: harvester1
          usage limit: 1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    And user of browser1 succeeds to consume token for "group1" group

    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 clicks on "Clean up obsolete tokens" button in tokens sidebar
    And user of browser2 sees that "Clean up obsolete tokens" modal has appeared
    And user of browser2 clicks on "Remove" button in modal "Clean up obsolete tokens"
    Then user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "ToSurvive" on tokens list
    And user of browser2 removes all tokens


  Scenario: User fails to consume revoked token
    Given using REST, user admin creates "harvester1" harvester in "onezone" Onezone service
    When user of browser2 creates token with following configuration:
          name: token1
          type: invite
          invite type: Invite group to harvester
          invite target: harvester1
    And user of browser2 revokes token named "token1"
    And user of browser2 sees that created token configuration is as following:
          name: token1
          invite type: Invite group to harvester
          invite target: harvester1
          revoked: True
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    Then user of browser1 sees alert with text: "Provided token has been revoked." on tokens page while trying to consume token

    And user of browser2 removes all tokens


  Scenario: User fails to consume deleted token
    Given using REST, user admin creates "harvester1" harvester in "onezone" Onezone service
    When user of browser2 creates and checks token with following configuration:
          name: token2
          type: invite
          invite type: Invite group to harvester
          invite target: harvester1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser2 removes token named "token2"

    Then user of browser1 sees alert with text: "This resource could not be loaded" on tokens page while trying to consume token

    And user of browser2 removes all tokens


  Scenario: User sees right Invite tokens after filtering them
    Given using REST, user admin creates ["harvester1", "harvester2"] harvester in "onezone" Onezone service
    Then user of browser2 removes all tokens
    And user of browser2 creates token with following configuration:
          name: space_token_1
          type: invite
          invite type: Invite user to space
          invite target: space2
    And user of browser2 creates token with following configuration:
          name: space_token_2
          type: invite
          invite type: Invite user to space
          invite target: space3
    And user of browser2 creates token with following configuration:
          name: harvester_token_1
          type: invite
          invite type: Invite user to harvester
          invite target: harvester1
    And user of browser2 creates token with following configuration:
          name: harvester_token_2
          type: invite
          invite type: Invite user to harvester
          invite target: harvester2
    And user of browser2 creates token with following configuration:
          name: group_token_1
          type: invite
          invite type: Invite user to group
          invite target: group2
    And user of browser2 creates token with following configuration:
          name: group_token_2
          type: invite
          invite type: Invite user to group
          invite target: group3
    And user of browser2 creates token with following configuration:
          name: cluster_token_1
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-1
    And user of browser2 creates token with following configuration:
          name: cluster_token_2
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-2
    And user of browser2 creates token with following configuration:
          name: register_token_1
          type: invite
          invite type: Register Oneprovider

    And user of browser2 chooses "Invite" filter in tokens sidebar
    Then user of browser2 sees exactly 9 item(s) on tokens list in tokens sidebar

    And user of browser2 chooses "Space" Invite filter in tokens sidebar
    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "space_token_1" on tokens list
    And user of browser2 sees that there is token named "space_token_2" on tokens list
    And user of browser2 chooses "space2" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "space_token_1" on tokens list

    And user of browser2 chooses "User" Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "register_token_1" on tokens list

    And user of browser2 chooses "Group" Invite filter in tokens sidebar
    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "group_token_1" on tokens list
    And user of browser2 sees that there is token named "group_token_2" on tokens list
    And user of browser2 chooses "group3" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "group_token_2" on tokens list

    And user of browser2 chooses "Harvester" Invite filter in tokens sidebar
    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "harvester_token_1" on tokens list
    And user of browser2 sees that there is token named "harvester_token_2" on tokens list
    And user of browser2 chooses "harvester1" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "harvester_token_1" on tokens list

    And user of browser2 chooses "Cluster" Invite filter in tokens sidebar
    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "cluster_token_1" on tokens list
    And user of browser2 sees that there is token named "cluster_token_2" on tokens list
    And user of browser2 chooses "oneprovider-1" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "cluster_token_1" on tokens list

    And user of browser2 removes all tokens


  Scenario: User can see removed space ID in invitation token
    When user of browser1 creates token with following configuration:
          name: space_token_1
          type: invite
          invite type: Invite group to space
          invite target: space1
    And user of browser1 removes "space1" space in Onezone page
    And user of browser1 clicks on Tokens in the main menu
    And user of browser1 sees that there is token named "space_token_1" on tokens list
    And user of browser1 clicks on "space_token_1" on token list
    And user of browser1 refreshes site
    Then user of browser1 sees that created token configuration is as following:
          name: space_token_1
          invite type: Invite group to space
          invite target: $(resolve_id space1)
