Feature: Basic data tab operations on file metadata in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser


  Scenario: Open metadata panel and check presence of navigation tabs
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Edit metadata"
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser sees [Basic, JSON, RDF] navigation tabs in metadata panel opened for "file1"


  Scenario: Edit metadata icon is visible if file has empty basic metadata entry
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser does not see metadata icon for "file1" in file browser
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    Then user of browser sees metadata icon for "file1" in file browser


  Scenario: Invalid basic metadata entry for file should be colored red
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    Then user of browser sees that edited attribute key in metadata panel opened for "file1" is highlighted as invalid


  Scenario: Entered invalid metadata for file will not be saved
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    # try saving empty forms
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page

    # try saving metadata with record key being filled only
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on add basic metadata entry icon in metadata panel opened for "file1"
    And user of browser sees that "Save all changes" button in metadata panel opened for "file1" is disabled

    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser should not see basic metadata entry with attribute named "attr" in metadata panel opened for "file1"


  Scenario: Add metadata to file (clicks both add icon and "Save all changes" button)
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser types "val" to value input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on add basic metadata entry icon in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*

    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser should see basic metadata entry with attribute named "attr" and value "val" in metadata panel opened for "file1"


  Scenario: Add metadata to file (clicks only "Save all changes" button)
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser types "val" to value input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*

    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser should see basic metadata entry with attribute named "attr" and value "val" in metadata panel opened for "file1"


  Scenario: Delete single basic metadata entry for file
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser types "val" to value input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on add basic metadata entry icon in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*

    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on delete basic metadata entry icon for basic metadata entry with attribute named "attr" in metadata panel opened for "file1"
    Then user of browser should not see basic metadata entry with attribute named "attr" in metadata panel opened for "file1"


  Scenario: User should not see any metadata for file after clicking "Remove metadata" button
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser types "val" to value input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*

    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser should see basic metadata entry with attribute named "attr" and value "val" in metadata panel opened for "file1"
    And user of browser clicks on "Remove metadata" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Dd]eleted.*metadata.*file1.*
    And user of browser sees that metadata panel for "file1" in files list has disappeared
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser should not see basic metadata entry with attribute named "attr" in metadata panel opened for "file1"


  Scenario: User starts adding metadata to file but discards changes
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser types "attr" to attribute input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser types "val" to value input box of new metadata basic entry in metadata panel opened for "file1"
    And user of browser clicks on add basic metadata entry icon in metadata panel opened for "file1"
    And user of browser clicks on "Discard changes" button in metadata panel opened for "file1"
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    Then user of browser should not see basic metadata entry with attribute named "attr" in metadata panel opened for "file1"


  Scenario: Add valid metadata to file in JSON format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared

    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    And user of browser types "{"id": 1}" to JSON textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    Then user of browser sees that JSON textarea placed in metadata panel opened for "file1" contains {"id": 1}


  Scenario: Delete file metadata in JSON format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared

    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    And user of browser types "{"id": 1}" to JSON textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    And user of browser sees that JSON textarea placed in metadata panel opened for "file1" contains {"id": 1}
    And user of browser clicks on "Remove metadata" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Dd]eleted.*metadata.*file1.*
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    Then user of browser sees that content of JSON textarea placed in metadata panel opened for "file1" is equal to: "{}"


  Scenario: Discard changes while entering metadata for file in JSON format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared

    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    And user of browser types "{"id": 1}" to JSON textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Discard changes" button in metadata panel opened for "file1"
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on JSON navigation tab in metadata panel opened for "file1"
    Then user of browser sees that content of JSON textarea placed in metadata panel opened for "file1" is equal to: "{}"


  Scenario: Add valid metadata to file in XML format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    And user of browser types "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" to RDF textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    Then user of browser sees that RDF textarea placed in metadata panel opened for "file1" contains <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>


  Scenario: Delete file metadata in XML format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared

    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    And user of browser types "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" to RDF textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Save all changes" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Mm]etadata.*saved.*successfully.*
    And user of browser refreshes site
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    And user of browser sees that RDF textarea placed in metadata panel opened for "file1" contains <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>
    And user of browser clicks on "Remove metadata" button in metadata panel opened for "file1"
    And user of browser sees an info notify with text matching to: .*[Dd]eleted.*metadata.*file1.*
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    Then user of browser sees that content of RDF textarea placed in metadata panel opened for "file1" is equal to: ""


  Scenario: Discard changes while entering metadata for file in XML format
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared

    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    And user of browser types "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" to RDF textarea placed in metadata panel opened for "file1"
    And user of browser clicks on "Discard changes" button in metadata panel opened for "file1"
    And user of browser sees that metadata panel for "file1" in files list has disappeared

    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks on metadata tool icon in file row for "file1" in file browser
    And user of browser sees that metadata panel for "file1" in files list has appeared
    And user of browser clicks on RDF navigation tab in metadata panel opened for "file1"
    Then user of browser sees that content of RDF textarea placed in metadata panel opened for "file1" is equal to: ""
