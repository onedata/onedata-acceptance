Feature: Dataset browser tests using user who is not the owner of a space

  Background:
      Given initial users configuration in "onezone" Onezone service:
              - user1
              - space-owner-user
      And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
              storage:
                  defaults:
                      provider: oneprovider-1
                  directory tree:
                      - dir1

      And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User cannot create archive for existing dataset if he does not have dataset & archive management privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks Close button in Datasets modal
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1
    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 cannot click "Create archive" option in data row menu in desktop browser


  Scenario: User cannot fails to dataset if he does not have dataset & archive management privilege