Feature: Management of invite tokens with caveats in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
          - user2
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: admin
          space2:
            owner: user1
          space3:
            owner: admin

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2
          group3:
            owner: admin
          group4:
            owner: admin

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User sees expiration and region allow caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            expiration:
              after: 10
            region:
              allow: True
              region codes:
                - Europe
                - Asia
            country:
              allow: True
              country codes:
                - PL
                - BS
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Asia
                - Europe
            country:
              allow: True
              country codes:
                - PL
                - BS

    And user of browser1 removes all tokens


  Scenario: User sees IP and region deny caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            region:
              allow: False
              region codes:
                - Europe
                - Asia
            IP:
              - 192.0.2.1
              - 192.0.2.0/24
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            region:
              allow: False
              region codes:
                - Asia
                - Europe
            IP:
              - 192.0.2.1/32
              - 192.0.2.0/24

    And user of browser1 removes all tokens


  Scenario: User sees ASN and country allow caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            country:
              allow: True
              country codes:
                - PL
                - BS
            ASN:
              - 64496
              - 64498
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            country:
              allow: True
              country codes:
                - PL
                - BS
            ASN:
              - 64496
              - 64498

    And user of browser1 removes all tokens


  Scenario: User sees all token caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            expiration:
              after: 10
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: True
              country codes:
                - BS
            ASN:
              - 64496
            IP:
              - 192.0.2.1
            consumer:
              - type: user
                by: id
                consumer name: user1
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: True
              country codes:
                - BS
            ASN:
              - 64496
            IP:
              - 192.0.2.1/32
            consumer:
              - type: user
                by: name
                consumer name: user1

    And user of browser1 removes all tokens


