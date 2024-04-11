Feature: Using workflows


  Scenario: All workflows from automation-examples are used in acceptance tests
    When workflows from automation-examples are gathered
    Then all gathered workflows are used in acceptance tests
