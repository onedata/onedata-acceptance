Feature: Clusters effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user2
            - user3
    And there is no groups in Onezone page used by admin before definition in next steps
    And initial groups configuration in "onezone" Onezone service:
          child_group1:
            owner: admin
          parent_group1:
            owner: admin
            users:
              - user2
              - user3
            groups:
                - child_group1
                - child_group2
          parent_group2:
              owner: admin
              users:
                - user3
              groups:
                - child_group1
                - child_group2
          child_group2:
              owner: admin

    And users opened [browser_admin, browser_user2] browsers' windows
    And users of [browser_admin, browser_user2] opened [Onezone, Onezone] page
    And user of [browser_admin, browser_user2] logged as [admin, user2] to [Onezone, Onezone] service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin adds "child_group1" group to "oneprovider-1" cluster
    And user of browser_admin adds "parent_group1" group to "oneprovider-1" cluster
    And user of browser_admin clicks "child_group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "child_group1" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "parent_group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group1" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks "child_group1" group in "oneprovider-1" cluster members groups list
    Then user of browser_admin sees following privileges of "child_group1" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin invites user of browser_user2 to "oneprovider-1" cluster
    And user of browser_user2 joins to cluster

    And user of browser_admin adds "parent_group1" group to "oneprovider-1" cluster
    And user of browser_admin clicks "parent_group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group1" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: False

    And user of browser_admin clicks "user2" user in "oneprovider-1" cluster members users list
    And user of browser_admin sets following privileges for "user2" user in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks "user2" user in "oneprovider-1" cluster members users list
    Then user of browser_admin sees following privileges of "user2" user in cluster members subpage:
          Cluster management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin adds "parent_group1" group to "oneprovider-1" cluster
    And user of browser_admin adds "parent_group2" group to "oneprovider-1" cluster
    And user of browser_admin clicks "parent_group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group1" group in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "parent_group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group2" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks "child_group2" group in "oneprovider-1" cluster members groups list
    Then user of browser_admin sees following privileges of "child_group2" group in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin adds "parent_group1" group to "oneprovider-1" cluster
    And user of browser_admin adds "parent_group2" group to "oneprovider-1" cluster
    And user of browser_admin clicks "parent_group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group1" group in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "parent_group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "parent_group2" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks "user3" user in "oneprovider-1" cluster members users list
    Then user of browser_admin sees following privileges of "user3" user in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: True
