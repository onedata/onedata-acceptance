Feature: LUMA acceptance tests using multiple providers

  Scenario: User cannot remove file using client if he is not its owner
    Given oneclients [client11, client12, client21, client22]
      mounted in [/home/rob/onedata, /home/marie/onedata, /home/rob/onedata, /home/marie/onedata]
      on client_hosts [oneclient-1, oneclient-1, oneclient-2, oneclient-2] respectively,
      using [token, token, token, token] by [rob, marie, rob, marie]

    When rob creates directories [krk-pl-par-c/dir1] on client21
    And rob creates regular files [krk-pl-par-c/dir1/file1] on client21
    And rob sees [file1] in krk-pl-par-c/dir1 on client21
    And rob changes krk-pl-par-c/dir1/file1 mode to 644 on client21

    Then marie fails to delete files [krk-pl-par-c/dir1/file] on client12
    And marie fails to delete files [krk-pl-par-c/dir1/file] on client22

    And rob sees [file1] in krk-pl-par-c/dir1 on client11


  Scenario: User not in LUMA cannot create file
    Given oneclients [client11, client12, client21]
      mounted in [/home/rob/onedata, /home/karen/onedata, /home/rob/onedata]
      on client_hosts [oneclient-1, oneclient-1, oneclient-2] respectively,
      using [token, token, token] by [rob, karen, rob]
    Then karen fails to create regular files [krk-pl-par-c/file2] on client12
    And rob can't stat [file2] in krk-pl-par-c on client11
    # wait to ensure synchronization between providers
    And rob waits 10 seconds
    And rob can't stat [file2] in krk-pl-par-c on client21


  Scenario: Imported directory ownership is correctly mapped on provider with LUMA and is not mapped on other provider
    Given oneclients [client11, client12, client21]
      mounted in [/home/rob/onedata, /home/marie/onedata, /home/rob/onedata]
      on client_hosts [oneclient-1, oneclient-1, oneclient-2] respectively,
      using [token, token, token] by [rob, marie, rob]
    # storage with files is created with environment
    # space "krk-plirw-par-c" is supported with import by this storage
    When rob creates directories [krk-plirw-par-c/Landsat-5] on client11
    # wait to ensure synchronization between providers
    And rob waits 10 seconds
    And rob sees [Landsat-5] in krk-plirw-par-c on client11
    Then rob sees that owner's uid and gid for krk-plirw-par-c/Landsat-5 are equal to 40001 and 42001 on client11

    And marie sees [Landsat-5] in krk-plirw-par-c on client12
    And marie sees that owner's uid and gid for krk-plirw-par-c/Landsat-5 are equal to 40001 and 42001 on client12

    And rob sees [Landsat-5] in krk-plirw-par-c on client21
    And rob sees that owner's uid and gid for krk-plirw-par-c/Landsat-5 are not equal to 40001 and 42001 on client21


  Scenario: Ownership of new file created on provider without LUMA is correctly mapped on storage with import
    Given oneclients [client11, client21]
      mounted in [/home/rob/onedata, /home/rob/onedata]
      on client_hosts [oneclient-1, oneclient-2] respectively,
      using [token, token] by [rob, rob]
    When rob creates directories [krk-plirw-par-c/Landsat-5] on client21
    # wait to ensure synchronization between providers
    And rob waits 10 seconds
    And rob creates regular files [krk-plirw-par-c/Landsat-5/file1] on client21

    Then rob sees [file1] in krk-plirw-par-c/Landsat-5 on client11
    And rob sees that owner's uid and gid for krk-plirw-par-c/Landsat-5/file1 are equal to 40001 and 42001 on client11
    And rob sees that owner's uid and gid for krk-plirw-par-c/Landsat-5/file1 are not equal to 40001 and 42001 on client21

    And rob opens krk-plirw-par-c/Landsat-5/file1 with mode r on client11
    And there is file "volume-data-sync-rw-luma/Landsat-5/file1" in container "volume-data-sync-rw-luma" on provider "oneprovider-1"
    And file "volume-data-sync-rw-luma/Landsat-5/file1" in container "volume-data-sync-rw-luma" on provider "oneprovider-1" has owner's uid and gid equal to 40001 and 42001
