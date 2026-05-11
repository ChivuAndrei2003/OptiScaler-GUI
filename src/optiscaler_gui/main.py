from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from optiscaler_gui.composition import build_main_window


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("OptiScaler GUI")
    app.setOrganizationName("OptiScaler GUI")

    window = build_main_window()
    window.resize(980, 680)
    window.show()

    return app.exec()
