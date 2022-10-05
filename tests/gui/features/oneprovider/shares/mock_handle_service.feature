Feature: Public share published with mock handle service

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
                    - dir1:
                        - file1: 11111

    And user space-owner-user is added to mock handle service in Onezone
    And users opened [space_owner_browser, browser1] browsers' windows
    And user of space_owner_browser opened onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service


  Scenario: User views files from public interface of share shared from another user on mock handle service
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates "share_dir1" share of "dir1" directory
    And user of space_owner_browser clicks on "share_dir1" share link with icon in shares panel

    And user of space_owner_browser opens "Description" tab on share's private interface
    And user of space_owner_browser clicks "Create description" button in "Description" form on share's private interface
    And user of space_owner_browser types "Description for another user to check if can see" into description field in "Description" form on share's private interface
    And user of space_owner_browser clicks "Save" button in "Description" form on share's private interface

    And user of space_owner_browser opens "Publish as Open Data" tab on share's private interface
    And user of space_owner_browser clicks "Choose a handle service" button on share's private interface
    And user of space_owner_browser chooses "Mock Handle Service" in dropdown menu for handle service on share's private interface
    And user of space_owner_browser clicks "Proceed" button on share's private interface

    And user of space_owner_browser writes "My test data" into last title input text field in "Dublin Core Metadata" form on share's private interface
    And user of space_owner_browser clicks "Add another title" button in "Dublin Core Metadata" form on share's private interface
    And user of space_owner_browser writes "Another title" into last title input text field in "Dublin Core Metadata" form on share's private interface
    And user of space_owner_browser writes "Kasia" into last creator input text field in "Dublin Core Metadata" form on share's private interface
    And user of space_owner_browser writes "This is test" into last description input text field in "Dublin Core Metadata" form on share's private interface
    And user of space_owner_browser clicks "Publish as Open Data" button on share's private interface

    And user of space_owner_browser sees that titles are ["My test data", "Another title"] in "Dublin Core Metadata" on share's private interface
    And user of space_owner_browser sees that creator is "Kasia" in "Dublin Core Metadata" on share's private interface
    And user of space_owner_browser sees that description is "This is test" in "Dublin Core Metadata" on share's private interface
    And user of space_owner_browser sees that link on share's private interface is "Public handle link"
    And user of space_owner_browser copies "Public handle link" from share's private interface
    And user of space_owner_browser sends copied URL to user of browser1

    Then user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"
    And user of browser1 sees that titles are ["My test data", "Another title"] in "Dublin Core Metadata" on share's public interface
    And user of browser1 sees that creator is "Kasia" in "Dublin Core Metadata" on share's public interface
    And user of browser1 sees that description is "This is test" in "Dublin Core Metadata" on share's public interface

    And user of browser1 clicks "XML" button on share's public interface
    And user of browser1 sees that XML data contains ["My test data", "Another title", "Kasia", "This is test"] on share's public interface

    And user of browser1 opens "Files" tab on share's public interface
    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees item(s) named "file1" in file browser

    And user of browser1 opens "Description" tab on share's public interface
    And user of browser1 sees "Description for another user to check if can see" description on share's public interface

