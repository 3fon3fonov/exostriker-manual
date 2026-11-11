Python API
==========

Import the numerical API directly. Importing ``exostriker`` alone does not create
a fit or expose every backend function; importing ``exostriker.gui`` creates Qt
application state and is unnecessary for scripts.

.. code-block:: python

   from pathlib import Path
   import numpy as np
   from exostriker.lib import RV_mod as rv

   fit = rv.signal_fit(name="My RV analysis")
   fit.init_fit = False
   fit.stellar_mass = fit.params.stellar_mass = 1.0  # solar masses
   data_path = Path("my_rvs.dat").resolve()
   data = np.loadtxt(data_path)
   fit.add_dataset("instrument A", str(data_path),
                   float(np.median(data[:, 1])), 1.0,
                   useoffset=True, usejitter=False)
   fit.add_planet(K=55.0, P=4.230785, e=0.0, w=0.0,
                  M0=180.0, i=90.0, cap=0.0,
                  usee=False, usew=False)
   fit.fitting(minimize_fortran=True, minimize_loglik=True,
               outputfiles=[1, 1, 1], amoeba_starts=2,
               fortran_kill=30, timeout_sec=120)
   print(fit.flag, fit.loglik, fit.P[0], fit.K[0])

This is a local point-estimate example, not a discovery or convergence test.
Set physically meaningful bounds/priors and inspect the results before sampling.
For real bundled inputs and explicit priors use ``examples/51Peg_RV.py``.

Session structure and indices
-----------------------------

Planet/dataset dictionaries use **zero-based slots**, whereas the GUI labels
Planet 1 / data 1. Sparse occupied slots are possible: do not assume ``range(npl)``
identifies all enabled planets. Parameter dictionaries include ``P``, ``K``,
``e``, ``w``, ``M0``, ``i`` and ``cap``; free flags use ``*_use``. Planet hard
bounds generally use ``*_bound``; dataset bounds use ``*_bounds``.
In stellar-density mode, the shared density uses ``stellar_rho_bounds``,
``stellar_rho_norm_pr`` and ``stellar_rho_jeff_pr`` instead of ``pl_a`` priors. The example
helpers illustrate these distinctions. ``use_planet`` identifies active planets.
Changing a displayed coordinate does not necessarily activate it in the chosen
parameterization.

Data import methods
-------------------

.. list-table:: ``signal_fit`` methods
   :header-rows: 1
   :widths: 46 54

   * - Call
     - Behavior
   * - ``add_dataset(name, path, offset, jitter, useoffset=True, usejitter=True, index=None)``
     - Add RV observations and instrument parameters; path is three-column time/RV/error text.
   * - ``add_planet(K=50, P=100, e=0, w=0, M0=180, i=90, cap=0, ..., index=None)``
     - Add/enable a planet; keyword useK/useP/usee/usew/useM0/usei/usecap selects free coordinates.
   * - ``add_transit_dataset(name, path, tra_idset=0, PDC=False)``
     - Load photometry or supported FITS; initialize the dataset's offset/jitter flags.
   * - ``add_ttv_dataset(name, path, ttv_idset=0, planet=0, use=False, stellar_density=None, Rpl_Rst=None)``
     - Import timing and optional summary measurements; explicitly enable and assign the planet.
   * - ``add_ast_dataset(name, path, ast_idset=0, planet=0, use=False)``
     - Load five-column relative astrometry.
   * - ``add_ast_dataset_hipp(...)`` / ``add_ast_dataset_gaia(...)``
     - Mission-specific absolute astrometry import; these are not generic imaging importers.
   * - ``add_act_dataset(name, path, act_idset=0)``
     - Load an activity indicator.

Some legacy import methods report a problem to stdout and return rather than
raising. Verify that the intended slot is populated and inspect diagnostics.
See :doc:`timing-astrometry` for units and depth conventions.

Optimization and sampling
-------------------------

``fit.fitting(...)`` is the established RV entry point. Important options are
``minimize_fortran``, ``minimize_loglik``, ``amoeba_starts``, ``fortran_kill``,
``timeout_sec``, ``npoints``, ``model_min``, ``model_max`` and
``outputfiles=[1,1,1]``. Plotting output options do not specify which observations
enter a joint likelihood. Check ``flag`` and finite scores rather than assuming
that returning means convergence.

``fit.fit_native(method=None, **options)`` optimizes supported joint Gaussian
RV/LC/TTV/TDV configurations. ``'LM'`` and ``'Simplex'`` explicitly select methods;
None uses configured stages. Set ``fit.init_fit=False`` for optimization.
It returns the session, with results on ``fit.fit_results``:

.. code-block:: python

   fit.fit_native("LM")
   result = fit.fit_results
   print(fit.loglik)
   print(result.native_fit_diagnostics)
   print(result.native_covariance)
   print(result.native_free_indices)

Session-specific solver budgets, tolerances and step controls are documented
in :doc:`fortran-optimization`. Read convergence and covariance status before using the errors. An unsupported
native configuration raises an error. Priors enter different objectives on the
native optimizer and SciPy paths; see :doc:`rvtran`.

The module functions ``rv.run_SciPyOp(fit, ...)``, ``rv.run_mcmc(fit, ...)`` and
``rv.run_nestsamp(fit, ...)`` run the corresponding workflows using session
settings. Configure free coordinates, bounds, priors, sampler settings and data
selection first. The bundled examples show the full setup and result exports.
Use an ``if __name__ == '__main__':`` guard in scripts with multiprocessing.
The GUI's Stop/rollback supervision is not supplied automatically to arbitrary
API calls; arrange process control/time limits for unattended work.

Native prediction and likelihood evaluation
-------------------------------------------

.. code-block:: python

   times = np.linspace(2458000.0, 2458010.0, 1000)
   prediction = fit.native_transit_model(times, dataset=0, phase="M0")
   likelihood = fit.evaluate_native_likelihood()
   print(likelihood.loglik)
   timing = fit.evaluate_native_ttv_likelihood(store=False)
   print(timing.loglik, timing.by_dataset)

These are evaluators, not optimizers. Their supported component sets differ.
``native_transit_model`` uses current parameters, defaults to M0, and accepts
``phase='t0'`` for Keplerian GUI-transit phase. It does not mutate the fit.
``evaluate_native_likelihood`` evaluates selected RV/photometry Gaussian terms,
excluding GP, separate timing and astrometry. It stores named native results by
default, without replacing existing fitted parameters/scores.
``evaluate_native_ttv_likelihood`` is the dedicated enabled-timing evaluator;
``store=False`` avoids publication, while ``publish=True`` also updates the
legacy-compatible five-section ``ttv_results`` structure.

``fit.ttv_model_backend='native'`` followed by ``fit.evaluate_ttv_model()`` selects
the dedicated native timing plot. ``'legacy'`` restores TTVFast; ``'native_joint'``
uses the joint optimizer's timing-result adapter. These selectors are distinct
from ``transit_likelihood_backend`` and do not by themselves switch samplers.

``fit.update_model_curves()`` refreshes plotting predictions without optimization.
``calculate_transit_model`` and ``calculate_transit_events`` control optional
publication work; dense plots are not the observation-time likelihood. Native
curves include ``fit_results.model_jd``, ``model``, ``transit_model_jd`` and
``transit_model`` when requested/supported. Inspect the named fields rather than
relying on undocumented positions inside old result arrays.

Saving and exporting
--------------------

.. code-block:: python

   import dill
   with open("analysis.ses", "wb") as stream:
       dill.dump(fit, stream)
   with open("analysis.ses", "rb") as stream:
       loaded = dill.load(stream)  # trusted files only
   loaded = rv.check_for_missing_instances(rv.signal_fit(), loaded)

Migration supplies missing fields but cannot make every historical physical
backend identical to current code. Save a new copy after checking a migrated fit.
``rv.latex_pl_param_table`` and ``rv.latex_prior_table`` export scientific tables;
inspect their current keyword options and output destination. Example tools save
sessions, RV figures and posterior/statistics exports.

Advanced modules
----------------

``RV_mod.dynamical_posterior`` provides ``IntegrationOptions``,
``integrate_posterior``, ``export_posterior`` and ``save_integrated_session`` for
posterior integrations. ``RV_mod.resonance`` provides resonance/normal-form
analysis. ``exostriker.lib.swift.api`` wraps SWIFT integration. These interfaces
are under active development; use the bundled posterior-stability scripts and
source docstrings for their detailed configuration and output structures.
Low-level ExTRA uses different angle/sky conventions from GUI rows.

.. note::
   Numerical backend imports may compile/load native extensions. Keep compatible
   NumPy/compiler builds and record the source revision and dependencies.
   The documentation intentionally avoids importing these modules during Sphinx
   builds so hosted documentation does not require Qt or Fortran.


Activity and magnetic-cycle session settings
--------------------------------------------

Use these controls on an existing fit with the author's activity observations
already loaded. ``slot`` is that dataset's zero-based slot; this example does
not create observation data or prescribe numerical model values.

.. code-block:: python

   from exostriker.lib.activity_gp import ensure as ensure_activity_gp
   from exostriker.lib.magnetic_cycle import ensure as ensure_cycle

   ensure_activity_gp(fit)
   fit.activity_gp[slot]['enabled'] = True
   # Existing RV kernel parameters and priors define the shared time process.
   # Choose the response/offset/jitter values, bounds and priors for your data.

   cycle = ensure_cycle(fit)
   cycle['enabled'] = True
   cycle['indicators'][slot]['enabled'] = True
   cycle['indicators'][slot]['phase_offset']['fit'] = True

The cycle has global ``period``, RV ``phase``, ``rv_amplitude`` and a fixed
``reference_epoch``. Each selected ``indicators[slot]`` record has an amplitude
and phase offset. Activity offsets and jitters are shared with
``fit.activity_gp[slot]`` when both models use the same indicator. Parameter
records store ``value``, ``fit``, ``bounds``, ``normal``, ``jeffreys`` and ``error``;
phase offsets use degrees and default to zero/fixed.

``fit.pyqt_symbols_act``, ``fit.pyqt_symbols_size_act``,
``fit.pyqt_color_alpha_act`` (0–255), and ``fit.act_colors`` hold activity
dataset display styles. These are presentation settings; the GUI residual
checkboxes do not overwrite ``fit.act_data_sets``. Activity display names are
the final field in the working record and its ``act_data_sets_init`` copy.
Use the GUI's **Edit file names** action to keep both copies and selectors in
sync. See :doc:`activity` for the full likelihood and GUI conventions.
