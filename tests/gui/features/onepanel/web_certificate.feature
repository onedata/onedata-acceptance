Feature: Management of web certificate in Onezone GUI

  Background:
    Given user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service

  Scenario: User sees correct information in Web certificate in Onezone panel
    When user of browser clicks on "Clusters" in the main menu
    And user of browser clicks on "onezone" in clusters menu
    And user of browser clicks "Web certificate" of "onezone" in the sidebar
    Then user of browser sees that "Use Lets Encrypt" toggle is unchecked in "Web certificate" view in Onepanel
    And user of browser sees that "onezone" "zone" domain is included in "DNS names" in "Web certificate" view in Onepanel
    And user of browser sees that "Certificate path" ends with "/certs/web_cert.pem" in "Web certificate" view in Onepanel
    And user of browser sees that "Key path" ends with "/certs/web_key.pem" in "Web certificate" view in Onepanel
    And user of browser sees that "Certificate chain path" ends with "/certs/web_chain.pem" in "Web certificate" view in Onepanel
