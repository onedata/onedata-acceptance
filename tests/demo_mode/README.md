# Demo-mode acceptance tests

Acceptance tests for the commands and examples used to start Onezone and
Oneprovider in demo mode. The tests run the example commands against real Docker
containers and verify the resulting configuration, REST access, data transfer,
and persistence.


# Development

Please read this document before writing or modifying demo-mode tests.


## Tutorial commands

The commands are based on the
[demo-mode admin guide](https://onedata.org/docs/25/admin-guide/demo-mode/).
The shell commands under [commands](commands), except those in
[test_only](commands/test_only), are the examples exercised by the tests. They
are loaded verbatim, with only `xRELEASExVERSIONx` replaced by the release
supplied on the command line. Keep these commands suitable for use as standalone
examples. The `test_only` directory contains supporting commands that are not
part of the tutorial.


## Docker terminal options

The original documentation used `docker run -it`. The `-t` option, which
allocates a pseudo-TTY, was intentionally removed because no terminal is
available when the commands run in automated tests. The examples retain `-i`
where standard input must remain open. Do not restore `-t` unless the test
execution model is changed to provide a TTY.


## Code organization

The test code is divided into:

* [scenarios](scenarios) - pytest scenarios and their high-level assertions,
* [steps](steps) - individual test operations and assertions,
* [meta_steps](meta_steps) - reusable sequences of steps,
* [utils](utils) - Docker command, REST, logging, and persistence helpers.


## Steps and meta steps

A step represents one logical test operation and must not import or call meta
steps. A meta step combines at least two steps; it may call both steps and other
meta steps. Accordingly, `meta_steps` modules may import `steps` modules, but
`steps` modules must never import `meta_steps`. Supporting functions that are
neither steps nor meta steps belong in `utils`.


# Prerequisites

* Docker with access to `/var/run/docker.sock`,
* access to the `onedata/onezone` and `onedata/oneprovider` images for the
  selected release,
* enough free space under `/tmp` for the persistence scenario.

The recommended Makefile target runs pytest in the repository's acceptance-test
image, so no local Python environment is required.


# Running tests using Makefile


## Complete suite

Run the complete demo-mode suite from the repository root:

```bash
make test_demo_mode RELEASE=25.1
```

`RELEASE` is required and is used as the tag for both demo-mode service images.


## Single scenario

To run one scenario, pass its file name without the `.py` extension:

```bash
make test_demo_mode RELEASE=25.1 SCENARIO=test_python_access
```


## Docker API compatibility

The Docker client in the acceptance-test image communicates with the host
Docker daemon through `/var/run/docker.sock`. Normally, Docker negotiates a
compatible API version automatically. If the client is newer than the daemon
and negotiation fails, set `DOCKER_API_VERSION` to the maximum API version
supported by the daemon:

```bash
make test_demo_mode RELEASE=25.1 DOCKER_API_VERSION=1.41
```

The demo-mode Bamboo plan supplies this override because its agents use a
daemon that supports Docker API version 1.41. Local runs can omit it and use
normal API negotiation.


## Test runner container

The Makefile target itself runs pytest in an acceptance-test runner container.
Through the mounted Docker socket, that runner starts Onezone and Oneprovider
as sibling containers on the host Docker daemon. As in the GUI, mixed, and
Oneclient test runner, the container starts as root, adds the Docker socket's
group, and switches to the invoking host user's UID and GID before replacing
itself with pytest. Consequently, logs and reports created in bind-mounted
directories belong to the local or Bamboo user and can be cleaned normally.
The switched user receives an ephemeral writable home directory inside the
runner container, so command-line tools do not try to access root's config.

`RUNNER_NAME` can optionally assign a name to the runner:

```bash
make test_demo_mode RELEASE=25.1 RUNNER_NAME=my-demo-mode-runner
```

Bamboo gives every runner a unique name based on the build result key. Its
final cleanup task uses that name to remove a runner left behind by a cancelled
or interrupted build, before removing the fixed `oz_test`, `op_test1`, and
`op_test2` service containers. Local runs do not need `RUNNER_NAME`; Docker
assigns an automatic name and `--rm` removes the runner after it exits normally.


## Command logs and artifacts

The test runner keeps printing its normal pytest and demo-mode progress to the
terminal. Output produced by each shell or Docker command is written separately
to numbered and named files. A timestamped
`tests/demo_mode/logs/report.<timestamp>` directory represents the pytest run
and contains a separate subdirectory for each test and then for each command.
For example, the first `run_onezone.sh` invocation is stored as
`python_access/run_onezone/command-001-run_onezone.log`. Repeated attempts of
the same command share its directory and retain distinct sequence numbers. The
`.sh` suffix is omitted from artifact directory and log-file names. This is
consistent with the GUI and mixed tests and keeps scenarios separate when the
complete suite is run without `SCENARIO`. The Bamboo plan publishes the report
directory as the `command-logs` artifact belonging to that job result.


## Execution model

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
