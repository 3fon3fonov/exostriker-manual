Troubleshooting and reproducibility
===================================

A fit or plot is empty
----------------------

Check the loaded dataset slot, its use flag, the analysis radio button, enabled
planets and free-coordinate checkboxes. Initialize before interpreting a residual
or component plot. Inspect **Stdout/Stderr** and **Fit statistics info** for an
invalid likelihood, failed import, time coverage or backend rejection.

Times, units and geometry disagree
----------------------------------

Check full versus reduced Julian dates and the time standard, m/s versus km/s,
normalized flux versus counts, degrees versus radians, and relative versus
stellar astrometry. Transit event numbers depend on the search start; gaps are
intentional. Native summary "depth" is mid-transit flux, as documented in
:doc:`timing-astrometry`. Check Jacobi and phase conventions before comparing
scores from older sessions or external codes.

Uncertainties are zero or unavailable
-------------------------------------

A fixed coordinate may have zero error. Failed convergence, a boundary, singular
curvature or disabled uncertainty estimation can produce unavailable free-coordinate
errors. Inspect covariance/Hessian diagnostics. A finite symmetric error is a local
approximation; use converged posterior exploration when that approximation is poor.

Installation or display fails
-----------------------------

Use the same Python interpreter for installation and launch. Confirm PyQt6 and
scientific dependencies are present, and compiler tools/development headers are
available for native extension builds. On headless Linux, Qt offscreen capture
can use ``QT_QPA_PLATFORM=offscreen``; a desktop launch still requires a functioning
Qt platform/display environment. Use writable cache directories if Matplotlib,
Numba or Jupyter reports cache/config permissions.

For a numerical-only script, avoid importing ``exostriker.gui``. For a canceled
main-window calculation wait for process cleanup; the starting session is
restored, not partial progress. Use ``exostriker -last`` only when a valid trusted
autosave exists, and retain explicit session saves.

Fatal ``none_dealloc`` during a long calculation
------------------------------------------------

A crash mentioning ``deallocating None`` in ``process_worker.py`` while scanning
child processes can come from an incompatible compiled psutil dependency. This
was reproduced on Python 3.10 with a system psutil 5.9.8 binary, using process
scans alone without Qt or GP calculations. It is separate from an invalid GP
parameter or a likelihood exception.

The supervisor now detects the affected Linux PID validator and uses equivalent
Python validation, leaving process tracking and Stop cleanup active. Restart
Exo-Striker after updating; the crashed calculation cannot be resumed through
this fix. For dependency installation, use the same Python interpreter as for
launching the application, and avoid sharing system binary extensions built
for another interpreter. A healthy psutil build is left unchanged by the guard.

What to record
--------------

Keep original inputs, preparation/masking steps, time/velocity/flux conventions,
source revision, dependency versions, active datasets, model/likelihood backend,
stellar assumptions, epoch, bounds/priors, optimizer/sampler settings, numerical
accuracy, convergence diagnostics, summary convention, session and exports.
A screenshot alone is not a reproducible analysis.

Native model status 4
---------------------

This means the N-body physical model reached its 1,000,000 integration-step
limit, rather than an optimizer iteration/evaluation limit. Check the orbital
epoch, full versus reduced Julian dates, observation/search coverage and
integration step. The physical integrator can further reduce its step for short
or eccentric orbits. The native RV path resolves epoch zero to the first RV
observation, matching the established solver; restart after updating code that
previously interpreted the sentinel as literal Julian date zero. Explicit nonzero
epochs retain their meaning.
