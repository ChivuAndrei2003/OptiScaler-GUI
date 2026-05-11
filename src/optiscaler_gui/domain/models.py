from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Platform(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class GameProfile:
    id: str
    name: str
    install_dir: Path
    executable_path: Path | None = None


@dataclass(frozen=True, slots=True)
class OptiScalerPackage:
    root_dir: Path
    version: str | None = None
    files: tuple[Path, ...] = ()


@dataclass(frozen=True, slots=True)
class InjectionRequest:
    game: GameProfile
    package: OptiScalerPackage
    dry_run: bool = False
    create_backup: bool = True


@dataclass(frozen=True, slots=True)
class InjectionStep:
    label: str
    source: Path | None = None
    destination: Path | None = None
    destructive: bool = False


@dataclass(frozen=True, slots=True)
class InjectionPlan:
    request: InjectionRequest
    steps: tuple[InjectionStep, ...]


@dataclass(frozen=True, slots=True)
class OperationResult:
    succeeded: bool
    message: str
    details: tuple[str, ...] = ()
