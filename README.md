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
