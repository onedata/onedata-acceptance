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

    And user of space_owner_browser opens "Dublin Core" public data type editor in share's private interface

    And user of space_owner_browser fills the input fields of "Dublin Core" form with:
      title: My test data
      another title: Another title
      creator: Kasia
      description: This is test
    
    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface

    And user of space_owner_browser sees that properties of "Dublin Core" metadata in share's private interface are like the following:
      title:
        - My test data
        - Another title
      creator: Kasia
      description: This is test

    And user of space_owner_browser sends "Public handle link" from share's private interface to user of browser1
    Then user of browser1 opens received URL

    And user of browser1 sees that public share is named "share_dir1"

    And user of browser1 sees that properties of "Dublin Core" metadata in share's public interface are like the following:
      title:
        - My test data
        - Another title
      creator: Kasia
      description: This is test

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

    And user of space_owner_browser opens "Europeana Data Model" public data type editor in share's private interface

    And user of space_owner_browser adds property "Title" in section in "EDM" form on share's private interface
    And user of space_owner_browser adds property "Creator of the original object" in section in "EDM" form on share's private interface

    # And user of space_owner_browser writes "Some Title" to "Title" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Second Title" to second "Title" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Description" to "Description/Caption" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser chooses "TEXT" in "Category" section in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Subject" to "Subject" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Type of object" to "Type of object" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Creator" to "Creator of the original object" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "EUreka3D" to "Parent entity (collection, object, site…)" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser chooses "Bone" in "Material" section in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Description of digital object" to "Description of digital object" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Type of digital object" to "Type of digital object" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser writes "Some Content provider institution" to "Content provider institution" section text field in "EDM" form on share's private interface
    # And user of space_owner_browser chooses "Photoconsortium" in "Name of organisation uploading the data" section in "EDM" form on share's private interface
    # And user of space_owner_browser chooses "CC BY 4.0" in "Copyright licence URL of the digital object" section in "EDM" form on share's private interface

    And user of browser1 fills text section fields of "EDM" metadata form with:
      Title: "Some Title"
      second Title: "Some Second Title"
      Description/Caption: "Some Description"
      Category: "TEXT"
      Subject: "Some Subject"
      Type of object: "Some Type of object"
      Creator of the original object: "Some Creator"
      Parent entity (collection, object, site…): "EUreka3D"
      Material: "http://vocab.getty.edu/aat/300011798"
      Description of digital object: "Some Description of digital object"
      Type of digital object: "Some Type of digital object"
      Content provider institution: "Some Content provider institution"
      Name of organisation uploading the data: "Photoconsortium"
      Copyright licence URL of the digital object: "CC BY 4.0"

    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface

    Then user of space_owner_browser sees that "Title" section has value "Some Title" in "EDM" form on share's private interface
    And user of space_owner_browser sees that second "Title" section has value "Some Second Title" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Description/Caption" section has value "Some Description" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Category" section has value "TEXT" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Subject" section has value "Some Subject" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Type of object" section has value "Some Type of object" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Creator of the original object" section has value "Some Creator" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Parent entity (collection, object, site…)" section has value "EUreka3D" in "EDM" form on share's private interface
    # After fix TODO: VFS-13113 add checking material name
    And user of space_owner_browser sees that "Material" section has value "http://vocab.getty.edu/aat/300011798" in "EDM" form on share's private interface

    And user of space_owner_browser sees that "Description of digital object" section has value "Some Description of digital object" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Type of digital object" section has value "Some Type of digital object" in "EDM" form on share's private interface

    And user of space_owner_browser sees that "Content provider institution" section has value "Some Content provider institution" in "EDM" form on share's private interface
    And user of space_owner_browser sees that "Name of organisation uploading the data" section has value "Photoconsortium" in "EDM" form on share's private interface
    # After fix TODO: VFS-13113 add checking license name
    And user of space_owner_browser sees that "Copyright licence URL of the digital object" section has value "http://creativecommons.org/licenses/by/4.0/" in "EDM" form on share's private interface

    And user of space_owner_browser sees warning alert message "The share name (share_dir1) does not match any title specified in the EDM metadata." in share's private interface

    And user of space_owner_browser clicks on menu on share view
    And user of space_owner_browser clicks "Rename" option in shares actions row menu
    And user of space_owner_browser sees that "Rename share" modal has appeared
    And user of space_owner_browser writes "Some Title" into text field in modal "Rename share"
    And user of space_owner_browser clicks on "Rename" button in modal "Rename share"

    And user of space_owner_browser sees there is no warning alert in share's private interface


Scenario: User sets DataCite metadata on mock handle service and sees updated XML after modification
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates "share_dir1" share of "dir1" directory
    And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

    And user of space_owner_browser opens "DataCite" public data type editor in share's private interface

    # And user of space_owner_browser writes "DataCite title initial" into title input text field in metadata form on share's private interface
    And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface
    And user of space_owner_browser sees that link on share's private interface is "Public handle link"
    And user of space_owner_browser copies "Public handle link" from share's private interface
    And user of space_owner_browser sends copied URL to user of browser1

    And user of browser1 opens received URL
    # And user of browser1 clicks "XML" button on share's public interface
    # And user of browser1 sees that XML data contains ["DataCite title initial", "identifier", "alternateIdentifier"] on share's public interface

    And user of space_owner_browser clicks "Modify" button on share's private interface
    # And user of space_owner_browser writes "DataCite title modified" into title input text field in metadata form on share's private interface
    And user of space_owner_browser clicks "Save" button on share's private interface

    And user of browser1 refreshes site
    Then user of browser1 clicks "XML" button on share's public interface
    # Then user of browser1 sees that XML data contains ["DataCite title modified", "identifier", "alternateIdentifier"] on share's public interface


Scenario: User sets OpenAIRE metadata on mock handle service and sees updated XML after modification
  When user of space_owner_browser opens file browser for "space1" space
  And user of space_owner_browser creates "share_dir1" share of "dir1" directory
  And user of space_owner_browser clicks on "Show details" link for "share_dir1" share in shares panel

  And user of space_owner_browser opens "Expose as Public Data" tab on share's private interface
  And user of space_owner_browser clicks "Choose a handle service" button on share's private interface
  And user of space_owner_browser chooses "Mock Handle Service" in dropdown menu for handle service on share's private interface
  And user of space_owner_browser clicks "Choose a metadata type" button on share's private interface
  And user of space_owner_browser chooses "OpenAIRE" in dropdown menu for metadata type on share's private interface
  And user of space_owner_browser clicks "Proceed" button on share's private interface

  # And user of space_owner_browser writes "OpenAIRE title initial" into title input text field in metadata form on share's private interface
  And user of space_owner_browser clicks "Expose as Public Data" button on share's private interface
  And user of space_owner_browser sees that link on share's private interface is "Public handle link"
  And user of space_owner_browser copies "Public handle link" from share's private interface
  And user of space_owner_browser sends copied URL to user of browser1

  And user of browser1 opens received URL
  # And user of browser1 clicks "XML" button on share's public interface
  And user of browser1 sees that XML data contains ["OpenAIRE title initial", "identifier", "alternateIdentifier"] on share's public interface

  And user of space_owner_browser clicks "Modify" button on share's private interface
  # And user of space_owner_browser writes "OpenAIRE title modified" into title input text field in metadata form on share's private interface
  And user of space_owner_browser clicks "Save" button on share's private interface

  And user of browser1 refreshes site
  Then user of browser1 clicks "XML" button on share's public interface
  # Then user of browser1 sees that XML data contains ["OpenAIRE title modified", "identifier", "alternateIdentifier"] on share's public interface