# Demo-mode acceptance tests

This suite runs the commands published in the
[demo-mode admin guide](https://onedata.org/docs/25/admin-guide/demo-mode/) and
checks the resulting Onezone and Oneprovider services through their REST APIs.

It covers foreground and detached startup, a two-provider environment,
persistent state, Python access through `fs.onedatarestfs`, and the complete
Docker/REST example.

## Quick start

Docker must be available through `/var/run/docker.sock`, and the selected
Onezone and Oneprovider images must be accessible locally or from their image
registry.

Run the complete suite from the repository root:

```bash
make test_demo_mode RELEASE=25.1
```

Run one scenario by passing its filename without `.py`:

```bash
make test_demo_mode RELEASE=25.1 SCENARIO=test_python_access
```

When running directly in a prepared Python environment:

```bash
python3 -m pytest --confcutdir=tests/demo_mode -rs -s -v \
    tests/demo_mode/scenarios --release=25.1
```

## Adding or changing a scenario

1. Put the tutorial command in [commands](commands). Keep it usable as a
   standalone example. Use `xRELEASExVERSIONx` and `xCONTAINERxNAMEx` where the
   test must supply those values.
2. Register its `CommandTemplate` in `utils/commands.py` and expose it through
   `DemoCommands`. No other module should contain command paths or instantiate
   templates.
3. Add an operation to `steps` if the scenario needs a reusable external
   action. A step may run a command, wait for a service, or perform a REST
   request; a plain equality assertion is not a step.
4. Compose operations in `meta_steps` when the sequence is reused, then keep
   the scenario focused on the behavior being verified.

For example, command scripts are bound centrally and only the resulting
`Command` is executable:

```python
command = demo_commands.foreground_oneprovider(provider.container)
process = command.start()
```

REST calls use clients that retain their service and access token:

```python
provider = OneproviderRestClient(service, access_token)
provider.upload(space_id=space_id, file_name=file_name, content=content)
```

Use keyword arguments for REST resource identifiers and payloads. This keeps
upload, download, removal, and support operations consistent and readable.

## Code organization

- `commands/` contains the unmodified shell and Python examples under test.
- `scenarios/` contains pytest scenarios and their high-level assertions.
- `steps/` contains externally observable operations.
- `meta_steps/` combines operations and performs behavior-level checks.
- `utils/commands.py` owns command templates, binding, execution, and process
  lifecycle.
- `utils/rest.py` provides `OnezoneRestClient` and `OneproviderRestClient`.
- `utils/` also contains logging and persistence-directory support.

`CommandTemplate` only loads a script and binds its placeholders. It produces a
`Command`, which is the sole execution interface for `run`, `start`, retry,
logging, timeouts, and process termination. The `demo_commands` fixture supplies
the release-bound `DemoCommands` catalog to scenarios.

Started services are represented by `Onezone` and `Oneprovider`. Composite
startup operations return a `DemoEnvironment`. A service process is `None` when
the launch command exited after creating a detached container or an all-in-one
example owns the lifecycle.

## Test conventions

- A step performs an external action; it is not a wrapper around one `assert`.
- A meta step combines operations or validates a complete behavior.
- Steps never import meta steps.
- Scenarios and steps do not instantiate `CommandTemplate` or contain command
  paths.
- REST code passes a client first and uses keyword-only operation arguments.
- Foreground launcher processes are registered for cleanup immediately.
- All providers are started before service readiness checks begin.

The tutorial's `docker run -i` is intentional. Do not add `-t`: automated tests
do not provide a terminal.

## Debugging failures

Each test receives a directory under
`tests/demo_mode/logs/report.<timestamp>`. Every command invocation has a
numbered log containing the rendered command and its output. Repeated readiness
attempts receive separate files.

JUnit results are written to `test-reports/results-demo-mode.xml`. Bamboo also
publishes the command-log directory as the `command-logs` artifact.

If Docker reports an API compatibility error, specify the newest API supported
by the daemon:

```bash
make test_demo_mode RELEASE=25.1 DOCKER_API_VERSION=1.41
```

An interrupted local run can leave the fixed `oz_test`, `op_test1`, or
`op_test2` container names occupied. Remove those test containers before
retrying. The suite normally removes them before and after every scenario.

The persistence scenario additionally uses `/tmp/oz-pers`, `/tmp/op-pers`, and
`/tmp/op-storage`. It removes these paths only when their test ownership marker
is valid.

## Runner internals

`make test_demo_mode` starts pytest in the acceptance-test image and mounts the
host Docker socket. Service containers are therefore siblings of the test
runner. The runner temporarily starts as root to gain socket access, then
switches to the invoking UID and GID so reports and logs remain owned by the
developer or Bamboo user.

`RUNNER_NAME` is optional locally and lets Bamboo identify a runner left after
cancellation:

```bash
make test_demo_mode RELEASE=25.1 RUNNER_NAME=my-demo-mode-runner
```

Unlike the GUI, mixed, and Oneclient suites, demo-mode tests do not use an
`ENV_FILE` or `test_run.py`; every scenario starts its own services directly.
