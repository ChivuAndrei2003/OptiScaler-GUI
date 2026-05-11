from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from optiscaler_gui.application.dto import AppSettings


class JsonSettingsStore:
    def __init__(self, settings_file: Path | None = None) -> None:
        self._settings_file = settings_file or self._default_settings_file()

    def load(self) -> AppSettings:
        if not self._settings_file.exists():
            return AppSettings()

        payload = json.loads(self._settings_file.read_text(encoding="utf-8"))
        return AppSettings(
            optiscaler_package_dir=self._optional_path(payload.get("optiscaler_package_dir")),
            game_roots=tuple(Path(path) for path in payload.get("game_roots", [])),
        )

    def save(self, settings: AppSettings) -> None:
        self._settings_file.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "optiscaler_package_dir": (
                str(settings.optiscaler_package_dir) if settings.optiscaler_package_dir else None
            ),
            "game_roots": [str(path) for path in settings.game_roots],
        }
        self._settings_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _default_settings_file(self) -> Path:
        app_name = "optiscaler-gui"

        if os.name == "nt":
            base_dir = os.environ.get("APPDATA")
            if base_dir:
                return Path(base_dir) / app_name / "settings.json"

        config_home = os.environ.get("XDG_CONFIG_HOME")
        if config_home:
            return Path(config_home) / app_name / "settings.json"

        return Path.home() / ".config" / app_name / "settings.json"

    def _optional_path(self, value: object) -> Path | None:
        if not isinstance(value, str) or not value:
            return None

        return Path(value)
