Feature: Account management in Onepanel

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      |

  Background:
    Given initial users configuration in "z1" Onezone service:
            - admin2:
                password: passwd
                user role: admin
    And opened browser with admin2 logged to "z1 zone panel" service


  Scenario Outline: User changes password using <client1> and he can login with new password using <client2>
    When using <client1>, admin2 changes his password to "heheszki" in "z1" Onezone panel service
    And using <client2>, admin2 logs out from "z1" Onezone panel service
    Then using <client2>, admin2 successfully logs in to "z1" Onezone panel service using password "heheszki"
