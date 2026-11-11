# Exo-Striker manual

Current user workflows, GUI walkthrough and Python API documentation for
the adjacent Exo-Striker checkout. Source review: 11 November 2026; package
metadata: 0.97.1 (development source can precede PyPI releases).

Build from this directory:

```sh
python -m pip install -r docs/requirements.txt
python -m sphinx -n -W --keep-going -b html docs/source docs/_build/html
```

Open `docs/_build/html/index.html`. Read the Docs uses `.readthedocs.yaml`.
The documentation build does not import the application or require Qt/Fortran.

The GUI figures are **empty placeholders** until the author supplies real
screenshots/examples. No invented observations or synthetic fitted examples
are used. To regenerate the full-window placeholders and annotated indexes:

```sh
python tools/capture_gui.py
```

This uses a fully installed application environment and isolated temporary
settings. It captures the actual empty application and its `-QSO` presentation.
The manual's “Maintaining this manual” chapter describes provenance and how to
replace placeholders with author-provided examples.
