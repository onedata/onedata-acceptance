Feature: Basic files tab operations on directory xattrs metadata in file browser

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
                    - file2: 11111
                - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: Open metadata panel and check absence of any metadata
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks on menu for "<item>" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees that "<modal>" modal has appeared
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    Then user of browser sees [xattrs, JSON, RDF] navigation tabs in metadata panel
    And user of browser sees that all metadata tabs are marked as empty
    And user of browser sees that there is no metadata in metadata panel

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User adds xattr metadata entry and checks their presence with metadata status tag and after refreshing page
    When user of browser opens file browser for "space1" space

    And user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser types "attr" to key input box of new metadata xattr entry
    And user of browser types "val" to value input box of attribute "attr" metadata xattr entry
    And user of browser clicks on "Save" button in metadata panel
    Then user of browser sees metadata status tag for "<item>" in file browser

    And user of browser opens "Metadata" tab in "<modal>" modal via clicking on metadata status tag for "<item>"
    And user of browser sees xattr metadata entry with key "attr" and value "val"

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser opens "Metadata" tab in "<modal>" modal via clicking on metadata status tag for "<item>"
    And user of browser sees xattr metadata entry with key "attr" and value "val"

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: Delete one of two xattrs metadata entries
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr1" and value "val1"
    And user of browser adds xattr entry with key "attr2" and value "val2"
    And user of browser clicks on "Save" button in metadata panel

    And user of browser clicks on delete icon for xattr metadata entry with key "attr1"
    Then user of browser does not see xattr metadata entry with key "attr1"
    And user of browser sees xattr metadata entry with key "attr2" and value "val2"
    And user of browser clicks on "Save" button in metadata panel

    And user of browser does not see xattr metadata entry with key "attr1"
    And user of browser sees xattr metadata entry with key "attr2" and value "val2"

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: Delete all xattrs metadata entries after saving it
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel

    And user of browser clicks on delete icon for xattr metadata entry with key "attr"
    Then user of browser sees that there is no xattrs metadata
    And user of browser clicks on "Save" button in metadata panel
    And user of browser does not see metadata status tag for "<item>" in file browser

    And user of browser sees that there is no xattrs metadata

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: Delete single xattr metadata entry (one visit in modal)
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser sees xattr metadata entry with key "attr" and value "val"
    And user of browser clicks on delete icon for xattr metadata entry with key "attr"
    Then user of browser sees that there is no xattrs metadata

    And user of browser clicks on "X" button in modal "<modal>"
    And user of browser does not see metadata status tag for "<item>" in file browser

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser sees that there is no xattrs metadata

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User starts adding xattrs metadata, but discards changes
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Discard changes" button in metadata panel
    Then user of browser does not see xattr metadata entry with key "attr"

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User sees empty xattr value in xattr column, then add metadata and can see it, also after refreshing
    When user of browser opens file browser for "space1" space
    And user of browser creates new xattr column with "attr" key in file browser table
    And user of browser enables only "attr" column in columns configuration popover in file browser table
    Then user of browser sees that item named "<item>" has "—" value in xattr column in file browser

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<modal>"
    And user of browser sees that item named "<item>" has "val" value in xattr column in file browser

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space
    And user of browser sees that item named "<item>" has "val" value in xattr column in file browser

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario: User sees empty xattr value in xattr column with custom name, then add metadata and can see it
    When user of browser opens file browser for "space1" space
    And user of browser creates new xattr column with "attr" key and "test" column label in file browser table
    And user of browser enables only "test" column in columns configuration popover in file browser table
    Then user of browser sees that item named "dir1" has "—" value in xattr column in file browser

    And user of browser clicks on "Metadata" in context menu for "dir1"
    And user of browser sees that "Directory details" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "Directory details"
    And user of browser sees that item named "dir1" has "val" value in xattr column in file browser


  Scenario Outline: User successfully modifies key and value of xattr entry
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser sees xattr metadata entry with key "attr" and value "val"

    Then user of browser modifies key field by typing "aaaa" for exisiting xattr metadata entry with "attr" key
    And user of browser modifies value field by typing "bbbb" for exisiting xattr metadata entry with "aaaa" key
    And user of browser sees xattr metadata entry with key "aaaa" and value "bbbb"

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User modifies key for xattr entry and label for xattr column, that was initialized for previous entry
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<modal>"

    And user of browser creates new xattr column with "attr" key and "test" column label in file browser table

    Then user of browser modifies xattr column with "test" key by changing label to "apple" in file browser table
    And user of browser sees xattr column named "apple" in columns configuration popover in file browser table
    And user of browser does not see xattr column named "test" in columns configuration popover in file browser table

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser sees xattr column named "apple" in columns configuration popover in file browser table
    And user of browser does not see xattr column named "test" in columns configuration popover in file browser table

    And user of browser enables only "apple" column in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has "val" value in xattr column in file browser

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User deletes xattr column
    When user of browser opens file browser for "space1" space
    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<modal>"

    And user of browser creates new xattr column with "attr" key in file browser table

    And user of browser removes xattr column named "attr" in columns configuration popover in file browser table

    Then user of browser does not see xattr column named "attr" in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has no xattr column in file browser

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser does not see xattr column named "attr" in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has no xattr column in file browser

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User hides visibility for xattr column and then restores it
    When user of browser opens file browser for "space1" space
    And user of browser disables ["Size", "Modified", "Owner"] columns in columns configuration popover in file browser table

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr" and value "val"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<modal>"

    And user of browser creates new xattr column with "attr" key in file browser table

    Then user of browser disables "attr" column in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has no xattr column in file browser

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser sees that item named "<item>" has no xattr column in file browser

    And user of browser enables "attr" column in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has "val" value in xattr column in file browser

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser sees that item named "<item>" has "val" value in xattr column in file browser

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User modifies key for xattr column
    When user of browser opens file browser for "space1" space
    And user of browser disables ["Size", "Modified", "Owner"] columns in columns configuration popover in file browser table

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser adds xattr entry with key "attr1" and value "val1"
    And user of browser adds xattr entry with key "attr2" and value "val2"
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<modal>"

    And user of browser creates new xattr column with "attr1" key in file browser table
    Then user of browser modifies xattr column with "attr1" key by changing key to "attr2" in file browser table

    # Label was not modified, only key for xattr column
    And user of browser sees xattr column named "attr1" in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has "val2" value in xattr column in file browser

    And user of browser refreshes site and waits for page to load
    And user of browser opens file browser for "space1" space

    And user of browser sees xattr column named "attr1" in columns configuration popover in file browser table
    And user of browser sees that item named "<item>" has "val2" value in xattr column in file browser

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |