Feature: Dataset browser tests using user who is not the owner of a space

  Background:
      Given initial users configuration in "onezone" Onezone service:
              - user1
              - space-owner-user
      And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              users:
                - user1
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
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    Then user of browser_user1 cannot click "Create archive" option in data row menu in dataset browser


  Scenario: User fails to create dataset if he does not have manage datasets privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" file in file browser
    And user of browser_user1 clicks "Datasets" option in data row menu in file browser
    Then user of browser_user1 fails to click Mark this file as dataset toggle in Datasets modal
    And user of browser_user1 clicks on "X" button in modal "Datasets"


  Scenario: User fails to detach dataset if he does not have manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Detach" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Proceed" button in modal "Detach Dataset"
    Then user of browser_user1 sees that error modal with text "Changing some dataset(s) state failed!" appeared


  Scenario: User fails to enable write protection for dataset if he does not have manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

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
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Remove dataset" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Remove" button in modal "Remove Selected Dataset"
    Then user of browser_user1 sees that error modal with text "Removing some dataset(s) failed!" appeared


  Scenario: User successfully creates dataset if he has manage datasets privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True

    When user of browser_user1 creates dataset for item "dir1" in "space1"
    Then user of browser_user1 sees Dataset status tag for "dir1" in file browser


  Scenario: User  successfully removes dataset if he has manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Remove dataset" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Remove" button in modal "Remove Selected Dataset"
    Then user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 does not see Dataset status tag for "dir1" in file browser


  Scenario: User successfully enable write protection for dataset if he has manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Write protection" option in data row menu in dataset browser
    And user of browser_user1 clicks data write protection toggle in Write Protection modal
    And user of browser_user1 clicks metadata write protection toggle in Write Protection modal
    And user of browser_user1 clicks on "Close" button in modal "Write Protection"
    Then user of browser_user1 sees metadata protected status tag for "dir1" in dataset browser
    And user of browser_user1 sees data protected status tag for "dir1" in dataset browser


 Scenario: User successfully detaches dataset if he has manage datasets privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True

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
    When user of space_owner_browser creates dataset for item "dir1" in "space1"

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True
              View archives: True
              Create archives: True

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" dataset in dataset browser
    And user of browser_user1 clicks "Create archive" option in data row menu in dataset browser
    And user of browser_user1 clicks on "Create" button in modal "Create Archive"
    And user of browser_user1 goes back to dataset browser from archive browser
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    Then user of browser_user1 sees that item "dir1" has 1 archive


  Scenario: User does not see archive file browser if he does not have view archives privilege
    When user of space_owner_browser creates dataset for item "dir1" in "space1"
    And user of space_owner_browser creates archive for item "dir1" in "space1" with following configuration:
          layout: plain

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Dataset & archive management:
            granted: False

    And user of browser_user1 clicks Datasets of "space1" in the sidebar
    And user of browser_user1 sees dataset browser in datasets tab in Oneprovider page
    And user of browser_user1 clicks on archives count link for "dir1" in dataset browser
    Then user of browser_user1 sees that error page with text "OPERATION NOT PERMITTED" appeared

