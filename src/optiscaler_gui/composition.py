from __future__ import annotations

import platform

from optiscaler_gui.application.services import OptiScalerService
from optiscaler_gui.infrastructure.filesystem.game_scanner import LocalGameScanner
from optiscaler_gui.infrastructure.platform.linux_backend import LinuxInjectionBackend
from optiscaler_gui.infrastructure.platform.null_backend import NullInjectionBackend
from optiscaler_gui.infrastructure.platform.windows_backend import WindowsInjectionBackend
from optiscaler_gui.infrastructure.providers.local_package_provider import LocalPackageProvider
from optiscaler_gui.infrastructure.settings.json_settings_store import JsonSettingsStore
from optiscaler_gui.presentation.qt.main_window import MainWindow
from optiscaler_gui.presentation.qt.view_models.main_view_model import MainViewModel


def build_main_window() -> MainWindow:
    service = OptiScalerService(
        settings_store=JsonSettingsStore(),
        game_scanner=LocalGameScanner(),
        package_provider=LocalPackageProvider(),
        injection_backend=_build_injection_backend(),
    )
    return MainWindow(MainViewModel(service))


def _build_injection_backend():
    system_name = platform.system().lower()

    if system_name == "windows":
        return WindowsInjectionBackend()

    if system_name == "linux":
        return LinuxInjectionBackend()

    return NullInjectionBackend(system_name or "unknown")
