from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore, QtWidgets

from optiscaler_gui.domain.models import InjectionPlan
from optiscaler_gui.presentation.qt.view_models.main_view_model import MainViewModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, view_model: MainViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._current_plan: InjectionPlan | None = None

        self.setWindowTitle("OptiScaler GUI")
        self._build_ui()
        self._connect_signals()
        self._view_model.load()

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        package_layout = QtWidgets.QHBoxLayout()
        self._package_input = QtWidgets.QLineEdit()
        self._package_input.setPlaceholderText("OptiScaler package folder")
        self._package_button = QtWidgets.QPushButton("Browse")
        package_layout.addWidget(self._package_input, 1)
        package_layout.addWidget(self._package_button)

        roots_layout = QtWidgets.QHBoxLayout()
        self._root_input = QtWidgets.QLineEdit()
        self._root_input.setPlaceholderText("Game library folder")
        self._add_root_button = QtWidgets.QPushButton("Add root")
        self._scan_button = QtWidgets.QPushButton("Scan")
        roots_layout.addWidget(self._root_input, 1)
        roots_layout.addWidget(self._add_root_button)
        roots_layout.addWidget(self._scan_button)

        self._games_table = QtWidgets.QTableWidget(0, 3)
        self._games_table.setHorizontalHeaderLabels(["Game", "Folder", "Executable"])
        self._games_table.horizontalHeader().setStretchLastSection(True)
        self._games_table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents
        )
        self._games_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self._games_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._games_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self._games_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        actions_layout = QtWidgets.QHBoxLayout()
        actions_layout.addStretch(1)
        self._dry_run_checkbox = QtWidgets.QCheckBox("Dry run")
        self._dry_run_checkbox.setChecked(True)
        self._backup_checkbox = QtWidgets.QCheckBox("Create backup")
        self._backup_checkbox.setChecked(True)
        self._plan_button = QtWidgets.QPushButton("Create plan")
        self._apply_button = QtWidgets.QPushButton("Apply")
        self._apply_button.setEnabled(False)
        actions_layout.addWidget(self._dry_run_checkbox)
        actions_layout.addWidget(self._backup_checkbox)
        actions_layout.addWidget(self._plan_button)
        actions_layout.addWidget(self._apply_button)

        self._log = QtWidgets.QPlainTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumBlockCount(600)

        layout.addLayout(package_layout)
        layout.addLayout(roots_layout)
        layout.addWidget(self._games_table, 1)
        layout.addLayout(actions_layout)
        layout.addWidget(self._log, 1)

        self.setCentralWidget(central)

    def _connect_signals(self) -> None:
        self._package_button.clicked.connect(self._browse_package)
        self._add_root_button.clicked.connect(self._add_root_from_input)
        self._scan_button.clicked.connect(self._view_model.scan_games)
        self._plan_button.clicked.connect(self._create_plan)
        self._apply_button.clicked.connect(self._apply_plan)

        self._view_model.settings_changed.connect(self._show_settings)
        self._view_model.games_changed.connect(self._show_games)
        self._view_model.log_message.connect(self._append_log)
        self._view_model.plan_created.connect(self._show_plan)

    @QtCore.Slot()
    def _browse_package(self) -> None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select OptiScaler package")
        if directory:
            self._package_input.setText(directory)
            self._view_model.set_package_dir(Path(directory))

    @QtCore.Slot()
    def _add_root_from_input(self) -> None:
        text = self._root_input.text().strip()
        if text:
            self._view_model.add_game_root(Path(text))
            self._root_input.clear()

    @QtCore.Slot()
    def _create_plan(self) -> None:
        selected_game_index = self._selected_game_index()
        if selected_game_index is None:
            self._append_log("Select a game before creating a plan.")
            return

        package_dir = Path(self._package_input.text().strip())
        self._view_model.create_plan(
            selected_game_index,
            package_dir,
            dry_run=self._dry_run_checkbox.isChecked(),
            create_backup=self._backup_checkbox.isChecked(),
        )

    @QtCore.Slot()
    def _apply_plan(self) -> None:
        if self._current_plan is not None:
            self._view_model.apply_plan(self._current_plan)

    @QtCore.Slot(object)
    def _show_settings(self, settings) -> None:
        if settings.optiscaler_package_dir:
            self._package_input.setText(str(settings.optiscaler_package_dir))

    @QtCore.Slot(object)
    def _show_games(self, games) -> None:
        self._games_table.setRowCount(0)
        for row, game in enumerate(games):
            self._games_table.insertRow(row)
            self._games_table.setItem(row, 0, QtWidgets.QTableWidgetItem(game.name))
            self._games_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(game.install_dir)))
            executable = str(game.executable_path) if game.executable_path else ""
            self._games_table.setItem(row, 2, QtWidgets.QTableWidgetItem(executable))

    @QtCore.Slot(str)
    def _append_log(self, message: str) -> None:
        self._log.appendPlainText(message)

    @QtCore.Slot(object)
    def _show_plan(self, plan: InjectionPlan) -> None:
        self._current_plan = plan
        self._apply_button.setEnabled(True)
        self._append_log("Plan:")
        for index, step in enumerate(plan.steps, start=1):
            self._append_log(f"{index}. {step.label}")

    def _selected_game_index(self) -> int | None:
        selected_rows = self._games_table.selectionModel().selectedRows()
        if not selected_rows:
            return None

        return selected_rows[0].row()
