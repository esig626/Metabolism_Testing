# Validation status

Status: the focused exported-package test suite passed.

The tests were run from the clean target clone with Python 3.11.2 and the
recorded source environment: COBRApy 0.31.1, NumPy 2.4.6, pandas 2.3.3, SciPy
1.17.1, PyYAML 6.0.3, pytest 9.1.1, and nlopt 2.11.0. mfapy was supplied from
the separately audited source tree at the Commit B post-patch optimize.py blob
b48359a8f6f9c562f03e97d6d6071eabde783837.

The normalized command, with machine-local dependency locations represented by
placeholders, was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=simulation/src \
FLUXEMU_MFAPY_SOURCE=<audited-mfapy-source-checkout> \
python -m pytest -q -p no:cacheprovider simulation/tests
```

The initial export run collected 185 tests: 182 passed and 3 failed in 7.96
seconds. Two failures came from zero entries in an export-only synthetic
Control0 callback where MIDClass requires strictly positive Dirichlet centres.
The third incorrectly compared the U-13C70 fixture checksum with the originating
50% tracer source checksum. Only those export-test assumptions were corrected;
no scientific implementation was changed.

The repeated command then completed with 185 passed in 7.63 seconds. Cache and
bytecode writing were disabled. No full historical research suite, bulk-result
runner, or uncommitted R1 runner/test was executed.

After a whitespace-only end-of-file cleanup in the adapted carbon-transition
test, the same environment and options were used for
`simulation/tests/test_carbon_transitions.py`; 8 tests passed in 1.96 seconds.

Historical source-repository test results are not transferred as validation
claims. The compact CSV and JSON files under fixtures/ are frozen generated
evidence or diagnostics. Their embedded PASS/valid fields describe the
originating computations. Passing this focused suite establishes only the
observed software behavior in the recorded environment; it does not establish
biological validity, complete reproducibility, novelty, or a uniform theorem.
