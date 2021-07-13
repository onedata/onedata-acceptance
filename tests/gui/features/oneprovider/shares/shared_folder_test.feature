Feature: shared and linked folders
  Background:
    Given initial users configuration in "onezone" Onezone service:
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
                    - dir2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


    Scenario: User shares folder
      When user of browser clicks on Files in the space1 sidebar
      And user of browser clicks on dir2 options menu
      And user of browser clicks on the share option in the popover menu in dir2
      And user of browser clicks on the create button in the modal window
      And user of browser clicks on the close button in the second modal window
      And user of browser clicks on dir1 options menu to make symbolic link
      And user of browser clicks on the share option in the popover menu in dir1
      And user of browser doubleclicks on the dir2 to enter it
      And user of browser clicks on the place_the_symbolic_link button in the top right corner
      And user of browser clicks on the shares button in the left sidebar
      And user of browser clicks on the dir2 button to enter it in shares browser
      And user of browser doubleclicks on the dir2 button in the item browser in shares page
      Then user of browser sees error icon in the share_browser


