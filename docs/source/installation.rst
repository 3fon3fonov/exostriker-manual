Installation and launch
=======================

The checkout declares Python **3.10 or newer**, PyQt6, NumPy, SciPy, and the
scientific dependencies in ``pyproject.toml``. Native extensions require a working
C compiler and GFortran; NumPy/f2py, Meson, and Ninja provide the build machinery.
Install the development headers for your Python on systems that package them
separately. SWIFT has its own compiled component.

Source installation
-------------------

Use an isolated environment. From the root of the Exo-Striker source checkout::

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -e .
   exostriker

On Windows, activate using ``.venv\Scripts\activate`` in CMD or
``.venv\Scripts\Activate.ps1`` in PowerShell. Install a compatible compiler
toolchain before building native extensions. With a conda environment, the
project's installation guide uses ``conda install conda-forge::gfortran``.

``python -m pip install exostriker`` installs the published package, which may
have fewer features than this development checkout. Avoid mixing interpreters:
use ``python -m pip`` from the environment used to launch the application.
The optional chat integration is installed with ``python -m pip install -e '.[chat]'``;
it requires separate service configuration.

Launch and recovery
-------------------

The supported entry point is ``exostriker`` (``exostriker.gui:main``).
Session arguments handled by the current GUI include::

   exostriker -ses /absolute/path/system.ses
   exostriker -mses /absolute/path/comparison.mses
   exostriker -last
   exostriker -debug
   exostriker -QSO

Use an absolute path: the normal launcher changes its working directory to your
home directory. ``-last`` reads ``~/autosave/auto_save.ses``. This is recovery
from an available autosave, not a guarantee that every edit was saved.
User display settings live in ``~/.exostriker/ES_settings.json`` and are seeded
from packaged defaults. Sessions are serialized Python objects; open only files
from trusted sources.

For a display-free import of the numerical API, see :doc:`api`. The documentation
build does not import Qt or compile the scientific backend.

See :doc:`qso-mode` for the QSO presentation and its hidden exoplanet controls.
