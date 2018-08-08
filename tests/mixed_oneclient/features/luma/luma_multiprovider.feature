Feature: LUMA acceptance tests using multiple providers. This feature uses scenario-1oz-3op-luma

  Background:
    # users and luma mappings are created with environment
    # clients are mounted with environment; create mappings to structures used in tests
    Given there are mounted clients:
        client1: oneclient-krakow
        client2: oneclient-paris


  Scenario: Not owner cannot remove file
    When using client2 joe creates file "dir/file1" in space "krk-pl-par-c"
    And using client2 joe sees "dir/file1" in space "krk-pl-par-c"
    
    Then using client1 marie tries to remove "dir/file1" in space "krk-pl-par-c"
    And using client2 marie tries to remove "dir/file1" in space "krk-pl-par-c"

    And using client1 joe sees "dir/file1" in space "krk-pl-par-c"
    And using client1 joe succeeds to remove "dir/file1" in space "krk-pl-par-c"
  
    
  Scenario: User not in LUMA cannot create file
    When using client1 karen fails to create file "file2" in space "krk-pl-par-c"
    
    And using client1 joe does not see file "file2" in space "krk-pl-par-c"
    # wait to ensure synchronization between providers
    And user joe waits for 10 seconds
    And using client2 joe does not see file "file2" in space "krk-pl-par-c"


  Scenario: Imported directory is correctly mapped on provider with LUMA and is not mapped on other provider
    When using client1 joe sees "Landsat-5" in space "krk-plirw-par-c"
    Then using client1 joe sees that "Landsat-5" in space "krk-plirw-par-c" has:
        owner_name: 40001
        owner_group: 42001

    And using client1 marie sees "Landsat-5" in space "krk-plirw-par-c"
    And using client1 marie sees that "Landsat-5" in space "krk-plirw-par-c" has:
        owner_name: 40001
        owner_group: 42001

    And using client2 joe sees "Landsat-5" in space "krk-plirw-par-c"
    And using client2 joe sees that "Landsat-5" in space "krk-plirw-par-c" has not:
        owner_name: 40001
        owner_group: 42001


  Scenario: New file created on provider without LUMA is correctly mapped on storage with import
    When using client2 joe creates file "Landsat-5/file1" in space "krk-plirw-par-c"

    Then using client1 joe sees that "Landsat-5/file1" in space "krk-plirw-par-c" has:
        owner_name: 40001
        owner_group: 42001

    And using client2 joe sees that "Landsat-5/file1" in space "krk-plirw-par-c" has not:
        owner_name: 40001
        owner_group: 42001

    And using client1 joe opens "Landsat-5/file1" in space "krk-plirw-par-c"
    And there is file "volume-data-sync-rw-luma/Landsat-5/file1" in container "volume-data-sync-rw-luma" on provider "oneprovider-1"
    And file "volume-data-sync-rw-luma/Landsat-5/file1" in container "volume-data-sync-rw-luma" on provider "oneprovider-1" has:
        owner_name: 40001
        owner_group: 42001
