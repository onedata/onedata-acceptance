Important notes
===============

- Currently the highest supported version of Firefox is 46.0.x - v47 is not supported due to incompatibility
with build-in selenium Firefox driver



GUI acceptance/BDD tests
========================

GUI acceptance/BDD test can be run in few ways using ``./test_run.py``:
 1. Headless tests inside Pod on new Onedata environment
 2. Tests using existing Onedata installation or starting new preserving Onedata installation after tests 
    1. Headless tests inside Pod
    2. Non-headless tests on local machine


Headless with automatic one-env environment set up
=====================================================

Using this method, the Onedata environment will be set up automatically with OZ and OP (for details see ``environments``
dir with configurations). Setting up environment can take some time.

Example: (invoke from onedata repo root dir)
```
./test_run.py -t tests/gui -i onedata/gui_builder:latest --test-type gui --driver=Chrome
```

Used parameters:

* ``-t tests/gui`` - standard ``./test_run.py`` parameter to set the test cases path to gui tests
* ``-i onedata/gui_builder:latest`` - use Docker image with dependencied for GUI tests (i.a. Xvfb, Selenium, Firefox, Chrome)
* ``--test-type gui`` - set the test type use by core Onedata test helpers to differ from "cucumber" tests etc.
* ``--driver=<Firefox|Chrome>`` - set the browser to test in (will be launched in headless mode)
* ``--self-contained-html`` - optional, if used generated report will be contained in 1 html file
* ``--firefox-logs`` - optional, if used and driver is Firefox generated report will contain console logs from browser
* ``--xvfb`` - starts xvfb, necessary if used with headless tests
* ``--xvfb-recording=<all|none|failed>`` - optional, record all or none or failed tests as movies and save them to <logdir>/movies
* ``--no-mosaic-filter`` - optional, if set videos of tests using multiple browsers will be recorded as different video for each browser (mosaic video created by default) 
* ``--keywords`` - run only tests matching given string expression (``py.test`` option)


Preserving Onedata installation after tests
=====================================================

Using this method, existing Onedata installation will be used. If there is no running Onedata installation it will be 
set up automatically. Installation is not destroyed after tests in this method.

To start Onedata installation navigate to one_env directory and run
 ```
 ./onenv up -f ../tests/gui/environments/<env_file>
 ```
Where ``env_file`` is one of the yamls describing the environment.

2.1. Headless tests in Pod
-----------------------------------------------------

Example: (invoke from onedata repo root dir)
```
./test_run.py -t tests/gui --test-type gui --driver=Chrome -i onedata/acceptance_gui:latest --no-clean
```

New parameters:

* ``--no-clean`` - prevents deleting environment after tests

2.2. Non-headless using local machine (BDD)
-----------------------------------------------------

These tests will be run using ``py.test`` runner on local machine.
Required Python packages to install (e.g. using ``pip install``) are listed
in requirement file: `tests/gui/requirements.txt`

A handy oneliner to install Python dependencies (invoke from repo root):
```
pip install -r tests/gui/requirements.txt
```

Additional applications required in system:

* xclip (Linux) or pbcopy (OSX)

A browser selected for tests (with ``--driver``) should be also installed.

Example: (invoke from onedata repo root dir)
```
./test_run.py -t tests/gui --test-type gui --driver=Chrome -i onedata/acceptance_gui:lates --local
```

New parameters:

* ``--local`` - starts tests on host instead of starting them in pod.
* ``--add-test-domain`` - when running tests on local machine option for adding entries to ``/etc/hosts`` is turned off by default. This may
cause that some test will fail. You can enable adding entries to ``/etc/hosts`` using ``-add-test-domain`` option or add entries manually.


Test reports
============

The test report in HTML format with embedded screenshots of browser in failed test will be saved to:
``<onedata_repo_root>/tests/gui/logs/report.<time_stamp>/report.html``


Taking screenshots
==================

For some purposes, taking screenshots can be required in time of test run.

In steps of scenarios simply use:
```
driver.get_screenshot_as_file('/tmp/some-screenshot.png')
```
where driver is instance of Selenium WebDriver

Development
===========

Please read these section before you start writing or modifying GUI tests.

Fixtures and pytest plugins overrides
=====================================

* The default configuration of ``pytest-selenium-multi`` for sensitive URLs is inverted:
all tests are considered *non-destructive by default*.
You can add a ``@pytest.mark.destructive`` mark to test scenario to mark test as destructive.

* The ``sensitive_url`` fixture has module scope, because we start new environment for each module
(so it could have different ``base_url's``)
