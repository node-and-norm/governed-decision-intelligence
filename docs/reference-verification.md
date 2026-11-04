# Reference verification: Governed Decision Intelligence

These commands reproduce the existing checks at the audited source revision. They leave the working checkout untouched by using a disposable clone. The expected messages below come from the [repository validator](../scripts/validate_repository.py); they describe success conditions, rather than a new research finding.

## Environment and exact commands

Use Git, a POSIX shell and Python 3.12, the version selected by [continuous integration](../.github/workflows/ci.yml). The project declares Python 3.10 or later in its [existing guide](validation-and-reproducibility.md). Internet access is needed to clone and install the [pinned dependencies](../requirements-dev.txt).

```sh
(
  set -eu
  review_dir="$(mktemp -d)"
  git clone https://github.com/node-and-norm/governed-decision-intelligence.git "$review_dir/repository"
  cd "$review_dir/repository"
  git checkout --detach 68ac580470d6fbd7d3505e3f42c4917fa9bc9582
  git rev-parse HEAD
  python3.12 --version
  python3.12 -m venv .venv
  . .venv/bin/activate
  python -m pip install -r requirements-dev.txt
  export PYTHONDONTWRITEBYTECODE=1
  python scripts/validate_repository.py
  git diff --exit-code
  git status --short
  python -m pip freeze
)
```

The final validator line should be `repository validation: PASS`, with exit status 0. A failed check produces `repository validation: FAIL` and exit status 1. [Validator](../scripts/validate_repository.py).

## Check scope and expected outputs

| Command inside the disposable environment | Successful message | Scope |
| :--- | :--- | :--- |
| `python scripts/validate_repository.py --only schema` | `schema validation: PASS` | Schema validity, included example and selected negative cases. |
| `python scripts/validate_repository.py --only gate` | `gate classifier: PASS` | Existing classifier fixture assertions. |
| `python scripts/validate_repository.py --only interop` | `interoperability fixtures: PASS` | Local receipt regression assertions. |
| `python scripts/validate_repository.py --only citation` | `citation metadata: PASS` | Citation format. |

The [wrapper](../scripts/validate_repository.py) defines these commands. The [current review guide](current-review.md#known-limits) records contract and test gaps that a passing run leaves unresolved.

## Write effects and interpretation

Environment installation writes `.venv`. The command suppresses Python bytecode writes because the repository tracks a cache file. Without that setting, a test run can change that tracked cache. Receipt checks can use generated fixture artifacts; the separate `gdi_driver.py` demo writes `receipts/gdi/`. Keep those outputs in the disposable checkout. The supplied signing key is public demonstration material. [Existing reproducibility guide](validation-and-reproducibility.md), [driver](../examples/testvectors-interop/gdi_driver.py).

Record the commit, Python version, dependency versions, command, exit status and generated files. Local checks have the scope of their fixtures. A new external conformance run needs its own revision and result record. [Contribution record](scopeblind-contribution-review.md), [research limits](limitations.md).
