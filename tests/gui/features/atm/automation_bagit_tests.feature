Feature: Bagit uploader tests


  Background:
    Given initial users configuration in "onezone" Onezone service:
          - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: s3
                    size: 10000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1

    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory


  Scenario Outline: User sees desirable exception in task audit log after executing BagIt Uploader with invalid archive - <input_archive>
    Given possible exception messages appearing for workflow files:
      - "invalid_bagit_txt.tgz":
        - "Invalid 'Tag-File-Character-Encoding' definition in 1st line in bagit.txt"
      - "unsupported_url.zip":
        - "URL from line number 1 in fetch.txt is not supported"
      - "unsupported_archive_type.7z":
        - "Unsupported archive type: .7z"
      - "missing_manifest_file.tgz":
        - "No manifest file found"
      - "missing_data_dir.tar":
        - "Payload directory not found"
      - "missing_bagit_txt.tar":
        - "Bagit directory not found"
      - "invalid_fetch_url.zip":
        - "File path not within data/ directory (fetch.txt line 1)"
      - "missing_fetch_txt.zip":
        - "bagit_missing_fetch_txt/fetch.txt referenced by bagit_missing_fetch_txt/tagmanifest-md5.txt not found"
        - "bagit_missing_fetch_txt/fetch.txt referenced by bagit_missing_fetch_txt/tagmanifest-sha256.txt not found"
      - "wrong_tagmanifest_checksums.zip":
        - "md5 checksum verification failed for macaroon_bag1/fetch.txt.\nExpected:
           5e8594d60bc90071ae12ad9b589166be, Calculated: ceb502eb82f571ea033f743f3c3c9123"
        - "sha256 checksum verification failed for macaroon_bag1/fetch.txt.\nExpected:
           a4127b2d0ced5571d738917292cb64ae686bea0c016d18a66029062b43dbd7eb, Calculated: 8db8b25444ca1130c2150fe622df8aac8e5604332cd0ec84e80adb9ce90240ab"
      - "missing_payload.zip":
        - "Files referenced by macaroon_bag1/manifest-md5.txt do not match with payload files.\n  Files
           in payload but not referenced: set()\n  Files
           referenced but not in payload: {'data/ark-file-meta.csv'}"
        - "Files referenced by macaroon_bag1/manifest-sha256.txt do not match with payload files.\n  Files
           in payload but not referenced: set()\n  Files
           referenced but not in payload: {'data/ark-file-meta.csv'}"
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload archive "automation/bagit_test_archives/<input_archive>" to current dir
    And user of browser sees that item named <input_archive> has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "BagIt Uploader" workflow
    And user of browser chooses "dir1" file as initial value of "destination-directory" store for workflow in "Select files" modal
    And user of browser chooses <input_archive> file as initial value of "input-bagit-archives" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish

    And user of browser clicks on first executed workflow
    Then user of browser sees that audit log in task "bagit-uploader-validate" in 1st parallel box in lane "validate" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Invalid bagit archive

    And user of browser sees that "archive" content of audit log in task "bagit-uploader-validate" in 1st parallel box in lane "validate" is <input_archive>
    And user of browser sees expected exception for <input_archive> in "reason" content of audit log in task "bagit-uploader-validate" in 1st parallel box in lane "validate"

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-unpack-data" in 1st parallel box in "unpack" lane
    And user of browser sees that time in right corner of chart with processing stats is around current time
    And user of browser sees that files processing speed is equal 0 per second on chart with processing stats
    And user of browser sees that bytes processing speed is equal 0 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that audit log in task "bagit-uploader-unpack-fetch" in 1st parallel box in lane "unpack" doesn't contain user's entry

    And user of browser sees that number of elements in the content of the "files-to-download" store details modal is 0
    And user of browser closes "Store details" modal
    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-download-files" in 1st parallel box in "download-files" lane
    And user of browser sees that time in right corner of chart with processing stats is around current time
    And user of browser sees that files processing speed is equal 0 per second on chart with processing stats
    And user of browser sees that bytes processing speed is equal 0 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-calculate-checksum" in 1st parallel box in "calculate checksums" lane
    And user of browser sees "There is no data to show." message on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"
    And user of browser sees that number of elements in the content of the "calculated-checksums" store details modal is 0
    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-archive-destination" in 1st parallel box in "archive destination" lane
    And user of browser sees that time in right corner of chart with processing stats is around current time
    And user of browser sees that files processing speed is equal 0 per second on chart with processing stats
    And user of browser sees that bytes processing speed is equal 0 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"


    Examples:
        | input_archive                     |
        | "invalid_bagit_txt.tgz"           |
        | "unsupported_url.zip"             |
        | "unsupported_archive_type.7z"     |
        | "missing_manifest_file.tgz"       |
        | "missing_data_dir.tar"            |
        | "missing_bagit_txt.tar"           |
        | "invalid_fetch_url.zip"           |
        | "missing_fetch_txt.zip"           |
        | "wrong_tagmanifest_checksums.zip" |
        | "missing_payload.zip"             |
