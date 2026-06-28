# Releasing Aegize to PyPI

Aegize is published to [PyPI](https://pypi.org/project/aegize/) using **PyPI
Trusted Publishing** (OpenID Connect). The release workflow authenticates to PyPI
via short-lived OIDC tokens issued to GitHub Actions — **no API token is stored in
GitHub secrets.**

- GitHub repository: `gggaswint/aegize`
- Workflow file: `.github/workflows/publish.yml`
- GitHub Environment: `pypi`
- Package name: `aegize`

---

## One-time setup (do this once)

### 1. Create a PyPI account

1. Register at <https://pypi.org/account/register/> and verify your email.
2. **Enable two-factor authentication** (PyPI requires it to publish).

### 2. Configure the Trusted Publisher on PyPI

The `aegize` project does not exist on PyPI yet, so add a **pending publisher**
(this both reserves the name and authorizes the workflow):

1. Go to <https://pypi.org/manage/account/publishing/>.
2. Under **"Add a new pending publisher"**, choose **GitHub** and enter:

   | Field | Value |
   | --- | --- |
   | PyPI Project Name | `aegize` |
   | Owner | `gggaswint` |
   | Repository name | `aegize` |
   | Workflow name | `publish.yml` |
   | Environment name | `pypi` |

3. Click **Add**.

> If the name `aegize` is already taken by someone else, you'll need a different
> name — tell the maintainer before proceeding.

### 3. (Recommended) Create the GitHub Environment

In the repo: **Settings → Environments → New environment → `pypi`**. You can add
protection rules (e.g. required reviewers) so only approved runs can publish. The
workflow references this environment; the Trusted Publisher above is scoped to it.

---

## Publishing a release

### First release (current version, no new tag needed)

A GitHub Release for `v0.2.0` already exists, so trigger the workflow manually:

1. Finish the one-time setup above.
2. Repo → **Actions → "Publish to PyPI" → Run workflow** (branch `main`).
3. The workflow builds the sdist + wheel, runs `twine check`, and publishes via
   Trusted Publishing.

### Subsequent releases

1. Bump `version` in `pyproject.toml` (e.g. `0.2.1`). Commit and push to `main`.
2. Tag and create a GitHub Release:
   ```bash
   git tag -a v0.2.1 -m "Aegize v0.2.1"
   git push origin v0.2.1
   gh release create v0.2.1 --title "v0.2.1" --notes "…" --latest
   ```
3. Publishing a Release fires `release: published`, which runs the workflow and
   publishes automatically.

> Versions are immutable on PyPI: you can never re-upload the same version. Always
> bump the version for any change.

---

## Build and check locally (optional, before tagging)

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

Test the built wheel in a clean environment:

```bash
python -m venv /tmp/aegize-test
/tmp/aegize-test/bin/pip install dist/*.whl
/tmp/aegize-test/bin/python -c "import aegize; print(aegize.__version__)"
```

---

## Verify the published release

After the workflow succeeds:

```bash
pip install aegize
python -c "import aegize; print(aegize.__version__)"
```

The project page is <https://pypi.org/project/aegize/>.

---

## Rollback / yanked releases

PyPI does not allow deleting-and-reuploading a version. If a release is broken:

- **Fix forward:** bump the version (e.g. `0.2.2`), and release again.
- **Yank** the bad version so new installs skip it (existing pins still resolve it):
  PyPI → **Manage project → Releases →** select the version → **Options → Yank**.
- Deleting a release entirely is possible but discouraged — the version number is
  then permanently burned (it can never be reused).

---

## Notes

- The workflow targets production PyPI. To rehearse on **TestPyPI** first, add a
  second pending publisher on <https://test.pypi.org> (same fields) and a job
  using `repository-url: https://test.pypi.org/legacy/`.
- The sdist is intentionally lean (`[tool.hatch.build.targets.sdist]` in
  `pyproject.toml`): only `src/`, `tests/`, `examples/`, `README.md`, `LICENSE`,
  and `pyproject.toml` ship. The wheel contains only the `aegize` package
  (including `py.typed`).
- README images use absolute URLs so they render on the PyPI project page.
