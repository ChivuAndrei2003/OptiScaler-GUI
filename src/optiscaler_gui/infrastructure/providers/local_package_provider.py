from __future__ import annotations

from pathlib import Path

from optiscaler_gui.domain.errors import InvalidPackageError
from optiscaler_gui.domain.models import OptiScalerPackage


class LocalPackageProvider:
    def load_from_directory(self, package_dir: Path) -> OptiScalerPackage:
        package_dir = package_dir.expanduser()

        if not package_dir.exists() or not package_dir.is_dir():
            raise InvalidPackageError(f"OptiScaler package directory does not exist: {package_dir}")

        files = tuple(path for path in sorted(package_dir.iterdir()) if path.is_file())
        version = self._read_version(package_dir)

        return OptiScalerPackage(root_dir=package_dir, version=version, files=files)

    def _read_version(self, package_dir: Path) -> str | None:
        version_file = package_dir / "version.txt"
        if not version_file.exists():
            return None

        version = version_file.read_text(encoding="utf-8").strip()
        return version or None
