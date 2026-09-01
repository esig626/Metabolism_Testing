"""Load an explicitly supplied mfapy source dependency."""

from __future__ import annotations

import importlib
import os
from functools import lru_cache
from pathlib import Path
import sys
from types import ModuleType


@lru_cache(maxsize=1)
def load_mfapy() -> ModuleType:
    """Return mfapy from an installation or an explicit source checkout.

    The upstream mfapy 0.6.3 packaging metadata does not expose its nested
    package correctly when installed editable. FLUXEMU_MFAPY_SOURCE may
    therefore identify a separately obtained mfapy source checkout. No
    vendored or machine-specific fallback is assumed by this export.
    """

    try:
        return importlib.import_module("mfapy")
    except ModuleNotFoundError as exc:
        if exc.name != "mfapy":
            raise

    configured = os.environ.get("FLUXEMU_MFAPY_SOURCE")
    if not configured:
        raise ModuleNotFoundError(
            "mfapy is not importable; install/provide the separately "
            "provenanced mfapy dependency or set FLUXEMU_MFAPY_SOURCE"
        )
    source_root = Path(configured).expanduser().resolve()
    package_init = source_root / "mfapy" / "__init__.py"
    if not package_init.is_file():
        raise ModuleNotFoundError(
            "mfapy is not importable and the configured source was not found at "
            f"{source_root}; set FLUXEMU_MFAPY_SOURCE"
        )
    source_text = str(source_root)
    if source_text not in sys.path:
        sys.path.insert(0, source_text)
    return importlib.import_module("mfapy")


def mfapy_source_path() -> Path:
    """Return the source directory of the loaded mfapy package."""

    module = load_mfapy()
    return Path(module.__file__).resolve().parent
