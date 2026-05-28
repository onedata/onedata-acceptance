Feature: Checks of S3 subdomain in web certificate GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User can see a certificate warning after using web certificate that does not include subdomain for OneS3
    When user1 replaces web cert for one not including OneS3 domain in "oneprovider-1" provider
    And user1 restarts oneprovider oneprovider-krakow
    And user of browser clicks on "Clusters" in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Web certificate item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    Then user of browser sees "No DNS name matching the \"s3\" subdomain." warning in DNS names section in Web certificate view in Onepanel