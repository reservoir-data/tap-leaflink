"""LeafLink entry point."""  # ruff:ignore[missing-copyright-notice]

from __future__ import annotations

from tap_leaflink.tap import TapLeafLink

TapLeafLink.cli()
