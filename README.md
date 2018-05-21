# Onedata Acceptance Tests

This is the code repository containing acceptance tests for Onedata. It uses 
one_env for creating environment running on kubernetes. To start Onedata 
deployment navigate to one_env directory and run:

 ```
 ./onenv up -f <env_file>
 ```
 
Where:
* ``env_file`` is yaml file describing the environment
* ``-f`` is option forcing new deployment, deleting an old one if present

# GUI tests
The whole procedure for running gui tests is described in details in the
``tests/gui/README.md`` file.