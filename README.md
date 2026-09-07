# macpkg-migrate-core

Lightweight, manager-neutral planning and safety primitives shared by
`brew2port`, `brew2fink`, and `macpkg-migrate`.

The package handles catalog snapshot loading, exact candidate selection,
review-only near-hit policy, serializable migration plan records, and the
shared no-implicit-removal safety rule. It never invokes Homebrew, MacPorts,
Fink, or any other package manager.

The public API is available from `macpkg_migrate_core`:

```python
from macpkg_migrate_core import Identity, candidates_for, plan_record
```

Manager-specific applications retain inventory, target availability checks,
installation, verification, rollback guidance, and user-facing workflows.

Releases are published to PyPI from the `pypi` GitHub environment using
trusted publishing. Configure `tomck/macpkg-migrate-core` as a trusted
publisher on PyPI before publishing the first release.

## First PyPI release

Publishing uses PyPI Trusted Publishing through GitHub Actions; no API token,
GPG key, or local signing setup is required. A repository administrator must
first create the project on PyPI (or configure its pending publisher) with:

- Owner: `tomck`
- Repository: `macpkg-migrate-core`
- Workflow: `publish.yml`
- GitHub environment: `pypi`

The workflow requests the required OIDC permission and publishes only when a
GitHub Release is marked published. After the PyPI publisher is saved, create
a GitHub Release for tag `v0.3.0`. The action builds and publishes the package
without storing a PyPI credential in GitHub.

After the workflow succeeds, verify the public installation in a clean
environment:

```sh
python3 -m venv /tmp/macpkg-migrate-core-check
. /tmp/macpkg-migrate-core-check/bin/activate
python -m pip install --upgrade pip
python -m pip install macpkg-migrate-core==0.3.0
python -c 'import macpkg_migrate_core; print(macpkg_migrate_core.__version__)'
```

Update consumer lock/checksum or Homebrew formula metadata only after this
clean installation succeeds.
