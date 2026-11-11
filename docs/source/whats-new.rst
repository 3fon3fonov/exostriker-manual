New in this 0.97.1 manual update
================================

The manual now includes a :doc:`tab-by-tab full-window gallery <tab-gallery>`
and a :doc:`QSO-mode check <qso-mode>`, alongside the shorter
:doc:`screenshots` introduction. Figures are empty GUI placeholders with brief annotations, awaiting real
examples supplied by the author. They keep the plots, open settings and dataset
panels in context; no observation data or fitted examples are invented.

Activity diagnostics and coupled models
---------------------------------------

* **Plot opt. → Activity** now follows the RV/transit Size, Alpha, Symbol and
  Color controls, with the same pickers. It also holds activity-model styling
  and the moved correlation axis-label, color, error-bar and regression controls.
* Both activity time series and correlation plots have **Go to plot options**
  and **Cross hair** controls. The time series also has **Legend**.
* Independent time-series and GLS **o-c** checkboxes use the initialized activity
  mean, including selected cycle/GP contributions. Without a model they subtract
  the data mean. They never change the uploaded observations.
* **Edit → Edit file names → Activity** updates display names throughout the
  selectors, legends and GP/cycle forms. The current correlation pair is retained.
* The :doc:`joint activity GP <activity>` conditions RVs and selected indicators
  together in time. Existing kernel parameters and priors are shared; per-index
  responses and nuisance parameters expose their own bounds/priors. Unsupported
  derivative responses are disabled for the selected kernel.
* **Joint act.+ RV Magnetic cycle proxy (sine)** is an intrinsic deterministic
  mean outside celerite. Choose cycle indicators independently of the GP. Its
  period is shared; each activity index can have an independent phase offset
  relative to the RV cycle. Zero/fixed offsets preserve the earlier shared-phase
  behavior. Fit checkboxes precede values; uncertainties are labels beside them.
* RHK-prime-scale values remain representable in the numeric controls. Ordinary
  uncertainty labels use ``+/- 0.000``; tiny nonzero uncertainties use scientific
  notation. Stored errors retain full precision and accept inference errors
  from sampling or SciPy when available.

Fitting and interpretation
---------------------------

**Adopt best P** transfers the GLS/MLP sine period, amplitude and orbital phase
into the first free planet slot and evaluates the model without launching an
optimization. See :doc:`rvs` for the sine-to-circular-orbit convention.
**Print info** opens at a useful report size, fits within the screen, and retains
manual resizing.

Native **LM** and **Simplex** options, their defaults, fit-object persistence,
and supported prior behavior are documented in :doc:`fortran-optimization`.
Enabled priors enter inference, while reported **lnL** remains the data log
likelihood without prior density. Initialization validates bounds too.

Transit density mode uses the stellar-density bounds/priors under
**Limits and Priors → Stellar**, and labels density as density instead of
``a/R_star``. RV data take priority when choosing an automatic common epoch;
transit-only initialization uses the transit data. RV model plotting respects
its point-count and before/after-data controls in joint models. See
:doc:`rvtran` and :doc:`troubleshooting`.

The ExTRA :doc:`absolute-astrometry workflow <timing-astrometry>` has independent
Hipparcos and Gaia **Fit** checkboxes: fit either mission or both, with all
fitted planets contributing to the stellar motion. Unchecked missions remain
available for inspection but do not enter the likelihood or observation counts.

QSO presentation
-----------------

``-QSO`` keeps its existing GP, sine and quasar/test-data workflows. New
stellar-activity coupling, magnetic-cycle, transit and astrometric entry points
are hidden. Generic diagnostic styling and correlation tools remain shared.
See :doc:`qso-mode` for the actual launch screenshot and visibility conventions.
