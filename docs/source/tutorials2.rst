Reproducible Python tutorials
=============================

The current examples replace earlier downloadable session-based tutorials:

* ``examples/51Peg_RV.py`` and ``51Peg_RV.ipynb``: circular two-instrument RV fit.
* ``examples/HIP5364_RV.py`` and ``HIP5364_RV.ipynb``: multi-planet RV workflow.
* ``examples/WASP6_transit.py`` and ``WASP6_transit.ipynb``: transit modeling.
* ``examples/compare_transit_models.py``: compare available transit models.
* ``examples/check_native_likelihood.py``: native likelihood evaluation.
* ``examples/posterior_stability_scripts``: posterior dynamical analysis.

Read ``examples/README.md`` for requirements, command-line options and expected
outputs. Run scripts from the checkout root with the same Python environment as
the installed source. Scripts can produce files and long sampling/integration
runs; choose output directories and computational limits explicitly.

The embedded Jupyter console allows interactive inspection of session objects.
Confirm that the variable you are editing is the intended session and use
**Edit → push Jupyter var. to GUI** to transfer it. GUI updates and a Python
object reference are not interchangeable actions. For automation use :doc:`api`.
