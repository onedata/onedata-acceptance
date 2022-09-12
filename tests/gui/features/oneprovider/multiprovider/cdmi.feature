Feature: Oneprovider functionality using multiple providers and cdmi service

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
                  - oneprovider-2:
                      storage: posix
                      size: 1000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  # TODO: VFS-9473 reimplement gui data distribution tests after move to file info modal
  # Scenario: User uploads file on one provider, sees it's distribution, writes to it using cdmi on other provider and sees it's distribution
  #   When user of browser clicks "space1" on the spaces list in the sidebar
  #   And user of browser clicks "Files" of "space1" space in the sidebar
  #   And user of browser sees file browser in files tab in Oneprovider page
  #   And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
  #   And user of browser sees that item named "20B-0.txt" has appeared in file browser

  #   And user of browser is idle for 90 seconds
  #   And user of browser sees file browser in files tab in Oneprovider page

  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser

  #   And user of browser sees that "Data distribution" modal has appeared
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled

  #   And user of browser sees that chunk bar for provider "oneprovider-2" is entirely empty
  #   And user of browser clicks "Close" confirmation button in displayed modal

  #   And using CDMI API space-owner-user writes "ABCD" to "/space1/20B-0.txt" starting at offset 20 in "oneprovider-2" provider
  #   And user of browser is idle for 90 seconds
  #   And user of browser clicks "Refresh" button from file browser menu bar
  #   And user of browser sees file browser in files tab in Oneprovider page

  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   Then user of browser sees (0, 20) chunk(s) for provider "oneprovider-1" in chunk bar
  #   And user of browser sees (20, 24) chunk(s) for provider "oneprovider-2" in chunk bar

  #   And user of browser clicks "Close" confirmation button in displayed modal


  # TODO: VFS-9473 reimplement gui data distribution tests after move to file info modal
  # Scenario: User uploads file, sees it's size, writes to it using cdmi and sees that size has grown
  #   When user of browser clicks "space1" on the spaces list in the sidebar
  #   And user of browser clicks "Files" of "space1" space in the sidebar
  #   And user of browser sees file browser in files tab in Oneprovider page
  #   And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
  #   And user of browser sees that item named "20B-0.txt" has appeared in file browser

  #   And user of browser sees that item named "20B-0.txt" is of 20 B size in file browser
  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is of 20 B size
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
  #   And user of browser clicks "Close" confirmation button in displayed modal

  #   And using CDMI API space-owner-user writes "ABCD" to "/space1/20B-0.txt" starting at offset 20 in "oneprovider-1" provider
  #   And user of browser is idle for 90 seconds
  #   And user of browser clicks "Refresh" button from file browser menu bar
  #   And user of browser sees file browser in files tab in Oneprovider page

  #   And user of browser sees that item named "20B-0.txt" is of 24 B size in file browser
  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   Then user of browser sees that chunk bar for provider "oneprovider-1" is of 24 B size
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled


  # TODO: VFS-9473 reimplement gui data distribution tests after move to file info modal
  # Scenario: User uploads file on one provider, sees it's distribution, reads half of file on other provider using cdmi and again sees it's distribution
  #   When user of browser clicks "space1" on the spaces list in the sidebar
  #   And user of browser clicks "Files" of "space1" space in the sidebar
  #   And user of browser sees file browser in files tab in Oneprovider page
  #   And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
  #   And user of browser sees that item named "20B-0.txt" has appeared in file browser

  #   And user of browser sees file browser in files tab in Oneprovider page
  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
  #   And user of browser sees that chunk bar for provider "oneprovider-2" is entirely empty
  #   And user of browser clicks "Close" confirmation button in displayed modal

  #   And using CDMI API space-owner-user reads from "/space1/20B-0.txt" in range 10 to 20 in "oneprovider-2" provider
  #   And user of browser is idle for 90 seconds
  #   And user of browser clicks "Refresh" button from file browser menu bar
  #   And user of browser sees file browser in files tab in Oneprovider page

  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
  #   Then user of browser sees (10, 20) chunk(s) for provider "oneprovider-2" in chunk bar

  #   And user of browser clicks "Close" confirmation button in displayed modal


  # TODO: VFS-9473 reimplement gui data distribution tests after move to file info modal
  # Scenario: User uploads file, sees it's distribution, writes to it beyond the end of file using cdmi and sees it's distribution again
  #   When user of browser clicks "space1" on the spaces list in the sidebar
  #   And user of browser clicks "Files" of "space1" space in the sidebar
  #   And user of browser sees file browser in files tab in Oneprovider page
  #   And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
  #   And user of browser sees that item named "20B-0.txt" has appeared in file browser

  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   And user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
  #   And user of browser clicks "Close" confirmation button in displayed modal

  #   And using CDMI API space-owner-user writes "ABCD" to "/space1/20B-0.txt" starting at offset 40 in "oneprovider-1" provider
  #   And user of browser is idle for 90 seconds
  #   And user of browser clicks "Refresh" button from file browser menu bar
  #   And user of browser sees file browser in files tab in Oneprovider page

  #   And user of browser clicks on menu for "20B-0.txt" file in file browser
  #   And user of browser clicks "Data distribution" option in data row menu in file browser
  #   And user of browser sees that "Data distribution" modal has appeared
  #   Then user of browser sees [(0, 20), (40, 44)] chunk(s) for provider "oneprovider-1" in chunk bar

  #   And user of browser clicks "Close" confirmation button in displayed modal


  Scenario: User uploads file, appends some text to it, downloads it and sees it's content
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And using CDMI API space-owner-user writes "ABCD" to "/space1/20B-0.txt" starting at offset 20 in "oneprovider-1" provider
    And user of browser is idle for 90 seconds
    And user of browser clicks "Refresh" button from file browser menu bar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "20B-0.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-0.txt" is equal to: "00000000000000000000ABCD"
