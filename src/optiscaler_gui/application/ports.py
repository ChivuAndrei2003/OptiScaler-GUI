from __future__ import annotations

from pathlib import Path
from typing import Protocol, Sequence

from optiscaler_gui.application.dto import AppSettings
from optiscaler_gui.domain.models import (
    GameProfile,
    InjectionPlan,
    InjectionRequest,
    OperationResult,
    OptiScalerPackage,
)


class SettingsStore(Protocol):
    def load(self) -> AppSettings:
        ...

    def save(self, settings: AppSettings) -> None:
        ...


class GameScanner(Protocol):
    def scan(self, roots: Sequence[Path]) -> Sequence[GameProfile]:
        ...


class OptiScalerPackageProvider(Protocol):
    def load_from_directory(self, package_dir: Path) -> OptiScalerPackage:
        ...


class InjectionBackend(Protocol):
    def create_plan(self, request: InjectionRequest) -> InjectionPlan:
        ...

    def apply_plan(self, plan: InjectionPlan) -> OperationResult:
        ...
