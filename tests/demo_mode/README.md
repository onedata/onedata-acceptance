# Demo-mode acceptance tests

Acceptance tests for the commands and examples used to start Onezone and
Oneprovider in demo mode. The tests run the example commands against real Docker
containers and verify the resulting configuration, REST access, data transfer,
and persistence.


# Development

Please read this document before writing or modifying demo-mode tests.

The shell commands under [commands](commands) are the examples exercised by the
tests. They are loaded verbatim, with only `xRELEASExVERSIONx` replaced by the
release supplied on the command line. Keep these commands suitable for use as
standalone examples.

The original documentation used `docker run -it`. The `-t` option, which
allocates a pseudo-TTY, was intentionally removed because no terminal is
available when the commands run in automated tests. The examples retain `-i`
where standard input must remain open. Do not restore `-t` unless the test
execution model is changed to provide a TTY.

The test code is divided into:

* [scenarios](scenarios) - pytest scenarios and their high-level assertions,
* [steps](steps) - individual test operations and assertions,
* [meta_steps](meta_steps) - reusable sequences of steps,
* [utils](utils) - Docker command, REST, logging, and persistence helpers.


# Prerequisites

* Docker with access to `/var/run/docker.sock`,
* access to the `onedata/onezone` and `onedata/oneprovider` images for the
  selected release,
* enough free space under `/tmp` for the persistence scenario.

The recommended Makefile target runs pytest in the repository's acceptance-test
image, so no local Python environment is required.


# Running tests using Makefile

Run the complete demo-mode suite from the repository root:

```bash
make test_demo_mode RELEASE=25.1
```

`RELEASE` is required and is used as the tag for both demo-mode service images.

To run one scenario, pass its file name without the `.py` extension:

```bash
make test_demo_mode RELEASE=25.1 SCENARIO=test_python_access
```

Unlike the GUI, mixed, and Oneclient suites, demo-mode tests do not use an
`ENV_FILE` or `test_run.py`. Each scenario starts the required Onezone and
Oneprovider containers directly.


# Running tests directly (advanced)

When the repository's Python test dependencies are installed locally, the suite
can be invoked with pytest:

```bash
python3 -m pytest --confcutdir=tests/demo_mode -rs -s -v \
    tests/demo_mode/scenarios --release=25.1
```

To run a single scenario:

```bash
python3 -m pytest --confcutdir=tests/demo_mode -rs -s -v \
    tests/demo_mode/scenarios/test_run_in_foreground.py --release=25.1
```


# Covered scenarios

* foreground and detached demo-mode startup,
* a distributed environment with two Oneproviders,
* state preservation across container restarts,
* Python access through `fs.onedatarestfs`,
* the comprehensive Docker and REST example.


# Cleanup and fixed names

The tests use the fixed container names `oz_test`, `op_test1`, and `op_test2`.
These containers are removed before and after every scenario, so do not use the
same names for containers that must remain running.

The persistence scenario uses `/tmp/oz-pers`, `/tmp/op-pers`, and
`/tmp/op-storage`. Cleanup removes these directories only when their test-owned
marker is present; the test fails instead of removing unrecognized paths.
