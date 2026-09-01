# Historical mfapy optional-nlopt patch

FluxEMU is a bridge around mfapy, not an independent EMU numerical solver.
The selected source builds mfapy dictionaries and uses the mfapy-generated
calmdv function for forward MID calculation.

The audited dependency baseline is the mfapy repository commit
a10433af16682386548b360297e2476152d46ede, whose setup metadata identifies
version 0.6.3. At that baseline, mfapy/mfapy/optimize.py imports nlopt
unconditionally even though the forward-only calmdv path does not call its
nlopt-backed fitting routines.

Source-repository commit eef8dfb06c6cf9f67c5db06eb637f5684758ac4f
made that import optional and added a guard to fit_r_mdv_nlopt. The pre-patch
blob was 6f81091f302b0ad190a6dc4a9601b345177e3572 and the post-patch blob was
b48359a8f6f9c562f03e97d6d6071eabde783837. The exact historical diff is
preserved at
[provenance/patches/mfapy_optional_nlopt.patch](../provenance/patches/mfapy_optional_nlopt.patch).

No mfapy source is copied into this snapshot and the patch is not
automatically applied. A normal checkout of the pinned mfapy commit is
sufficient when nlopt is available. If nlopt is unavailable, the recorded
patch is the minimal historical adaptation, but a user must review and apply
it separately. The patch changes dependency handling only; it does not change
the forward EMU calculation.

Historical tests in fluxemu-prototype are evidence about the source
repository, not validation of this export. Export-specific test results are
recorded only in [provenance/VALIDATION_STATUS.md](../provenance/VALIDATION_STATUS.md).
