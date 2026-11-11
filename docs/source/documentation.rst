Maintaining this manual
=======================

This update was checked against the local source on 11 November 2026 (package
metadata 0.97.1). The application source and the manual are separate Git
repositories. Documentation updates do not deploy to Read the Docs until the
manual repository's hosting integration builds the updated branch.

Build without application dependencies
--------------------------------------

From ``exostriker-manual``::

   python -m pip install -r docs/requirements.txt
   python -m sphinx -n -W --keep-going -b html docs/source docs/_build/html

Open ``docs/_build/html/index.html``. The configuration reads no installed GUI or
native backend. ``.readthedocs.yaml`` defines the hosted build and documentation
requirements; source code installation is unnecessary for documentation builds.

GUI placeholders and author-provided examples
---------------------------------------------

Current GUI figures are **empty placeholders**. The author will supply real
screenshots and examples; do not invent observations, models or fit results
to populate them. Preserve full-window context and add only brief annotations.

To regenerate empty placeholders from the actual application::

   python tools/capture_gui.py

This runs ``capture_tab_gallery.py`` for the empty Exo-Striker GUI and an actual
``-QSO`` launch, then rebuilds the screenshot indexes. It uses Qt's offscreen
platform, isolated settings/caches under ``/tmp/exostriker-manual-capture``, and
no private session. It does not load observations or run fits/samplers. A version
change may require normal application extension compilation during import.
The compatibility ``capture_activity_gp.py`` entry point also produces empty
placeholders only.

``tools/build_tab_gallery.py`` groups the full-window views by workflow, retains
existing chapter image aliases, and builds :doc:`tab-gallery` and :doc:`qso-mode`.
``build_screenshot_gallery.py`` rebuilds the short :doc:`screenshots` overview.
Images live under ``docs/source/images/current``; JSON manifests record the
placeholder status, version, source hashes, open tabs and annotations.

When the author supplies a real example, replace the relevant placeholder and
update its caption and provenance together. Identify the actual data/session and
model state the author provides. Do not describe a default or empty panel as a
fit or initialize invented data to make an illustration look populated.

Legacy media
------------

The active manual no longer references the old screen photographs or animated
GIF tutorials. They remain in the repository as historical assets to preserve
external references; current pages use new Qt captures. Replace or remove an old
asset only after checking inbound links. The fresh gallery is :doc:`screenshots`.

Source references
-----------------

The behavior descriptions were checked against ``exostriker/gui.py``, the running
``lib/es.py`` UI, ``lib/UI/es.ui``, ``lib/RV_mod/__init__.py`` and the current native
joint/inference/model helpers. Further implementation notes live in the parent
checkout's ``docs/NATIVE_JOINT_FITTING.md``, ``NATIVE_INFERENCE.md``,
``SCIPY_UNCERTAINTIES.md``, ``STOPPING_CALCULATIONS.md``,
``EXTRA_CONVENTIONS_AUDIT.md`` and ``JOINT_ACTIVITY_GP.md``. Older implementation
notes may describe an earlier stage; current executable behavior takes precedence.
