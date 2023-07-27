Feature: Basic management of space marketplace privileges for users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user1
    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


 Scenario: User sees space, of which he is a member, in the Marketplace after
 getting Manage in Marketplace privileges and configuring it
   When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
   And user of space_owner_browser clicks "user1" user in "space1" space members users list
   And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
        Space management:
           granted: Partially
           privilege subtypes:
             View space: True
             Modify space: False
             Manage in Marketplace: False
   And user of browser_user1 clicks "Configuration" of "space1" space in the sidebar
   And user of browser_user1 sees "READ-ONLY" header label in configuration space
   And user of browers_user1 sees "Insufficient privileges" message after hovering on "Advertise in Marketplace" toggle
   And user of space_owner_browser clicks "user1" user in "space1" space members users list
   And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
        Space management:
           granted: Partially
           privilege subtypes:
             View space: True
             Modify space: True
             Manage in Marketplace: True
   And user of browser_user1 clicks "Configuration" of "space1" space in the sidebar
   And user of browser_user1 changes organization name for "org_name1" in space configuration subpage
   And user of browser_user1 sets organization description "some desc" in space configuration subpage
   And user of browser_user1 checks "Advertise in Marketplace" toggle on space configuration page
   And user of browser_user1 writes "example@gmail.com" into contact email text field in modal "Advertise space in the Marketplace"
   And user of browser_user1 accepts terms of privacy in Space Marketplace using checkbox in modal "Advertise space in the Marketplace"
   And user of browser_user1 clicks on "Proceed" button in modal "Advertise space in the Marketplace"
   And user of browser_user1 sees that "Advertise in Marketplace" toggle is checked on space configuration page
   Then user of browser_user1 sees "example@gmail.com" in marketplace contact e-mail address text field
   Then user of browser_user1 sees that "space1" space is advertised in the marketplace in space sidebar
   And user of browser_user1 clicks "View in Marketplace" link on space configuration page
   Then user of browser_user1 sees advertised space on Space Marketplace subpage with following parameters:
        space name: "space1"
        organization name: "org_name1"
        creation time: current
        description: "some desc"
