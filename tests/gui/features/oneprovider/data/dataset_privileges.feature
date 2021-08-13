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


  Scenario: User cannot create archive for existing dataset if he does not have create archives privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create and send token
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
    Then user of browser_user1 cannot click "Create archive" option in data row menu in dataset browser


  Scenario: User fails to create dataset if he does not have manage datasets privilege
    # create and send token
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Datasets" option in data row menu in file browser
    Then user of browser_user1 fails to click Mark this file as dataset toggle in Datasets modal
    And user of browser_user1 clicks on "Close" button in modal "Datasets"


  Scenario: User fails to detach dataset if he does not have manage datasets privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create and send token
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
    And user of browser_user1 clicks "Detach" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Proceed" button in modal "Detach Dataset"
    Then user of browser_user1 sees that error modal with text "Changing some dataset(s) state failed!" appeared


  Scenario: User fails to enable write protection for dataset if he does not have manage datasets privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create and send token
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
    And user of browser_user1 clicks "Write protection" option in data row menu in dataset browser
    And user of browser_user1 clicks data write protection toggle in Write Protection modal
    Then user of browser_user1 sees that error modal with text "Changing write protection settings failed!" appeared
    And user of browser_user1 closes "Error" modal
    And user of browser_user1 clicks metadata write protection toggle in Write Protection modal
    And user of browser_user1 sees that error modal with text "Changing write protection settings failed!" appeared


  Scenario: User fails to remove dataset if he does not have manage datasets privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create and send token
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
    And user of browser_user1 clicks "Remove dataset" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Remove" button in modal "Remove Selected Dataset"
    Then user of browser_user1 sees that error modal with text "Removing some dataset(s) failed!" appeared


  Scenario: User successfully creates dataset if he has manage datasets privilege
    # create and send token
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Datasets" option in data row menu in file browser
    And user of browser_user1 clicks Mark this file as dataset toggle in Datasets modal
    And user of browser_user1 clicks on "Close" button in modal "Datasets"
    Then user of browser_user1 sees Dataset status tag for "dir1" in file browser


  Scenario: User  successfully removes dataset if he has manage datasets privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create and send token
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Remove dataset" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Remove" button in modal "Remove Selected Dataset"
    Then user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 does not see Dataset status tag for "dir1" in file browser


  Scenario: User successfully enable write protection for dataset if he has manage datasets privilege
    # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    #create and send token
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Write protection" option in data row menu in dataset browser
    And user of browser_user1 clicks data write protection toggle in Write Protection modal
    And user of browser_user1 clicks metadata write protection toggle in Write Protection modal
    And user of browser_user1 clicks Close button in Write Protection modal
    And user of browser_user1 sees metadata protected status tag for "dir1" in dataset browser
    And user of browser_user1 sees data protected status tag for "dir1" in dataset browser


 Scenario: User successfully detaches dataset if he has manage datasets privilege
   # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

   # create and send token
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Detach" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Proceed" button in modal "Detach Dataset"
    And user of browser_user1 clicks on detached view mode on dataset browser page
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 sees item(s) named "dir1" in dataset browser
    Then user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 does not see Dataset status tag for "dir1" in file browser


 Scenario: User successfully creates archive for existing dataset if he has create archives and manage datasets privilege
   # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

   #create and send token
    And user of space_owner_browser clicks on Tokens in the main menu
    And user of space_owner_browser creates and checks token with following configuration:
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
                View archives: True
                Create archives: True
    And user of space_owner_browser clicks on copy button in token view
    And user of space_owner_browser sends copied token to user of browser_user1

    And user of browser_user1 joins space using received token
    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Create archive" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Create" button in modal "Create Archive"
    Then user of browser_user1 sees that item "dir1" has 1 Archives


  Scenario: User does not see archive file browser if he does not have view archives privilege
   # create dataset
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" file in file browser
    And user of space_owner_browser clicks "Datasets" option in data row menu in file browser
    And user of space_owner_browser clicks Mark this file as dataset toggle in Datasets modal
    And user of space_owner_browser clicks on "Close" button in modal "Datasets"

    # create archive
    And user of space_owner_browser clicks Datasets of "space1" in the sidebar
    And user of space_owner_browser sees dataset browser in datasets tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" dataset in dataset browser
    And user of space_owner_browser clicks "Create archive" option in data row menu in dataset browser
    And user of space_owner_browser clicks on "Create" button in modal "Create Archive"

   #create and send token
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
    And user of browser_user1 clicks on 1 in "dir1" Archives

    Then user of browser_user1 sees that error page with text "OPERATION NOT PERMITTED" appeared


