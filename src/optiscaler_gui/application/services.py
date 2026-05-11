from __future__ import annotations

from pathlib import Path
from typing import Sequence

from optiscaler_gui.application.dto import AppSettings
from optiscaler_gui.application.ports import (
    GameScanner,
    InjectionBackend,
    OptiScalerPackageProvider,
    SettingsStore,
)
from optiscaler_gui.domain.models import (
    GameProfile,
    InjectionPlan,
    InjectionRequest,
    OperationResult,
)


class OptiScalerService:
    def __init__(
        self,
        settings_store: SettingsStore,
        game_scanner: GameScanner,
        package_provider: OptiScalerPackageProvider,
        injection_backend: InjectionBackend,
    ) -> None:
        self._settings_store = settings_store
        self._game_scanner = game_scanner
        self._package_provider = package_provider
        self._injection_backend = injection_backend

    def load_settings(self) -> AppSettings:
        return self._settings_store.load()

    def save_settings(self, settings: AppSettings) -> None:
        self._settings_store.save(settings)

    def scan_games(self, roots: Sequence[Path]) -> Sequence[GameProfile]:
        return self._game_scanner.scan(roots)

    def create_injection_plan(
        self,
        game: GameProfile,
        package_dir: Path,
        *,
        dry_run: bool = False,
        create_backup: bool = True,
    ) -> InjectionPlan:
        package = self._package_provider.load_from_directory(package_dir)
        request = InjectionRequest(
            game=game,
            package=package,
            dry_run=dry_run,
            create_backup=create_backup,
        )
        return self._injection_backend.create_plan(request)

    def apply_injection_plan(self, plan: InjectionPlan) -> OperationResult:
        return self._injection_backend.apply_plan(plan)
