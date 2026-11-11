Fortran optimizer settings
==========================

Open **Model opt. → Models → Fortran opt. (RV / Transit / TTV)**, then select
**Nelder-Mead (Simplex)** or **LM**. These settings belong to the active fit
object and are saved in single/multi sessions. They are independent of global
appearance preferences in ``ES_settings.json``. Older sessions receive the
existing defaults when loaded or prepared.

**Auto (existing)** preserves the relevant backend's established rule;
it does not impose a new common budget or tolerance. **Restore existing defaults**
resets just the selected method. Small tolerances can be entered as ``1e-7``.
Scroll within the settings page if the window is too short to show all rows.

Default behavior
----------------

.. list-table:: Defaults retained by Auto
   :header-rows: 1
   :widths: 25 25 25 25

   * - Control
     - RV Keplerian
     - RV N-body
     - Native joint
   * - LM iterations
     - 200
     - 200
     - 5000 per run
   * - Simplex iterations
     - No extra cap beyond the existing evaluation counter
     - No extra cap beyond the existing evaluation counter
     - 5000 per run
   * - Simplex evaluation counter
     - 200000 per internal run
     - 50000 per internal run
     - No separate evaluation limit
   * - Simplex objective tolerance
     - Relative spread 1e-6
     - Relative spread 1e-3
     - Absolute spread 1e-7
   * - Simplex parameter tolerance
     - No additional diameter test
     - No additional diameter test
     - Scaled diameter sqrt(1e-7)
   * - Internal Simplex runs
     - Up to 20, stopping early on small improvement
     - 1
     - 1
   * - LM objective improvement tolerance
     - Absolute chi-square improvement 0.01
     - Absolute chi-square improvement 1e-5
     - Absolute objective improvement 1e-7
   * - LM initial damping
     - 0.001
     - 0.001
     - 0.001
   * - Simplex-size / derivative-step multipliers
     - 1 / analytic derivatives unchanged
     - 1 / 1
     - 1 / 1

These describe GUI fitting defaults. An explicit Python ``amoeba_starts`` argument
still controls the established RV call's internal-run budget. An explicit native
``maxiter`` or ``tolerance`` argument remains available; nonzero session tolerances
supply method-specific overrides. An older explicit ``native_joint_maxiter``
setting is retained when the new session iteration field is Auto.

Interpreting the controls
-------------------------

**Maximum iterations** limits optimizer updates; **Maximum function evaluations**
limits optimizer objective calls. They are different budgets. A positive evaluation
limit covers all internal RV restarts within a configured run, or each internal
joint run. Final result publication and covariance/error calculations are outside
the optimizer evaluation budget; total reported evaluation counts may therefore
be larger. The established automatic RV Simplex counter retains its historical
counting convention; an explicit evaluation cap counts actual objective calls.

**ftol** uses the backend-specific objective rule shown above. **xtol** adds a
parameter-change/diameter test: RV coordinates use a relative scale of at least
one, while joint coordinates use the optimizer's internal physical scaling.
Joint Simplex requires both its objective and diameter tests. LM also retains its
existing damping and gradient stopping rules. **Gradient tolerance** applies to
joint LM only, with the existing numerical floor retained.

**Initial simplex-size multiplier** scales the existing initial displacements;
1 preserves their parameter-specific sizes and additive offsets.
**Internal Simplex runs** rebuilds the simplex around the preceding result.
It is separate from the primary/secondary **N consecutive iter.** counters, which
repeat whole minimizer stages. These runs do not draw independent random starting
solutions. The RV restart-improvement tolerance remains 1e-6 by default.

**Initial LM damping** controls the first damped update; subsequent damping is
adaptive. **Derivative-step multiplier** applies to numerical N-body RV and joint
derivatives, leaving analytic Keplerian RV derivatives unchanged. It is separate
from the physical integration time step and integration accuracy.

A budget-limited result is a best available point, not evidence of convergence.
Inspect native joint convergence/covariance diagnostics and verify stability of
the solution when changing numerical settings. See :doc:`otbfpu` for uncertainty
interpretation and :doc:`rvtran` for the supported components of each backend.

Python configuration
--------------------

The fit stores a nested ``fortran_optimizer_options`` dictionary:

.. code-block:: python

   from fortran_optimizer_options import ensure_options

   options = ensure_options(fit)  # also fills defaults for old sessions
   options['simplex']['maxiter'] = 10000
   options['simplex']['step_scale'] = 0.5
   options['lm']['initial_damping'] = 0.01
   # Set maxiter/maxfev/ftol/xtol/gtol or restarts to 0 for Auto.
   # Multipliers default to 1; initial_damping defaults to 0.001.

GUI edits update this dictionary immediately. Switching sessions restores that
session's values. Programmatic changes are validated before a numerical call;
the GUI synchronizes them when the session is selected/refreshed.

Priors and the fitted objective
--------------------------------

Enable Gaussian or Jeffreys priors using the existing **Limits and Priors**
checkboxes. The native Fortran LM and Simplex optimizers then maximize
**log-likelihood + log-prior** (a MAP fit). With no enabled priors, the existing
likelihood behavior is preserved. Stellar-density mode uses the prior under
**Limits and Priors → Stellar**, alongside the shared density bounds.

The GUI routes RV-only fits with enabled priors through the native Fortran
solver as well. Its **Native joint** defaults in the table above apply.
Unsupported native physics requires SciPy; enabled priors are never silently
discarded in this route. The low-level legacy RV optimizer remains available
for likelihood fitting. For Python use ``fit.fit_native()`` or
``fit.fitting_sequence()`` for prior-aware fitting;
``fit.fit_native(use_priors=False)`` explicitly disables the prior terms.

The reported **Best lnL** remains the likelihood score. Output also shows the
log-prior and log-posterior, available as ``fit.logprior`` and
``fit.logposterior`` and in ``fit.native_fit_diagnostics``. Both optimizers
include prior curvature in local error estimates. These are local posterior
errors; use sampling to obtain credible intervals for asymmetric distributions.

Gaussian priors require a positive standard deviation. Jeffreys priors require
positive parameter values and positive, ordered normalization endpoints.
Parameter hard bounds remain separately enforced. **Init** validates the
starting bounds and evaluates the model without optimizing.

If free-parameter errors are ``NaN``, read the covariance diagnostic in the
calculation output. It distinguishes non-convergence, a covariance step crossing
a bound, a solution at a bound, failed model derivatives, and a singular or
non-positive information matrix. It names fitted coordinates at or near their
bounds and notes quadratic limb darkening near ``u1 + u2 = 1``, where limb
intensity vanishes. A tight prior can push a fit toward these constraints.
Changing the finite-difference step does not repair a genuinely invalid local
Gaussian approximation; use posterior sampling to assess asymmetric uncertainty.
