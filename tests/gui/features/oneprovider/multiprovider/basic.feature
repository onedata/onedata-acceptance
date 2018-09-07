Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
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
                  - oneprovider-2:
                      storage: posix
                      size: 1000000
          space2:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
                  - oneprovider-2:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User creates space in one provider and sees that it was created also in other provider
    # create space in onezone
    When user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "multiprov" into space name text field
    And user of browser clicks on Create new space button
    And user of browser sees that "multiprov" has appeared on the spaces list in the sidebar

    # check space in first provider
    And user of browser opens oneprovider-1 Oneprovider view in web GUI
    And user of browser sees that Oneprovider session has started
    And user of browser sees "multiprov" is in spaces list on Oneprovider page

    # check space in second provider
    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser opens oneprovider-2 Oneprovider view in web GUI
    And user of browser sees that Oneprovider session has started
    Then user of browser sees "multiprov" is in spaces list on Oneprovider page


  Scenario: User changes name of space in one provider and sees that it was changed also in other provider
    # rename space in onezone
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser writes "NewNameSpace" into rename space text field
    And user of browser presses enter on keyboard
    And user of browser sees that "NewNameSpace" has appeared on the spaces list in the sidebar
    And user of browser sees that "space1" has disappeared on the spaces list in the sidebar

    # check space in first provider
    And user of browser opens oneprovider-1 Oneprovider view in web GUI
    And user of browser sees that Oneprovider session has started
    And user of browser sees "NewNameSpace" is in spaces list on Oneprovider page
    And user of browser sees "space1" is not in spaces list on Oneprovider page

    # check space in second provider
    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser opens oneprovider-2 Oneprovider view in web GUI
    And user of browser sees that Oneprovider session has started
    Then user of browser sees "NewNameSpace" is in spaces list on Oneprovider page
    And user of browser sees "space1" is not in spaces list on Oneprovider page

  Scenario: User leaves space in one provider and sees that it was leaved from also in other provider
    # leave space in onezone
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on leave space button
    And user of browser clicks on yes button

    # check space in first provider
    And user of browser opens oneprovider-1 Oneprovider view in web GUI
    And user of browser sees "space1" is not in spaces list on Oneprovider page

    # check space in first provider
    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser opens oneprovider-2 Oneprovider view in web GUI
    Then user of browser sees "space1" is not in spaces list on Oneprovider page
