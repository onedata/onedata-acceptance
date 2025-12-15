Feature: File events checking

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                    - dir2:

    And opened browser with user1 signed in to "onezone" service


  Scenario: User can see suitable file events after creating, editing and deleting a file
    When user user1 starts observing file events on "[name, mtime, size]" on dir "dir1" in space "space1" in oneprovider-2
    And using REST, user1 succeeds to create file named "dir1/file1" in "space1" in oneprovider-1
    Then user user1 can see new file event about "dir1/file1" in space "space1" in oneprovider-2
    And using REST, user1 renames item named "dir1/file1" to "dir1/file2" in "space1" in oneprovider-1
    And user user1 can see following changed_or_created file events of "dir1/file2" in space "space1" in oneprovider-2:
        - name: file2
    And using REST, user1 writes "TEST TEXT ONEDATA" to file named "dir1/file2" in "space1" in oneprovider-1
    And user user1 can see following changed_or_created file events of "dir1/file2" in space "space1" in oneprovider-2:
        - size: 17
        - mtime
    And using REST, user1 succeeds to remove file named "dir1/file2" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And user user1 can see deleted file event about "dir1/file2" in space "space1" in oneprovider-2


  Scenario: User can see correct file events after reconnecting to SSE Stream
    When user user1 starts observing file events on "[name, mtime, size]" on dir "dir1" in space "space1" in oneprovider-2
    And using REST, user1 succeeds to create file named "dir1/file1" in "space1" in oneprovider-1
    And user user1 can see new file event about "dir1/file1" in space "space1" in oneprovider-2
    And using REST, user1 writes "TEST TEXT ONEDATA" to file named "dir1/file1" in "space1" in oneprovider-1
    And user user1 can see following changed_or_created file events of "dir1/file1" in space "space1" in oneprovider-2:
        - size: 17
        - mtime
    And using REST, user1 succeeds to create file named "dir1/file2" in "space1" in oneprovider-1
    And user user1 can see new file event about "dir1/file2" in space "space1" in oneprovider-2
    And using REST, user1 writes "TEST TEXT ONEDATA 2" to file named "dir1/file2" in "space1" in oneprovider-1
    And user user1 can see following changed_or_created file events of "dir1/file2" in space "space1" in oneprovider-2:
        - size: 19
        - mtime
    And user user1 disconnects from SSE Stream
    And user user1 reconnects to SSE Stream starting from first captured event id
    Then user user1 can see following changed_or_created file events of "dir1/file1" in space "space1" in oneprovider-2:
        - size: 17
        - mtime
    And user user1 can see following changed_or_created file events of "dir1/file2" in space "space1" in oneprovider-2:
        - size: 19
        - mtime


  Scenario: User can see heartbeat event, while modifying not observed dir
    When user user1 starts observing file events on "[name, mtime, size]" on dir "dir1" in space "space1" in oneprovider-2
    And using REST, user1 creates 50 empty files in "space1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    Then user user1 can see that the heartbeat event has just arrived in oneprovider-2
    And using REST, user1 creates 50 empty files in "space1/dir2" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And user user1 can see that the heartbeat event has just arrived in oneprovider-2