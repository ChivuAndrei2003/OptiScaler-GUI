from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore

from optiscaler_gui.application.dto import AppSettings
from optiscaler_gui.application.services import OptiScalerService
from optiscaler_gui.domain.errors import OptiScalerError
from optiscaler_gui.domain.models import GameProfile, InjectionPlan


class MainViewModel(QtCore.QObject):
    settings_changed = QtCore.Signal(object)
    games_changed = QtCore.Signal(object)
    plan_created = QtCore.Signal(object)
    log_message = QtCore.Signal(str)

    def __init__(self, service: OptiScalerService) -> None:
        super().__init__()
        self._service = service
        self._settings = AppSettings()
        self._games: tuple[GameProfile, ...] = ()

    def load(self) -> None:
        self._settings = self._service.load_settings()
        self.settings_changed.emit(self._settings)
        self.log_message.emit("Settings loaded.")

    def set_package_dir(self, package_dir: Path) -> None:
        self._settings = AppSettings(
            optiscaler_package_dir=package_dir,
            game_roots=self._settings.game_roots,
        )
        self._service.save_settings(self._settings)
        self.settings_changed.emit(self._settings)
        self.log_message.emit(f"OptiScaler package set to: {package_dir}")

    def add_game_root(self, root: Path) -> None:
        roots = tuple(dict.fromkeys((*self._settings.game_roots, root)))
        self._settings = AppSettings(
            optiscaler_package_dir=self._settings.optiscaler_package_dir,
            game_roots=roots,
        )
        self._service.save_settings(self._settings)
        self.settings_changed.emit(self._settings)
        self.log_message.emit(f"Added game root: {root}")

    @QtCore.Slot()
    def scan_games(self) -> None:
        self._games = tuple(self._service.scan_games(self._settings.game_roots))
        self.games_changed.emit(self._games)
        self.log_message.emit(f"Found {len(self._games)} game folder(s).")

    def create_plan(
        self,
        game_index: int,
        package_dir: Path,
        *,
        dry_run: bool,
        create_backup: bool,
    ) -> None:
        if not 0 <= game_index < len(self._games):
            self.log_message.emit("Invalid game selection.")
            return

        try:
            plan = self._service.create_injection_plan(
                self._games[game_index],
                package_dir,
                dry_run=dry_run,
                create_backup=create_backup,
            )
        except OptiScalerError as error:
            self.log_message.emit(str(error))
            return

        self.plan_created.emit(plan)

    def apply_plan(self, plan: InjectionPlan) -> None:
        try:
            result = self._service.apply_injection_plan(plan)
        except OptiScalerError as error:
            self.log_message.emit(str(error))
            return

        self.log_message.emit(result.message)
        for detail in result.details:
            self.log_message.emit(f"- {detail}")
