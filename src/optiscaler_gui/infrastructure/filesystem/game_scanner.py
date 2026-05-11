from __future__ import annotations

from pathlib import Path
from typing import Sequence
from uuid import uuid5, NAMESPACE_URL

from optiscaler_gui.domain.models import GameProfile


class LocalGameScanner:
    _windows_executable_suffixes = (".exe",)
    _linux_executable_suffixes = (".sh", ".x86_64", ".AppImage")

    def scan(self, roots: Sequence[Path]) -> Sequence[GameProfile]:
        games: list[GameProfile] = []

        for root in roots:
            root = root.expanduser()
            if not root.exists() or not root.is_dir():
                continue

            for candidate in self._candidate_dirs(root):
                executable = self._find_executable(candidate)
                games.append(
                    GameProfile(
                        id=str(uuid5(NAMESPACE_URL, candidate.as_posix())),
                        name=candidate.name,
                        install_dir=candidate,
                        executable_path=executable,
                    )
                )

        return tuple(games)

    def _candidate_dirs(self, root: Path) -> Sequence[Path]:
        return tuple(
            child
            for child in sorted(root.iterdir())
            if child.is_dir() and not child.name.startswith(".")
        )

    def _find_executable(self, game_dir: Path) -> Path | None:
        suffixes = self._windows_executable_suffixes + self._linux_executable_suffixes

        for child in sorted(game_dir.iterdir()):
            if child.is_file() and child.suffix in suffixes:
                return child

        return None
