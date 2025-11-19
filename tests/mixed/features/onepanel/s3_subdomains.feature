Feature: Basic management of S3 subdomains


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User can see suitable warning after replacing web certs for ones ont including OneS3 domain
    When user1 replaces web certs for ones not including oneS3 domain in "oneprovider-1" provider
    And user1 restarts oneprovider oneprovider-krakow
    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Web certificate item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel

    Then user of browser sees "The installed certificate does not match the domain of the cluster." warning in Web certificate view in Onepanel
    And user of browser sees "No DNS name matching the "s3" subdomain." warning in DNS names section in Web certificate view in Onepanel