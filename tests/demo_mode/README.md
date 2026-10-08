# Demo-mode acceptance tests

This suite guards the source [demo-mode admin guide](https://github.com/onedata/onedata-documentation/blob/develop/docs/admin-guide/demo-mode.md):
it runs its Docker commands and verifies the resulting Onezone and Oneprovider
services through their public interfaces.

Unlike the other acceptance suites, demo mode uses neither one-env,
`test_run.py`, nor pytest-bdd. `ENV_FILE`, `SUITE`, `KEYWORDS`, `OPTS`, and
`--no-clean` do not apply; plain pytest starts a fresh environment per scenario.

> **Warning:** every scenario force-removes `oz_test`, `op_test1`, and
> `op_test2`. Persistence also owns `/tmp/oz-pers`, `/tmp/op_test<N>-pers`, and
> `/tmp/op_test<N>-storage`; without the suite's marker it refuses to remove
> existing paths and fails instead.

## Scenarios

| Scenario | Guide section | Command directories | Bamboo job |
|---|---|---|---|
| `test_run_in_foreground` | Running in the foreground; Acquiring an access token | `run_in_foreground/`, `access_token/` | Run in foreground |
| `test_run_in_background` | Running in the background; Acquiring an access token | `run_in_background/`, `access_token/` | Run in background |
| `test_distributed_environment` | Distributed environment | `run_in_foreground/`, `access_token/` | Distributed environment |
| `test_comprehensive_example` | Comprehensive example | `comprehensive_example/`, `access_token/` | Comprehensive example |
| `test_python_access` | Data access using Python | `run_in_foreground/`, `python_access/` | Python access |
| `test_persistency` | Retaining persistence between restarts | `persistency/`, `access_token/` | disabled (`VFS-13556`) |

## Running

You need `/var/run/docker.sock`, the release's service images, initialized
submodules (`make submodules`), and the acceptance-test image. Python access
also needs PyPI while creating its virtual environment.

```bash
# All scenarios
make test_demo_mode RELEASE=25.1

# One scenario (filename without .py)
make test_demo_mode RELEASE=25.1 SCENARIO=test_distributed_environment
```

| Make variable | Required | Meaning |
|---|---|---|
| `RELEASE` | yes | Onezone and Oneprovider image tag |
| `SCENARIO` | no | one file from `scenarios/`, without `.py` |
| `DOCKER_API_VERSION` | no | Docker API compatibility version, e.g. `1.41` |
| `RUNNER_NAME` | no | explicit test-runner name, primarily for Bamboo cleanup |

For IDE integration or debugging in a prepared local environment:

```bash
python3 -m pytest --confcutdir=tests/demo_mode -rs -s -v \
    tests/demo_mode/scenarios --release=25.1
```

`--confcutdir` prevents loading repository-wide, one-env-based fixtures.

## Diagnosing failures

JUnit output is written to `test-reports/results-demo-mode.xml`. Command logs
are stored under `tests/demo_mode/logs/report.<timestamp>/` and published by
Bamboo as the `command-logs` artifact:

```text
report.<timestamp>/
└── <scenario>/
    ├── command-001-<name>.log
    ├── command-002-<name>.log
    └── setup.log                 # python_access only
```

Each numbered log contains the rendered command and output. Command failures
name the template; readiness failures point to `await-*` and launcher logs.
Python failures preserve `setup.log`; REST failures appear in pytest and JUnit.

## Changing guide commands

Files in `commands/` are tested guide fragments, not test helpers. Keep them in
sync with the source guide. The intentional test-only adaptations are:

- `docker run -it` becomes `docker run -i`, because the runner has no TTY;
- the Python REPL session becomes a script whose results are printed.

Keep `xRELEASExVERSIONx`; documentation replaces it during its build. Use
`xCONTAINERxNAMEx` only where the guide permits selecting a container name. If
the guide itself is wrong, fix it there and then copy the corrected command
here rather than adding a test-only workaround.

When adding a scenario:

1. Add or reuse a guide fragment under the matching `commands/` section.
2. Register its path in `utils/commands/`; paths must not appear elsewhere.
3. Put external operations in `steps/` and reusable guide-level procedures in
   `meta_steps/`; steps must never import meta steps.
4. Keep scenario data, ordering, and comparisons of already-fetched values in
   `scenarios/`.
5. Add a Bamboo job and keep its final container list synchronized with
   `constants.py`.

Implementation mechanics belong in docstrings near `utils/test_runner.py`,
`utils/command_context.py`, `utils/commands/`, and `steps/environment.py`.
