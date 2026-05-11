from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AppSettings:
    optiscaler_package_dir: Path | None = None
    game_roots: tuple[Path, ...] = ()
