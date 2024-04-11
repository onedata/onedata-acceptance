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


  Scenario: User sees desirable files in file browser after execution of uploaded "bagit-uploader" with valid.zip
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/bagit_test_archives/valid.zip" to current dir
    And user of browser sees that item named "valid.zip" has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "bagit-uploader" workflow in "space1" space with the following initial values:
      destination-directory:
        - dir1
      input-bagit-archives:
        - valid.zip
    Then user of browser sees "Finished" status in status bar in workflow visualizer

    # Checking if Audit Logs, Time Series charts and output stores for all tasks are correct
    And user of browser sees that audit log in task "bagit-uploader-validate" in 1st parallel box in lane "validate" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Valid bagit archive
        archive: valid.zip

    And user of browser sees that content of "valid-archives" store is:
      name: valid.zip

    And user of browser clicks on "valid.zip" archive link in Store details modal for "valid-archives" store
    And user of browser sees "valid.zip" item selected in the file browser opened in new web browser tab
    And user of browser switches to the previously opened tab in the web browser
    And user of browser sees automation page in files tab in Oneprovider page
    And user of browser closes "Store details" modal

    And user of browser sees that audit log in task "bagit-uploader-unpack-data" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
      status: Successfully unpacked 5 files.
      archive: valid.zip
    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-unpack-data" in 1st parallel box in "unpack" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is greater or equal 1 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 75000 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that audit log in task "bagit-uploader-unpack-fetch" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
      status: Found  1 files to be downloaded.
      archive: valid.zip

    And user of browser sees that number of elements in the content of the "files-to-download" store details modal is 1
    And user of browser sees destination path, size and source URL information in audit log in "files-to-download" store details and they are as follow:
      source URL: https://www.google.pl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png
      size: 5969
      destination path: googlelogo_color_272x92dp.png

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-download-files" in 1st parallel box in "download-files" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is greater or equal 1 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 2500 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    # Check if 5 files has been unpacked and 1 has been fetched
    And user of browser sees that number of elements in the content of the "uploaded-files" store details modal is 6
    And user of browser sees that each element in the content of the "uploaded-files" store details modal contains one of following file names:
      - Star__-__v7__-__SegueA__-__2013_02_18.bag_meta
      - Star__-__v7__-__SegueA__-__2013_02_18.csv
      - Star__-__v7__-__SegueA__-__2013_02_18.metadata.json
      - Star__-__v7__-__SegueA__-__2013_02_18.rfm
      - ark-file-meta.csv
      - googlelogo_color_272x92dp.png

    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-calculate-checksum" in 1st parallel box in "calculate checksums" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that bytes processing speed is greater or equal 150000 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that number of elements in the content of the "calculated-checksums" store details modal is 6
    And user of browser sees that each element in the content of the "calculated-checksums" store details modal contains following information:
      checksums:
        sha256:
          status: ok
        md5:
          status: ok
    And user of browser sees that each element in the content of the "calculated-checksums" store details modal contains one of following file path:
      - Star__-__v7__-__SegueA__-__2013_02_18.bag_meta
      - Star__-__v7__-__SegueA__-__2013_02_18.csv
      - Star__-__v7__-__SegueA__-__2013_02_18.metadata.json
      - Star__-__v7__-__SegueA__-__2013_02_18.rfm
      - ark-file-meta.csv
      - googlelogo_color_272x92dp.png
    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-archive-destination" in 1st parallel box in "archive destination" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is greater or equal 1 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 55000 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"
    And user of browser clicks on "dir1" directory link in Store details modal for "destination-directory" store
    And user of browser sees "dir1" item selected in the file browser opened in new web browser tab
    And user of browser switches to the previously opened tab in the web browser

    # Checking if Dataset in file browser has correct content
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees Dataset status tag for "dir1" in file browser
    And user of browser sees that the file structure in file browser is as follow:
      - dir1:
        - Star__-__v7__-__SegueA__-__2013_02_18.bag_meta
        - Star__-__v7__-__SegueA__-__2013_02_18.csv
        - Star__-__v7__-__SegueA__-__2013_02_18.metadata.json
        - Star__-__v7__-__SegueA__-__2013_02_18.rfm
        - ark-file-meta.csv
        - googlelogo_color_272x92dp.png

    And user of browser sees that each file in "dir1" directory has following metadata:
      - checksum.sha256.expected
      - checksum.sha256.calculated
      - checksum.md5.expected
      - checksum.md5.calculated

    And user of browser sees inherited status tag for "googlelogo_color_272x92dp.png" in file browser
    And user of browser clicks on inherited status tag for "googlelogo_color_272x92dp.png" in file browser
    And user of browser sees Dataset status tag for "googlelogo_color_272x92dp.png" in file browser


  Scenario Outline: User sees desirable xrootd file in file browser after execution of uploaded "bagit-uploader" with <xrootd_archive>
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload archive "automation/bagit_test_archives/<xrootd_archive>" to current dir
    And user of browser sees that item named <xrootd_archive> has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "bagit-uploader" workflow
    And user of browser chooses "dir1" file as initial value of "destination-directory" store for workflow in "Select files" modal
    And user of browser chooses <xrootd_archive> file as initial value of "input-bagit-archives" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish

    And user of browser clicks on first executed workflow
    Then user of browser sees "Finished" status in status bar in workflow visualizer

    # Check if 0 files has been unpacked and 1 has been fetched
    And user of browser sees that audit log in task "bagit-uploader-unpack-data" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Successfully unpacked 0 files.
        archive: <xrootd_archive>
    And user of browser sees that audit log in task "bagit-uploader-unpack-fetch" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Found  1 files to be downloaded.
        archive: <xrootd_archive>

    And user of browser sees that number of elements in the content of the "uploaded-files" store details modal is 1
    And user of browser sees that element in the content of the "uploaded-files" store details modal contains following file names:
      - LHC10c_pp_ESD_120076.json
    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-download-files" in 1st parallel box in "download-files" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is greater or equal 1 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 135000 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that number of elements in the content of the "files-to-download" store details modal is 1
    And user of browser sees that element in the content of the "files-to-download" store details modal contains following destination path:
      - LHC10c_pp_ESD_120076.json
    And user of browser closes "Store details" modal

    # Checking if Dataset in file browser has correct content
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees Dataset status tag for "dir1" in file browser
    And user of browser sees that the file structure in file browser is as follow:
      - dir1:
        - data:
          - LHC10c_pp_ESD_120076.json

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks and presses enter on item named "data" in file browser
    And user of browser sees inherited status tag for "LHC10c_pp_ESD_120076.json" in file browser
    And user of browser clicks on inherited status tag for "LHC10c_pp_ESD_120076.json" in file browser
    And user of browser sees Dataset status tag for "LHC10c_pp_ESD_120076.json" in file browser


    Examples:
      | xrootd_archive                   |
      | "valid_with_xrootd.zip"          |
      | "bagit_archive_fetch_xrootd.zip" |


  Scenario Outline: User sees desirable exception in task audit log after executing bagit-uploader with invalid archive - <input_archive>
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
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload archive "automation/bagit_test_archives/<input_archive>" to current dir
    And user of browser sees that item named <input_archive> has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "bagit-uploader" workflow
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
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is equal 0 per second on chart with processing stats
    And user of browser sees that bytes processing speed is equal 0 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that audit log in task "bagit-uploader-unpack-fetch" in 1st parallel box in lane "unpack" doesn't contain user's entry

    And user of browser sees that number of elements in the content of the "files-to-download" store details modal is 0
    And user of browser closes "Store details" modal
    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-download-files" in 1st parallel box in "download-files" lane
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that files processing speed is equal 0 per second on chart with processing stats
    And user of browser sees that bytes processing speed is equal 0 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-calculate-checksum" in 1st parallel box in "calculate checksums" lane
    And user of browser sees "There is no data to show." message on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"
    And user of browser sees that number of elements in the content of the "calculated-checksums" store details modal is 0
    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-archive-destination" in 1st parallel box in "archive destination" lane
    And user of browser sees that time in right corner of chart with processing stats is around actual time
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


  Scenario: User sees desirable exception in task audit log after executing bagit-uploader with invalid archive - wrong_manifest_checksum.zip
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/bagit_test_archives/wrong_manifest_checksum.zip" to current dir
    And user of browser sees that item named "wrong_manifest_checksum.zip" has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "bagit-uploader" workflow in "space1" space with the following initial values:
      destination-directory:
        - dir1
      input-bagit-archives:
        - wrong_manifest_checksum.zip

    Then user of browser sees "Failed" status in status bar in workflow visualizer
    And user of browser sees that status of "validate" lane in "bagit-uploader" is "Finished"
    And user of browser sees that status of "unpack" lane in "bagit-uploader" is "Finished"
    And user of browser sees that status of "download-files" lane in "bagit-uploader" is "Finished"
    And user of browser sees that status of "register metadata" lane in "bagit-uploader" is "Finished"


    And user of browser sees that status of "calculate checksums" lane in "bagit-uploader" is "Failed"
    And user of browser sees that status of task "bagit-uploader-calculate-checksum" in 1st parallel box in "calculate checksums" lane is "Failed"
    And user of browser sees that audit log in task "bagit-uploader-calculate-checksum" in 1st parallel box in lane "calculate checksums" contains following entry:
      timestamp: today
      source: system
      severity: Error
      content:
        details:
          reason: Expected file checksum c953ba35heh32b2de76f59640433bc70, when calculated checksum is c953ba35ed132b2de76f59640433bc70
        description: Lambda exception occurred during item processing.


  Scenario: User sees desirable exception in task audit log after executing bagit-uploader with invalid archive - wrong_fetch.zip
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/bagit_test_archives/wrong_fetch.zip" to current dir
    And user of browser sees that item named "wrong_fetch.zip" has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "bagit-uploader" workflow in "space1" space with the following initial values:
      destination-directory:
        - dir1
      input-bagit-archives:
        - wrong_fetch.zip

    Then user of browser sees "Failed" status in status bar in workflow visualizer
    And user of browser sees that status of "validate" lane in "bagit-uploader" is "Finished"
    And user of browser sees that status of "unpack" lane in "bagit-uploader" is "Finished"

    And user of browser sees that status of "download-files" lane in "bagit-uploader" is "Failed"
    And user of browser sees that status of task "bagit-uploader-download-files" in 1st parallel box in "download-files" lane is "Failed"
    And user of browser sees that audit log in task "bagit-uploader-download-files" in 1st parallel box in lane "download-files" contains following entry:
      timestamp: today
      source: system
      severity: Error
      content:
        details:
          reason: $(contains ["HTTPSConnectionPool(host='www.heh.xd', port=443)", "Max retries exceeded with url", "Caused by NewConnectionError", "Failed to establish a new connection", "[Errno -2] Name or service not known"])
        description: Lambda exception occurred during item processing.


  Scenario: User sees successful execution of uploaded "bagit-uploader" workflow and input file bagit_archive_unpack.tar
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload archive "automation/bagit_test_archives/bagit_archive_unpack.tar" to current dir
    And user of browser sees that item named "bagit_archive_unpack.tar" has appeared in file browser
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "bagit-uploader" workflow
    And user of browser chooses "bagit_archive_unpack.tar" file as initial value of "input-bagit-archives" store for workflow in "Select files" modal
    And user of browser chooses "dir1" file as initial value of "destination-directory" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits extended time for all workflows to finish
    And user of browser clicks on first executed workflow

    Then user of browser sees "Finished" status in status bar in workflow visualizer

    And user of browser sees that audit log in task "bagit-uploader-unpack-data" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Successfully unpacked 64 files.
        archive: "bagit_archive_unpack.tar"
    And user of browser sees that audit log in task "bagit-uploader-unpack-fetch" in 1st parallel box in lane "unpack" contains following entry:
      timestamp: today
      source: user
      severity: info
      content:
        status: Found  0 files to be downloaded.
        archive: "bagit_archive_unpack.tar"

    And user of browser sees that number of elements in the content of the "uploaded-files" store details modal is 21
    And user of browser closes "Store details" modal

    And user of browser sees chart with processing stats after opening "Time series" link for task "bagit-uploader-unpack-data" in 1st parallel box in "unpack" lane
    And user of browser changes time resolution to "1 min" in modal "Task time series"
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that bytes processing speed is greater or equal 13500 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that number of elements in the content of the "files-to-download" store details modal is 0
    And user of browser closes "Store details" modal

    # Checking if Dataset in file browser has correct content
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees Dataset status tag for "dir1" in file browser

    # TODO: VFS-11706 uncomment after implementing function which checks file
    #  structure and  recognize dirs with names not starting with "dir" prefix
#    And user of browser sees that the file structure in file browser is as follow:
#      - dir1:
#        - mid-covid6:
#          - data_objects: 41
#          - studies: 23

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees inherited status tag for "mid-covid6" in file browser
    And user of browser clicks on inherited status tag for "mid-covid6" in file browser
    And user of browser sees Dataset status tag for "mid-covid6" in file browser

    # TODO: VFS-11705 implement test for following archives after workflow fix
    # bagit_archive_5gbfile.zip
    # bagit_archive_fetch.zip
    # bagit_archive_unpack_and_fetch.zip
