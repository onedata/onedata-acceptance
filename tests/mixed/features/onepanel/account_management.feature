Feature: Account management in Onepanel

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - admin2:
                password: passwddd
                user role: admin
    And opened browser with admin2 logged to "onezone panel" service


  Scenario Outline: User changes password using <client1> and he can login with new password using <client2>
    When using <client1>, admin2 changes his password to "heheszki" in "onezone" Onezone panel service
    And using <client2>, admin2 logs out from "onezone" Onezone panel service
    Then using <client2>, admin2 successfully logs in to "onezone" Onezone panel service using password "heheszki"
