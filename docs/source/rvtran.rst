Joint models and backend selection
==================================

The analysis selector chooses RV+Transit, RV+TTV or RV+Astr.; individual dataset
use flags still apply. Load each data type into its own panel, use a consistent
time system and shared orbital epoch, and inspect each component separately.
Parameters such as period, geometry and stellar mass connect the components;
noise scales and offsets belong to the appropriate instruments/passbands.

Current optimizer behavior
--------------------------

The current **Fortran (internal opt.)** joint path fits supported RV, light-curve,
timing and enabled duration/depth combinations using LM and/or bounded
Nelder–Mead. Stage selectors and run counts apply to these joint models too.
It maximizes normalized Gaussian log likelihood, including free-jitter
log-variance terms, plus enabled Gaussian/Jeffreys log-prior densities. See
:doc:`fortran-optimization` for MAP scores and local uncertainty diagnostics.

GPs, astrometry, GR, mixed dynamical subsets, apsidal precession, stability
penalties and independent transit-time shifts require the other supported paths;
the GUI uses SciPy for unsupported native joint optimization. An explicit
``fit.fit_native(...)`` call raises an error for unsupported configurations.
Do not assume a native call silently drops the unsupported component.

SciPy optimization, MCMC and nested sampling have a separate automatic
RV/photometry likelihood selector. ``fit.transit_likelihood_backend`` accepts
``'auto'``, ``'native'`` or ``'legacy'``. Auto uses the joint native physical
likelihood where supported and retains the legacy backend otherwise. Inspect
``fit.likelihood_backend_used`` and ``fit.likelihood_backend_reason``.
A failing native trial is rejected; it is not evaluated with a different
physical model. The sampler engine and the likelihood backend are different
choices. Dedicated joint LM/Simplex timing support does not imply that every
sampler combination uses that same timing implementation.

Phase and dynamics
------------------

Keplerian native light-curve fitting defaults to t0 and derives M0 for RVs;
``phase='M0'`` explicitly selects the shared mean anomaly. N-body/timing-only
native fits use M0. RV+transit models use the RV epoch; adding transit data does
not replace it. A zero RV epoch resolves to the first RV observation. For
transit-only analyses, the default is the first transit-data timestamp. If RVs
are later added to an automatically initialized transit session, the RV epoch
takes priority. Explicitly chosen nonzero epochs remain unchanged. The resolved
epoch is shared by likelihood, plotting and published results. Dedicated timing-only
fits use the timing search start as the legacy element epoch and synchronize
the published epoch. In N-body models the physical trajectory fixes geometry
and stellar radius; an independent scaled axis is not another free orbital
coordinate. Shared density, limb darkening, coplanarity and jitter coordinates
are deduplicated in the native free vector.

Use an epoch before the first required timing event and an end after the last
observation. Event numbering can change if a conjunction crosses the search
boundary. Check integration step/tolerance and the Jacobi initialization
convention when comparing native and legacy solutions.

Uncertainties and scores
------------------------

Native LM uses Gaussian Fisher/Gauss–Newton covariance; Keplerian Simplex uses
an observed likelihood Hessian, and N-body Simplex uses Fisher covariance.
These are local symmetric errors without reduced-chi-squared rescaling.
Inspect ``native_fit_diagnostics`` for convergence and covariance status:
active bounds, singularity and failed convergence can make errors unavailable.

For joint fits ``fit.loglik`` is the combined score at the returned parameters.
``fit.fit_results.loglik`` retains a legacy component convention and can instead
be the RV-only contribution. Use named native component fields or the statistics
dialog when comparing models. Posterior mean/median parameters need not equal
the maximum-likelihood sample. See :doc:`otbfpu` and :doc:`api`.

RV model plotting range
-----------------------

In **Plot opt. → RV**, **N points to draw model** sets the RV curve's sample
count. **Model start before first RV [d]** extends the curve before the earliest
RV observation, and **Model end after last RV [d]** extends it after the latest
RV observation. These controls apply to joint RV+transit fits too. Regenerate
the model with **Initialize** or **Fit** after changing the controls.

The orbital epoch is a reference for the physical model; it does not force an
endpoint of the displayed RV curve. Transit and timing data at distant dates
do not enlarge the RV display range. Dense transit curves use their own
photometry range, and the transit data-time models still cover all loaded
photometry observations. Optional event searches retain the full data range.
