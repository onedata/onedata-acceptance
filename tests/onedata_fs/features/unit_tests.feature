Feature: Runs unit tests for onedata_fs in oneclient container


  Scenario Outline: Run unit tests in oneclient container using python<python_version>
    Given onedata_fs unit tests directory in "oneclient-1" container
    When root user starts onedata_fs unit tests in "oneclient-1" container using python <python_version> and following test configuration:
            oneprovider: oneprovider-1
            space: space1
            user: user1
    Then root user fetches tests results for python <python_version> from "oneclient-1" container

    Examples:
    | python_version |
    | 3 |
