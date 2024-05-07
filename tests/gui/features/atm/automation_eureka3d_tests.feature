Feature: Eureka3d workflow tests


  Background:
    Given initial users configuration in "onezone" Onezone service:
          - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            groups:
                - group1
            providers:
                - oneprovider-1:
                    storage: s3
                    size: 10000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1

    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And user of browser uploads "initialize-eureka3D-project" workflow from automation-examples repository to "inventory1" inventory


  Scenario: User sees successful execution of uploaded "initialize-eureka3D-project"
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "Initialize Eureka3D project" workflow in "space1" space with the following initial values:
      Parent directory:
        - dir1
      Project name:
        - "hello"
      Managing group ID:
        - { "groupId": "$(resolve_id group1)" }

    Then user of browser sees "Finished" status in status bar in workflow visualizer

    And user of browser sees that number of elements in the content of the "Project root dirs" store details modal is 1
    And user of browser closes "Store details" modal

    And user of browser sees that number of elements in the content of the "Project dirs" store details modal is 4
    And user of browser closes "Store details" modal

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that the file structure in file browser is as follow:
      - dir1:
        - hello:
          - 0-Reconnaissance
          - 1-Preliminary
          - 2-Detailed
          - Paradata
    And user of browser clicks and presses enter on item named "dir1" in file browser
    # Check ACL record
    And user of browser clicks on "Permissions" in context menu for "hello"
    And user of browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of browser selects "ACL" permission type in edit permissions panel
    And user of browser sees exactly 1 ACL record in edit permissions panel
    And user of browser sees that first ACL record in edit permissions panel is set for group group1
    And user of browser sees that all privileges are set in first ACL record in edit permissions panel


  Scenario: User sees successful execution of uploaded "initialize-eureka3D-project" with already created project in file browser
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    # create project dirs
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser creates dir "hello" in current dir
    And user of browser clicks and presses enter on item named "hello" in file browser
    And user of browser creates dir "0-Reconnaissance" in current dir
    And user of browser creates dir "1-Preliminary" in current dir
    And user of browser creates dir "2-Detailed" in current dir
    And user of browser creates dir "Paradata" in current dir

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "Initialize Eureka3D project" workflow in "space1" space with the following initial values:
      Parent directory:
        - dir1
      Project name:
        - "hello"
      Managing group ID:
        - { "groupId": "$(resolve_id group1)" }

    Then user of browser sees "Finished" status in status bar in workflow visualizer

    And user of browser sees that number of elements in the content of the "Project root dirs" store details modal is 1
    And user of browser closes "Store details" modal

    And user of browser sees that number of elements in the content of the "Project dirs" store details modal is 4
    And user of browser closes "Store details" modal

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that the file structure in file browser is as follow:
      - dir1:
        - hello:
          - 0-Reconnaissance
          - 1-Preliminary
          - 2-Detailed
          - Paradata
    And user of browser clicks and presses enter on item named "dir1" in file browser
    # Check ACL record
    And user of browser clicks on "Permissions" in context menu for "hello"
    And user of browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of browser selects "ACL" permission type in edit permissions panel
    And user of browser sees exactly 1 ACL record in edit permissions panel
    And user of browser sees that first ACL record in edit permissions panel is set for group group1
    And user of browser sees that all privileges are set in first ACL record in edit permissions panel
