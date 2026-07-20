Feature: Basic management of emergency Onezone panel


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


    And users opened [browser] browsers' windows
    And users of [browser] opened [Onezone panel] page
    And user of [browser] logged as [user1] to [emergency interface of Onezone] service


  Scenario: User sees correct information in overview in Onezone emergency panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser can see tabs "[Data, Shares, Providers, Groups, Tokens, Discovery, Automation]" are disabled in the main menu
    And user of browser clicks Overview of "onezone" in the sidebar
    Then user of browser sees Name is "dev-onezone" in info tile in overview view in Onepanel
    And user of browser sees Type is "Onezone" in info tile in overview view in Onepanel
    And user of browser sees Domain is "dev-onezone.default.svc.cluster.local" in info tile in overview view in Onepanel
    And user of browser sees Cluster ID is "onezone" in info tile in overview view in Onepanel


  Scenario: User sees correct information in Nodes in Onezone emergency panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser clicks Nodes of "onezone" in the sidebar
    Then user of browser sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options are enabled for .*onezone.* host in Nodes page in Onepanel
    And user of browser sees that [Database, Cluster Worker, Cluster Manager, Primary Cluster Manager] options cannot be changed for .*onezone.* host in Nodes page in Onepanel


  Scenario: User sees correct information in Web certificate in Onezone emergency panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser clicks Web certificate of "onezone" in the sidebar
    Then user of browser sees that "Use Lets Encrypt" toggle is unchecked in Web certificate view in Onepanel
    And user of browser sees that onezone zone domain is included in "DNS names" in Web certificate view in Onepanel
    And user of browser sees that "Certificate path" ends with "/certs/web_cert.pem" in Web certificate view in Onepanel
    And user of browser sees that "Key path" ends with "/certs/web_key.pem" in Web certificate view in Onepanel
    And user of browser sees that "Certificate chain path" ends with "/certs/web_chain.pem" in Web certificate view in Onepanel


  Scenario: User sees correct information in members in Onezone emergency panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser clicks Members of "onezone" in the sidebar
    Then user of browser sees 0 direct groups in Onezone clusters members page
    And user of browser sees 1 direct users in Onezone clusters members page
    And user of browser sees 0 effective groups in Onezone clusters members page
    And user of browser sees 1 effective users in Onezone clusters members page
    And user of browser clicks on "Open in Onezone" in Onezone clusters members page
    And user of browser logs as admin to Onezone service
    And user of browser can see Onezone clusters members page is opened


  Scenario: User correctly changes emergency passphrase in Onezone emergency panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser clicks Emergency passphrase of "onezone" in the sidebar
    And user of browser clicks on Change passphrase button on emergency passphrase page
    And user of browser types "password" to Current passphrase input field on emergency passphrase page
    And user of browser types "new_password" to New passphrase input field on emergency passphrase page
    And user of browser types "new_password" to Retype new passphrase input field on emergency passphrase page
    And user of browser clicks on Change button on emergency passphrase page
    And user of browser logs out from Onezone Emergency panel

    Then user of browser clicks Sign in to emergency interface in Onepanel login page
    And user of browser types "new_password" to Passphrase input in Onepanel login form
    And user of browser presses Sign in button in Onepanel login page
    And user of browser sees an info notify with text matching to: Authentication succeeded!

    # set previous password back
    And user of browser clicks on "Clusters" in the main menu
    And user of browser clicks Emergency passphrase of "onezone" in the sidebar
    And user of browser clicks on Change passphrase button on emergency passphrase page
    And user of browser types "new_password" to Current passphrase input field on emergency passphrase page
    And user of browser types "password" to New passphrase input field on emergency passphrase page
    And user of browser types "password" to Retype new passphrase input field on emergency passphrase page
    And user of browser clicks on Change button on emergency passphrase page


  Scenario: User sees notification on log-in page after setting sign-in notification in Onezone emergency panel
    When user of browser sets sign in notification: "test sign-in notification" in GUI settings page of "onezone"
    And user of browser logs out from Onezone Emergency panel
    And user of browser clicks open in onezone in Onepanel login page
    Then user of browser sees sign in notification message: "test sign-in notification" in the login page
    And user of browser logs as admin to Onezone service
    And user of browser removes "test sign-in notification" text from sign in notification in GUI settings page of "onezone"


  Scenario: User sees terms of use page after setting terms of use in Onezone emergency panel
    When user of browser sets terms of use: "test terms of use" in GUI settings page of "onezone"
    And user of browser logs out from Onezone Emergency panel
    And user of browser clicks open in onezone in Onepanel login page
    And user of browser logs as admin to Onezone service
    And user of browser expands account settings dropdown in the sidebar
    And user of browser goes to "Terms of use" page
    Then user of browser sees "test terms of use" on terms of use page
    And user of browser clicks "Back to main page" button on terms of use page
    And user of browser removes "test terms of use" text from terms of use in GUI settings page of "onezone"


  Scenario: User sets and sees correct information about using cookies and privacy policy terms in Onezone emergency panel
    When user of browser sets privacy policy: "test privacy policy" in GUI settings page of "onezone"
    And user of browser sets cookie consent notification: "test cookie consent" in GUI settings page of "onezone"
    And user of browser inserts privacy policy link in cookie consent notification in GUI settings page of "onezone"
    And user of browser logs out from Onezone Emergency panel
    And user of browser clicks open in onezone in Onepanel login page
    And user of browser logs as admin to Onezone service
    And user of browser clicks on "Data" in the main menu
    And user of browser clicks on privacy policy link in cookies popup
    Then user of browser sees "test privacy policy" on privacy policy page
    And user of browser clicks "I understand" button in cookies popup
    And user of browser clicks "Back to main page" button on privacy policy page
    And user of browser removes "test privacy policy" text from privacy policy in GUI settings page of "onezone"
    And user of browser removes "test cookie consent" text from cookie consent notification in GUI settings page of "onezone"