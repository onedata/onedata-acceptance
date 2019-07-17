Feature: Basic management of harvester in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User successfully adds user to harvester
    When user of browser1 creates "harvester1" harvester in Onezone page

    # copy invitation token
    And user of browser1 clicks on Discovery in the main menu
    And user of browser1 clicks "harvester1" on the harvesters list in the sidebar
    And user of browser1 clicks Members of "harvester1" harvester in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "harvester1" harvester members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    # join to harvester
    And user of browser2 clicks on Join to harvester button in discovery sidebar
    And user of browser2 pastes harvester invitation token into harvester token text field in discovery page
    And user of browser2 clicks Join the harvester button in discovery page

    Then user of browser2 sees that "harvester1" has appeared on the harvesters list in the sidebar

    And user of browser1 removes "harvester1" harvester in Onezone page


  Scenario: User fails to see harvester without view harvester privilege
    # join user to harvester
    When user of browser1 creates "harvester2" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester2" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester2" has appeared on the harvesters list in the sidebar

    # check view harvester privilege
    And user of browser1 clicks Members of "harvester2" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester2" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 unchecks "View harvester" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    And user of browser2 refreshes site
    And user of browser2 clicks Members of "harvester2" harvester in the sidebar
    Then user of browser2 sees Insufficient permissions alert in harvester members subpage

    And user of browser1 removes "harvester2" harvester in Onezone page


  Scenario: User successfully renames harvester with modify harvester privilege
    # join user to harvester
    When user of browser1 creates "harvester3" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester3" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester3" has appeared on the harvesters list in the sidebar

    # fail to rename harvester
    And user of browser2 clicks "harvester3" on the harvesters list in the sidebar
    And user of browser2 clicks on "Rename" button in harvester "harvester3" menu in the sidebar
    And user of browser2 types "harvester33" to rename harvester input field
    And user of browser2 confirms harvester rename using button
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check modify harvester privilege
    And user of browser1 clicks Members of "harvester3" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester3" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Modify harvester" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # rename harvester
    And user of browser2 refreshes site
    And user of browser2 clicks "harvester3" on the harvesters list in the sidebar
    And user of browser2 clicks on "Rename" button in harvester "harvester3" menu in the sidebar
    And user of browser2 types "harvester33" to rename harvester input field
    And user of browser2 confirms harvester rename using button

    And user of browser1 removes "harvester33" harvester in Onezone page


  Scenario: User successfully removes harvester with remove harvester privilege
    # join user to harvester
    When user of browser1 creates "harvester4" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester4" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester4" has appeared on the harvesters list in the sidebar

    # fail to remove harvester
    And user of browser2 clicks "harvester4" on the harvesters list in the sidebar
    And user of browser2 clicks on "Remove" button in harvester "harvester4" menu in the sidebar
    And user of browser2 clicks on "Remove" button in modal "Remove harvester"
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check remove harvester privilege
    And user of browser1 clicks Members of "harvester4" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester4" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Remove harvester" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # remove harvester
    Then user of browser2 clicks "harvester4" on the harvesters list in the sidebar
    And user of browser2 clicks on "Remove" button in harvester "harvester4" menu in the sidebar
    And user of browser2 clicks on "Remove" button in modal "Remove harvester"
    And user of browser2 sees that "harvester4" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully views privileges with view privileges privilege
    # join user to harvester
    When user of browser1 creates "harvester5" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester5" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester5" has appeared on the harvesters list in the sidebar

    # fail to view privileges
    And user of browser2 clicks Members of "harvester5" harvester in the sidebar
    And user of browser2 clicks "admin" user in "harvester5" harvester members users list
    And user of browser2 sees Insufficient permissions alert in harvester members subpage

    # check view privileges
    And user of browser1 clicks Members of "harvester5" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester5" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "View privileges" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # view privileges
    And user of browser2 refreshes site
    And user of browser2 clicks "user1" user in "harvester5" harvester members users list
    Then user of browser2 sees privileges for "user1" user in harvester members subpage

    And user of browser1 removes "harvester5" harvester in Onezone page


  Scenario: User successfully sets privileges with set privileges privilege
    # join user to harvester
    When user of browser1 creates "harvester6" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester6" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester6" has appeared on the harvesters list in the sidebar

    # fail to set privileges
    And user of browser2 clicks Members of "harvester6" harvester in the sidebar
    And user of browser2 sees "user1" user in "harvester6" harvester members users list
    And user of browser2 clicks "user1" user in "harvester6" harvester members users list
    And user of browser2 checks "Harvester management" privilege toggle for "user1" user in harvester members subpage
    And user of browser2 clicks Save button for "user1" user in harvester members subpage
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check set privileges
    And user of browser1 clicks Members of "harvester6" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester6" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Set privileges" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # set privilege
    Then user of browser2 refreshes site
    And user of browser2 clicks "user1" user in "harvester6" harvester members users list
    And user of browser2 checks "Harvester management" privilege toggle for "user1" user in harvester members subpage
    And user of browser2 clicks Save button for "user1" user in harvester members subpage

    And user of browser1 refreshes site
    And user of browser1 clicks "user1" user in "harvester6" harvester members users list
    And user of browser1 sees that "Harvester management" is checked for "user1" user in harvester members subpage

    And user of browser1 removes "harvester6" harvester in Onezone page


  Scenario: User successfully generate invitation token for user with add user privilege
    # join user to harvester
    When user of browser1 creates "harvester7" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester7" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester7" has appeared on the harvesters list in the sidebar

    # fail to generate invitation token for user
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester7" on the harvesters list in the sidebar
    And user of browser2 clicks Members of "harvester7" harvester in the sidebar
    And user of browser2 clicks on "Invite user using token" button in users list menu in "harvester7" harvester members view
    And user of browser2 sees Insufficient permissions alert in Invite user using token modal
    And user of browser2 closes "Invite using token" modal

    # check add user privilege
    And user of browser1 clicks Members of "harvester7" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester7" harvester members users list
    And user of browser1 expands "User management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Add user" privilege toggle in "User management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # generate invitation token for user
    Then user of browser2 clicks on "Invite user using token" button in users list menu in "harvester7" harvester members view
    And user of browser2 sees non-empty token in token area

    And user of browser1 removes "harvester7" harvester in Onezone page


  Scenario: User successfully removes user with remove user privilege
    # join user to harvester
    When user of browser1 creates "harvester8" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester8" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester8" has appeared on the harvesters list in the sidebar

    # fail to remove user
    And user of browser2 removes "admin" user from "harvester8" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check remove user privilege
    And user of browser1 clicks Members of "harvester8" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester8" harvester members users list
    And user of browser1 expands "User management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Remove user" privilege toggle in "User management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # remove user
    Then user of browser2 removes "admin" user from "harvester8" harvester members
    And user of browser1 sees that "harvester8" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully add group to harvester with add group privilege
    When user of browser2 creates group "group1"

    # join user to harvester
    And user of browser1 creates "harvester9" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester9" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester9" has appeared on the harvesters list in the sidebar

    # fail to add group to harvester
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester9" on the harvesters list in the sidebar
    And user of browser2 clicks Members of "harvester9" harvester in the sidebar
    And user of browser2 clicks on "Add one of your groups" button in groups list menu in "harvester9" harvester members view
    And user of browser2 chooses "group1" from dropdown in add group modal
    And user of browser2 clicks on "Add" button in modal "Choose Group"
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check add group privilege
    And user of browser1 clicks Members of "harvester9" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester9" harvester members users list
    And user of browser1 expands "Group management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Add group" privilege toggle in "Group management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # add group to harvester
    Then user of browser2 clicks on "Add one of your groups" button in groups list menu in "harvester9" harvester members view
    And user of browser2 chooses "group1" from dropdown in add group modal
    And user of browser2 clicks on "Add" button in modal "Choose Group"
    And user of browser2 sees "group1" group in "harvester9" harvester members groups list

    And user of browser1 removes "harvester9" harvester in Onezone page


  Scenario: User successfully remove group from harvester with remove group privilege
    When user of browser1 creates group "group1"

    # join user to harvester
    And user of browser1 creates "harvester10" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester10" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester10" has appeared on the harvesters list in the sidebar

    # add group to harvester
    And user of browser1 clicks Members of "harvester10" harvester in the sidebar
    Then user of browser1 clicks on "Add one of your groups" button in groups list menu in "harvester10" harvester members view
    And user of browser1 chooses "group1" from dropdown in add group modal
    And user of browser1 clicks on "Add" button in modal "Choose Group"

    # fail to remove group from harvester
    And user of browser2 removes "group1" group from "harvester10" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check remove group privilege
    And user of browser1 clicks Members of "harvester10" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester10" harvester members users list
    And user of browser1 expands "Group management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Remove group" privilege toggle in "Group management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # remove group from harvester
    And user of browser2 removes "group1" group from "harvester10" harvester members
    And user of browser2 does not see "group1" group in "harvester10" harvester members groups list

    And user of browser1 removes "harvester10" harvester in Onezone page


  Scenario: User successfully adds space with add space privilege
    When user of browser2 creates "space1" space in Onezone page

    # join user to harvester
    And user of browser1 creates "harvester11" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester11" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester11" has appeared on the harvesters list in the sidebar

    # fail to add space
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester11" on the harvesters list in the sidebar
    And user of browser2 clicks Spaces of "harvester11" harvester in the sidebar
    And user of browser2 clicks add one of your spaces button in harvester spaces page
    And user of browser2 chooses "space1" from dropdown in add space modal
    And user of browser2 clicks on "Add" button in modal "Choose Space"
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check add space privilege
    And user of browser1 clicks Members of "harvester11" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester11" harvester members users list
    And user of browser1 expands "Space management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Add space" privilege toggle in "Space management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # add space
    And user of browser2 clicks Spaces of "harvester11" harvester in the sidebar
    And user of browser2 clicks add one of your spaces button in harvester spaces page
    And user of browser2 chooses "space1" from dropdown in add space modal
    And user of browser2 clicks on "Add" button in modal "Choose Space"

    Then user of browser2 sees that "space1" has appeared on the spaces list in discovery page
    And user of browser1 removes "harvester11" harvester in Onezone page


  Scenario: User successfully removes space with remove space privilege
    When user of browser1 creates "space2" space in Onezone page
    # join user to harvester
    And user of browser1 creates "harvester12" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester12" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester12" has appeared on the harvesters list in the sidebar

    # join space to harvester
    And user of browser1 clicks Spaces of "harvester12" harvester in the sidebar
    And user of browser1 clicks add one of your spaces button in harvester spaces page
    And user of browser1 chooses "space2" from dropdown in add space modal
    And user of browser1 clicks on "Add" button in modal "Choose Space"

    # fail to remove space from harvester
    And user of browser2 clicks Spaces of "harvester12" harvester in the sidebar
    And user of browser2 removes "space2" space from harvester
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    # check remove space privilege
    And user of browser1 clicks Members of "harvester12" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester12" harvester members users list
    And user of browser1 expands "Space management" privilege for "user1" user in harvester members subpage
    And user of browser1 checks "Remove space" privilege toggle in "Space management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    # remove space
    Then user of browser2 removes "space2" space from harvester

    And user of browser1 removes "harvester12" harvester in Onezone page
    And user of browser1 leaves "space2" space in Onezone page


