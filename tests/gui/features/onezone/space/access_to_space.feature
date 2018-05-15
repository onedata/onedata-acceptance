Feature: Test user has access to space via group membership


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
              groups:
                  - group1

	And opened [browser1, browser2] with [user1, user2] logged to [onezone, onezone] service
	And opened oneprovider-1 Oneprovider view in web GUI by user of browser1


 Scenario: User has access to space via group membership

    # user1 generate group invitation token
    When user of browser1 clicks on the "groups" tab in main menu sidebar
    And user of browser1 sees that group named "group1" has appeared in the groups list
    And user of browser1 clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser1 clicks on the "INVITE USER" item in settings dropdown for group named "group1"
    And user of browser1 sees that "Invite user to the group" modal has appeared
    And user of browser1 sees non-empty token in active modal
    And user of browser1 clicks on copy button in active modal
    And user of browser1 sends copied token to user of browser2
    And user of browser1 clicks "OK" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    # user2 joins group
    And user of browser2 clicks on the join button in "Group management" Onezone panel
    And user of browser2 sees that "Join a group" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types received token on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# user1 uploads file
    And user of browser1 clicks on the "data" tab in main menu sidebar
	And user of browser1 uses upload button in toolbar to upload file "20B-0.txt" to current dir

    # user1 changes file acl
    And user of browser1 sees file browser in data tab in Oneprovider page
   	And user of browser1 clicks once on item named "20B-0.txt" in file browser
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "ACL" permission type in active modal
    And user of browser1 clicks "Add" in ACL edit permissions modal
    And user of browser1 selects group as subject type in first ACL record in edit permissions modal
    And user of browser1 expands select list for first ACL record in edit permissions modal
    And user of browser1 selects group1 from subject list in first ACL record in edit permissions modal
    And user of browser1 sets "read" option in first ACL record in edit permissions modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    # user2 sees file in Oneprovider data tab
    And user of browser2 clicks on "oneprovider-1" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser2 clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map
    And user of browser2 sees that Oneprovider session has started
    And user of browser2 sees file browser in data tab in Oneprovider page
    Then user of browser2 sees that item named "20B-0.txt" has appeared in file browser
