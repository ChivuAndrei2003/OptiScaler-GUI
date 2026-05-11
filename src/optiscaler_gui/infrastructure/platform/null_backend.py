from __future__ import annotations

from optiscaler_gui.infrastructure.platform.base_stub_backend import BaseStubInjectionBackend


class NullInjectionBackend(BaseStubInjectionBackend):
    def __init__(self, platform_name: str = "unsupported") -> None:
        self.platform_name = platform_name
