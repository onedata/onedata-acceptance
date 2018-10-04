Onedata Acceptance Tests
========================

This is the code repository containing acceptance tests for Onedata. It uses 
one_env for creating environment running on kubernetes. To start Onedata 
deployment navigate to one_env directory and run:

 ```
 ./onenv up -f <env_file>
 ```
 
Where:
* ``env_file`` is yaml file describing the environment
* ``-f`` is option forcing new deployment, deleting an old one if present

Important notes:
1. If you want to deploy environment with nfs storage make sure that:
- you have installed ``/sbin/mount.nfs`` helper program on node
- node's resolv.conf have to be able to resolve nfs domain name


GUI tests
===========
The whole procedure for running gui tests is described in details in the
``tests/gui/README.md`` file.

Oneclient tests
=================
To run oneclient tests use ``./test_run.py`` script. Example invoke:
```
./test_run.py -t tests/acceptance --test-type acceptance -i onedata/worker --env-file=singleprovider_singleclient_directio --no-clean
```

Where:
* ``-t`` - standard ``./test_run.py`` parameter to set the test cases path to oneclient tests
* ``--test-type acceptance`` - set the test type use by core Onedata test helpers
* ``-i onedata/worker`` - use Docker image with dependencies for oneclient tests
* ``--env-file=singleprovider_singleclient_directio`` - path to description of test environment in .yaml file
* ``--no-clean`` - ff present prevents cleaning onedata environment 

