Optimization, priors and uncertainty
====================================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

.. _otbfpu:

A fitted point estimate, local covariance and sampled posterior answer different
questions. Optimize a plausible starting model and inspect residuals before
sampling. Check all free-coordinate flags, physical bounds, prior families,
noise models and the actual likelihood backend.

Native Fortran LM/Simplex includes enabled Gaussian and Jeffreys priors in the
fitted objective and local covariance. With priors enabled the result is a MAP
estimate. See :doc:`fortran-optimization` for score reporting and backend selection.

Local parameter errors
----------------------

Fortran joint LM/Simplex publishes convergence/covariance diagnostics as described
in :doc:`rvtran`. Failed covariance is unavailable rather than proof of a fixed
parameter. Fixed-coordinate errors can remain zero.

**Model opt. → Models → SciPyOp opt. → Estimate parameter uncertainties
(numerical Hessian)** estimates curvature of the negative probability used by
SciPy after fitting. With Gaussian/Jeffreys priors this is local posterior
curvature, not purely likelihood curvature. It is off by default, skipped for
initialization and saved in the session. Successful central differences require
roughly ``4*N*N + 1`` objective evaluations for N free coordinates per pass;
additional smaller-step passes can increase this. Inspect the status/progress
and unavailable-error diagnostics. These symmetric errors do not find distant
modes or replace a credible interval.

MCMC
----

Configure **Model opt. → MCMC opt.**, including walkers, steps, initial spread,
burn-in, thinning and workers, then **Run MCMC**. The bundled emcee implementation
samples the prior-weighted probability. Keep walkers within valid bounds and
avoid identical or singular initial positions. Use multiple diagnostics:
trace behavior, mixing, autocorrelation where reliable, independent runs and
stability of marginal intervals as the chain length increases. Thinning cannot
repair an unconverged chain.

Inspect **Sample corr.**, histograms and the cornerplot controls. Select the
parameters and angle-display conventions deliberately; distributions spanning
0/360 degrees require circular interpretation. Record whether reported values
are best sample, mean or median and which interval convention was used.

Nested sampling
---------------

Configure **Nest. Samp. opt.** and **Run Nest.samp.**. The bundled dynesty sampler
uses the specified prior transform. Live points, stopping criteria and proposal
settings trade computational cost against exploration. Inspect weight-aware
posterior summaries and repeat difficult multimodal problems with more thorough
exploration. Evidence depends on prior volume and likelihood normalization;
compare it only for appropriate common data/model conventions.

Saved samplers identify their likelihood backend for native inference. Save the
session and export samples/statistics with your data and settings. The main-window
Stop operation discards incomplete sampling and returns to the starting session;
it does not turn a partial chain into an accepted result.

Sampler controls at a glance
----------------------------

.. list-table:: Settings that change a sampling run
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Interpretation
   * - N walkers factor / live points factor
     - Multiplied by the number of free dimensions; increasing a factor increases ensemble/live-point size and cost. Inspect the actual resulting count.
   * - Init. Gaussian Ball
     - Spread around the starting solution; it must produce distinct valid points within bounds, not an identical ensemble.
   * - Burning phase / MCMC phase
     - Settling and production steps. Inspect the discarded/retained phases before interpreting summaries.
   * - N threads/CPUs
     - Parallel work allocation. Native likelihood cost and process overhead determine whether extra workers help.
   * - Save samples in memory / ASCII
     - Controls retaining interactive results and writing a table. Set the destination explicitly; preserve labels and weights with the samples.
   * - Stability constraints; AMD / N-body
     - Adds the chosen stability selection to inference. This changes the allowed model, can be expensive and is distinct from a post-fit integration.
   * - Adopt parameter as
     - Chooses mean, median, mode, best-lnL or starting values to publish to the session. These summaries need not share the same likelihood.
   * - MAD / percentiles
     - Chooses the displayed spread/interval convention. Record which was used and inspect asymmetric or wrapped distributions.
   * - Static / Dynamic nested sampling
     - Fixed live-point allocation versus adaptive additional effort during a run.
   * - Dynesty bound / sampling options
     - Constrained-prior proposal construction and draw strategy; poor choices can be costly in correlated or multimodal models.
   * - dlogz stop / maxcall / maxiter
     - Evidence-based stopping tolerance versus likelihood-call/iteration budgets. A budget stop can precede the requested evidence accuracy.
   * - Posterior frac.; weighted samples
     - Allocation toward posterior accuracy in dynamic runs and treatment of nonuniform nested weights. Preserve weights for valid summaries.

Fit statistics
--------------

The GUI's combined information criteria use ``AIC = -2 lnL + 2 k`` and
``BIC = -2 lnL + k ln(N)``, where k counts unique free parameters and N the
included observations. Shared physical coordinates must not be counted twice.
Component parameter counts are nominal diagnostic counts rather than
leverage-based effective degrees of freedom. GP/noise models complicate naive
interpretations of reduced chi-squared and tests based on it.

The dataset-statistics view reports RMS and inverse-variance-weighted RMS of
fitted-model residuals before GP subtraction. Its weights use formal measurement
errors, without added jitter. These statistics have the data's units; they are
not interchangeable with a normalized Gaussian likelihood that includes jitter
and log-variance terms. F-test/periodogram FAP outputs depend on their assumptions
and trial/search configuration; they are not posterior planet probabilities.
