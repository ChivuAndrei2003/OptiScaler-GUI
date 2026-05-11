## OptiScaler-GUI

### Pre-release checklist
#### 1) Basic and clean GUI ❌
#### 2) Main Logic : 
##### detect installed games ❌
##### install / uninstall optiscaler ❌
##### dowloand cache / components ❌

Python + Qt GUI skeleton for Windows and Linux OptiScaler workflows.

### Run the current project

If you already have the local virtual environment from this repo, run:

```bash
env/bin/python main.py
```

On Windows, the equivalent is:

```powershell
.\env\Scripts\python.exe main.py
```

If you are setting up from scratch:

```bash
python -m venv env
env/bin/python -m pip install -e .
env/bin/python main.py
```

On Windows:

```powershell
py -m venv env
.\env\Scripts\python.exe -m pip install -e .
.\env\Scripts\python.exe main.py
```

The installed console command is also available after `pip install -e .`:

```bash
optiscaler-gui
```

### Architecture

```text
src/optiscaler_gui/
  application/      Use cases, DTOs, and ports implemented by adapters.
  domain/           Core models and errors with no Qt or OS dependencies.
  infrastructure/   Filesystem, settings, package discovery, Windows/Linux backends.
  presentation/     Qt windows and view models.
  resources/        Icons, styles, and packaged static assets.
```

The actual Windows/Linux OptiScaler injection logic is intentionally isolated behind
`InjectionBackend` in `application/ports.py`. Implement that contract in:

- `infrastructure/platform/windows_backend.py`
- `infrastructure/platform/linux_backend.py`

This keeps UI code, persistence, scanning, and platform-specific operations separate.
