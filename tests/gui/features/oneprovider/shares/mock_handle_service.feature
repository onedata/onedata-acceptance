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
    And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

    And user of space_owner_browser adds "Description for another user to check if can see" description for "share_dir1" share on share's private interface
    And user of space_owner_browser opens "Dublin Core" Public Data editor in share's private interface

    And user of space_owner_browser fills the input fields of Dublin Core form with:
      title: 
        - My test data
        - Another title
      creator: 
        - Kasia
        - Jakub
      description:
        - This is test
        - test2
      publisher:
        - Some publisher
        - Another publisher
    
    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface

    And user of space_owner_browser sees that properties of Dublin Core metadata in share's private interface are like the following:
      title:
        - My test data
        - Another title
      creator: 
        - Kasia
        - Jakub
      description:
        - This is test
        - test2
      publisher:
        - Some publisher
        - Another publisher

    And user of space_owner_browser sends "Public handle link" from share's private interface to user of browser1
    Then user of browser1 opens received URL

    And user of browser1 sees that public share is named "share_dir1"

    And user of browser1 sees that properties of Dublin Core metadata in share's public interface are like the following:
      title:
        - My test data
        - Another title
      creator:
        - Kasia
        - Jakub
      description:
        - This is test
        - test2
      publisher:
        - Some publisher
        - Another publisher

    And user of browser1 clicks "XML" button on share's public interface
    And user of browser1 sees that XML data contains ["My test data", "Another title", "Kasia", "This is test"] on share's public interface

    And user of browser1 opens share's file browser on share's public interface
    And user of browser1 goes to "dir1" in share's file browser
    And user of browser1 sees item(s) named "file1" in share's file browser

    And user of browser1 opens "Description" tab on share's public interface
    And user of browser1 sees "Description for another user to check if can see" description on share's public interface


  Scenario: User opens Public Data expose view using toggle in modal "Share / Publish directory"
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser clicks on "Share / Publish" in context menu for "dir1"
    And user of space_owner_browser writes "share_dir1" into text field in modal "Share / Publish directory"
    And user of space_owner_browser checks "Expose as a Public Data record" toggle in modal "Share / Publish directory"
    And user of space_owner_browser clicks on "Create" button in modal "Share / Publish directory"

    Then user of space_owner_browser sees "Expose as Public Data" tab on share's private interface
    And user of space_owner_browser sees that share in private view is named "share_dir1"


  Scenario: User sets EDM metadata on mock handle service and after saving can see it
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates "share_dir1" share of "dir1" directory
    And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

    And user of space_owner_browser opens "Europeana Data Model" Public Data editor in share's private interface

    And user of space_owner_browser fills text section fields of EDM metadata form with:
      Title: 
        - "Some Title"
        - "Some Second Title"
      Description/Caption: "Some Description"
      Category: "TEXT"
      Subject: "Some Subject"
      Type of object: "Some Type of object"
      Creator of the original object: "Some Creator"
      Parent entity (collection, object, site…): "EUreka3D"
      Material: 
        group: "Bone"
        value: "Bone"
      Description of digital object: "Some Description of digital object"
      Type of digital object: "Some Type of digital object"
      Content provider institution: "Some Content provider institution"
      Name of organisation uploading the data: "Photoconsortium"
      Copyright licence URL of the digital object: "CC BY 4.0"

    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface

    Then user of space_owner_browser sees that fields of EDM metadata form are like the following:
      Title:
        - "Some Title"
        - "Some Second Title"
      Description/Caption: "Some Description"
      Category: "TEXT"
      Subject: "Some Subject"
      Type of object: "Some Type of object"
      Creator of the original object: "Some Creator"
      Parent entity (collection, object, site…): "EUreka3D"
      # After fix TODO: VFS-13113 add checking material name
      Material: "http://vocab.getty.edu/aat/300011798"
      Description of digital object: "Some Description of digital object"
      Type of digital object: "Some Type of digital object"
      Content provider institution: "Some Content provider institution"
      Name of organisation uploading the data: "Photoconsortium"
      # After fix TODO: VFS-13113 add checking license name
      Copyright licence URL of the digital object: "http://creativecommons.org/licenses/by/4.0/" 

    And user of space_owner_browser sees warning alert message "The share name (share_dir1) does not match any title specified in the EDM metadata." in share's private interface

    And user of space_owner_browser renames "share_dir1" share to "Some Title" on share's private interface
    And user of space_owner_browser sees there is no warning alert in share's private interface


Scenario: User sets DataCite metadata on mock handle service and sees updated XML after modification
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates "share_dir1" share of "dir1" directory
    And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

    And user of space_owner_browser opens "DataCite" Public Data editor in share's private interface
    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface
    
    And user of space_owner_browser sends "Public handle link" from share's private interface to user of browser1

    And user of browser1 opens received URL
    Then user of browser1 sees that DataCite XML data contains nodes like: ["datacite:identifier", "datacite:alternateIdentifier"] on share's private interface
    And user of browser1 sees that DataCite XML node with "datacite:title" tag has "share_dir1" value in share's private interface

    And user of space_owner_browser modifies DataCite XML element with "datacite:title" tag by changing its text to "new_title" in share's private interface

    And user of browser1 refreshes site
    And user of browser1 sees that DataCite XML node with "datacite:title" tag has "new_title" value in share's private interface


Scenario: User sets OpenAIRE metadata on mock handle service and sees updated XML after modification
  When user of space_owner_browser opens file browser for "space1" space
  And user of space_owner_browser creates "share_dir1" share of "dir1" directory
  And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

  And user of space_owner_browser opens "OpenAIRE" Public Data editor in share's private interface
  And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface

  And user of space_owner_browser sends "Public handle link" from share's private interface to user of browser1

  And user of browser1 opens received URL

  Then user of browser1 sees that OpenAIRE XML data contains nodes like: ["datacite:identifier", "datacite:alternateIdentifier"] on share's private interface
  And user of browser1 sees that OpenAIRE XML node with "datacite:title" tag has "share_dir1" value in share's private interface

  And user of space_owner_browser modifies OpenAIRE XML element with "datacite:title" tag by changing its text to "new_title" in share's private interface

  And user of browser1 refreshes site
  And user of browser1 sees that OpenAIRE XML node with "datacite:title" tag has "new_title" value in share's private interface


Scenario: User sees public data status tag after refreshing file list
  When user of space_owner_browser opens file browser for "space1" space
  And user of space_owner_browser creates "share_dir1" share of "dir1" directory
  And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel
  And user of space_owner_browser opens "Dublin Core" Public Data editor in share's private interface
  And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface
  And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
  And user of space_owner_browser sees file browser in files tab in Oneprovider page
  And user of space_owner_browser clicks "Refresh" button from file browser menu bar
  Then user of space_owner_browser sees public data status tag for "dir1" in file browser
  