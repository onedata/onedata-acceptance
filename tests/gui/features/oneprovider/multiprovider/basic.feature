Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: admin
          group3:
            owner: admin

    # unused_space is used only to introduce "oneprovider-1" for use of user1
    # thanks to this "oneprovider-1" is listed in consumer caveats popup
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
          space2:
            owner: admin
          space3:
            owner: admin
          unused_space:
            owner: user1
            providers:
            - oneprovider-1:
                storage: posix
                size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, Onezone] service


  Scenario: User supports space by two providers and sees that there are two provider in file browser
    Given there are no spaces supported by oneprovider-1 in Onepanel
    When user of browser1 sends support token for "space1" to user of browser2
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-2" in clusters menu
    And user of browser2 supports "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of browser1 sends support token for "space1" to user of browser2
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 clicks on Choose other Oneprovider on file browser page
    Then user of browser1 sees provider named "oneprovider-1" on file browser page
    And user of browser1 sees provider named "oneprovider-2" on file browser page
    And user of browser1 clicks on "oneprovider-2" provider on file browser page


  Scenario: Provider fails to support space using invite token with consumer caveat set not for them
    When user of browser1 creates and checks token with following configuration:
          type: invite
          invite type: Support space
          invite target: space1
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-2" in clusters menu
    Then user of browser2 fails to support "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB


  Scenario: User sees right Invite tokens after filtering them
    Given user admin has no harvesters
    And using REST, user admin creates "harvester1", "harvester2" harvester in "onezone" Onezone service

    # on bamboo, after test fails once, other tokens remain. They need to be deleted
    When user of browser2 removes all tokens

    And user of browser2 creates token with following configuration:
          name: space_token_2
          type: invite
          invite type: Invite user to space
          invite target: space2
    And user of browser2 creates token with following configuration:
          name: space_token_3
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
          name: group_token_3
          type: invite
          invite type: Invite user to group
          invite target: group3
    And user of browser2 creates token with following configuration:
          name: group_token_2
          type: invite
          invite type: Invite user to group
          invite target: group2

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
    And user of browser2 sees that there is token named "space_token_3" on tokens list
    And user of browser2 sees that there is token named "space_token_2" on tokens list
    And user of browser2 chooses "space2" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "space_token_2" on tokens list

    And user of browser2 chooses "User" Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "register_token_1" on tokens list

    And user of browser2 chooses "Group" Invite filter in tokens sidebar
    And user of browser2 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "group_token_3" on tokens list
    And user of browser2 sees that there is token named "group_token_2" on tokens list
    And user of browser2 chooses "group3" name Invite filter in tokens sidebar
    And user of browser2 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser2 sees that there is token named "group_token_3" on tokens list

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
