from pathlib import Path

from optiscaler_gui.application.dto import AppSettings
from optiscaler_gui.application.services import OptiScalerService
from optiscaler_gui.infrastructure.filesystem.game_scanner import LocalGameScanner
from optiscaler_gui.infrastructure.platform.null_backend import NullInjectionBackend
from optiscaler_gui.infrastructure.providers.local_package_provider import LocalPackageProvider
from optiscaler_gui.infrastructure.settings.json_settings_store import JsonSettingsStore


def test_service_can_be_composed(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.json"
    package_dir = tmp_path / "package"
    package_dir.mkdir()

    service = OptiScalerService(
        settings_store=JsonSettingsStore(settings_file),
        game_scanner=LocalGameScanner(),
        package_provider=LocalPackageProvider(),
        injection_backend=NullInjectionBackend(),
    )

    service.save_settings(AppSettings(optiscaler_package_dir=package_dir))

    assert service.load_settings().optiscaler_package_dir == package_dir
