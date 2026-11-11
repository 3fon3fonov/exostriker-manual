Radial velocities
=================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

.. _rvs:

Import and noise model
----------------------

Use **RV data → Offsets and jitters** to load a dataset into a free row. Generic
text input has at least three whitespace-separated numeric columns::

   # BJD [days]       RV [m/s]   sigma_RV [m/s]
   2458000.125        12.4       1.2
   2458001.130        18.7       1.4

Use finite timestamps/measurements and positive uncertainties. Convert km/s to
m/s before loading. Keep a consistent time standard, preferably documenting
BJD_TDB explicitly. A plot-axis date offset does not convert the input time system.

Each instrument has its own additive velocity offset and white-noise jitter.
Jitter adds in quadrature to formal errors: variance = sigma squared + jitter
squared. Keep a physically meaningful nonnegative jitter branch and bounds.
Separate instruments and configuration changes when their zero points differ.
**RV trends** adds linear/quadratic baseline terms; check degeneracy with a
long-period companion. **Data options** controls individual datasets and access
to helper tools. RVBank and MAROON-X have dedicated importers.

Search, fit, inspect
--------------------

Use **GLS** to inspect sinusoidal periodicities and **Window (DFT)** to identify
sampling aliases. **GLS o-c** searches the residuals of the current model;
**MLP** compares trial-period likelihoods. Configure search bounds and resolution
in **Model opt. → GLS/MLP/TLS opt.**. Do not interpret every peak as a planet:
check sampling, stellar activity and residual structure.

**Adopt best P** in GLS o-c (or the MLP adoption action) copies the strongest
sine into the first free planet slot, including its period, semi-amplitude and
phase, then evaluates without optimizing. Its circular-orbit mean anomaly is
``360 * ((epoch - T0) % P) / P - 90`` degrees, wrapped to a full circle for
the model's cosine RV convention. Adopting a peak does not establish a planet.

Enable a planet, enter a plausible period/amplitude, choose the free coordinates
and finite bounds, then Initialize and Fit. Start with a Keplerian model.
**Extra Plots → Phased RV plots** isolates a planetary component; inspect the
unphased residuals as well. Multiple planets can require several starting points.
The automated search is a candidate-finding aid.

Use **N-body** when interactions matter. Check stellar mass, inclinations,
ascending nodes, shared epoch, numerical accuracy and Jacobi conventions. A
coplanar constraint shares inclination rather than supplying independent
inclination measurements. Current native joint fitting supports such shared
coordinates; the older manual's SciPy-only restriction is obsolete.

Validate with **Fit statistics info**, residual diagnostics, uncertainty
estimation and :doc:`stability`. RV-only inclinations are generally poorly
constrained unless interactions provide information.
