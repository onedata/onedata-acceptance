Feature: Test user has access to space via group membership


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
              groups:
                  - group1

	And opened [space_owner_browser, browser1] with [space-owner-user, user1] signed in to [onezone, onezone] service
	And opened oneprovider-1 Oneprovider view in web GUI by user of space_owner_browser


 Scenario: User has access to space via group membership

    # Space-owner-user generate group invitation token
    When user of space_owner_browser clicks on the "groups" tab in main menu sidebar
    And user of space_owner_browser sees that group named "group1" has appeared in the groups list
    And user of space_owner_browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of space_owner_browser clicks on the "INVITE USER" item in settings dropdown for group named "group1"
    And user of space_owner_browser sees that "Invite user to the group" modal has appeared
    And user of space_owner_browser sees non-empty token in active modal
    And user of space_owner_browser clicks on copy button in active modal
    And user of space_owner_browser sends copied token to user of browser1
    And user of space_owner_browser clicks "OK" confirmation button in displayed modal
    And user of space_owner_browser sees that the modal has disappeared

    # User1 joins group
    And user of browser1 clicks on the join button in "Group management" Onezone panel
    And user of browser1 sees that "Join a group" modal has appeared
    And user of browser1 clicks on input box in active modal
    And user of browser1 types received token on keyboard
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared

	# Space-owner-user uploads file
    And user of space_owner_browser clicks on the "data" tab in main menu sidebar
	And user of space_owner_browser uses upload button in toolbar to upload file "20B-0.txt" to current dir

    # Space-owner-user changes file acl
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
   	And user of space_owner_browser clicks once on item named "20B-0.txt" in file browser
    And user of space_owner_browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of space_owner_browser sees that "Edit permissions" modal has appeared
    And user of space_owner_browser selects "ACL" permission type in active modal
    And user of space_owner_browser clicks "Add" in ACL edit permissions modal
    And user of space_owner_browser selects group as subject type in first ACL record in edit permissions modal
    And user of space_owner_browser expands select list for first ACL record in edit permissions modal
    And user of space_owner_browser selects group1 from subject list in first ACL record in edit permissions modal
    And user of space_owner_browser sets "read" option in first ACL record in edit permissions modal
    And user of space_owner_browser clicks "Ok" confirmation button in displayed modal
    And user of space_owner_browser sees that the modal has disappeared

    # User1 sees file in Oneprovider files tab
    And user of browser1 clicks on "oneprovider-1" provider in expanded "GO TO YOUR FILES" Onezone panel
    And user of browser1 clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map
    And user of browser1 sees that Oneprovider session has started
    And user of browser1 sees file browser in files tab in Oneprovider page
    Then user of browser1 sees that item named "20B-0.txt" has appeared in file browser
