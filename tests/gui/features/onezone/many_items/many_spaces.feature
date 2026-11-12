Feature: Management of a great number of spaces

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see correct number of previously created spaces in spaces list in the sidebar
    When using REST, user1 creates 509 spaces in "onezone" Onezone service
    And user of browser sees that "space000" has appeared on the spaces list in the sidebar
    And user of browser is idle for 5 seconds
    Then user of browser can see there are 509 spaces headers on the spaces list in the sidebar

    And using REST, user1 removes space named "space000" in "onezone" Onezone service
    And user of browser sees that "space000" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 508 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space001" in "onezone" Onezone service
    And user of browser sees that "space001" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 507 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space002" in "onezone" Onezone service
    And user of browser sees that "space002" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 506 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space003" in "onezone" Onezone service
    And user of browser sees that "space003" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 505 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space004" in "onezone" Onezone service
    And user of browser sees that "space004" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 504 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space005" in "onezone" Onezone service
    And user of browser sees that "space005" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 503 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space006" in "onezone" Onezone service
    And user of browser sees that "space006" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 502 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space007" in "onezone" Onezone service
    And user of browser sees that "space007" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 501 spaces headers on the spaces list in the sidebar
    And using REST, user1 removes space named "space008" in "onezone" Onezone service
    And user of browser sees that "space008" has disappeared on the spaces list in the sidebar
    And user of browser can see there are 500 spaces headers on the spaces list in the sidebar



  Scenario: User can see that correct space is opened after refreshing page
    When using REST, user1 creates 500 spaces in "onezone" Onezone service
    And user of browser sees that "space000" has appeared on the spaces list in the sidebar
    And user of browser is idle for 5 seconds
    And user of browser opens "space100" space on the lexicographically sorted list of 500 spaces in the sidebar
    And user of browser refreshes site and waits for page to load
    And user of browser can see that opened space is "space100" on the spaces list in the sidebar
