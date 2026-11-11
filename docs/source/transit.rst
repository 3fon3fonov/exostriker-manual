Transit photometry
==================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

.. _transit:

Load and prepare data
---------------------

**Transit data** accepts text columns ``BJD flux sigma_flux [airmass]``. Supply
relative flux, a baseline near one, finite values and positive flux errors.
The optional fourth column supplies the auxiliary airmass regressor. Dedicated
FITS handling recognizes TESS light curves (SAP or PDC selection) and CHEOPS
SCI_COR products. The TESS importer adds its mission epoch offset; do not add it
a second time. Check the imported dates and flux/error scales in the inspector.

**Data options → detrend** opens the interactive detrending window. Inspect
raw data, protect transits with an appropriate mask, select the wotan filter
and time scale, preview with **Try!**, and compare the corrected light curve.
Filtering on a transit's own time scale can erase or distort it. Interactive
point/region rejection and binning change the analyzed data: retain the original
file and record these choices. Export the corrected series when appropriate.
Mission PDC processing is not a substitute for checking residual systematics.

Set **Transit** in the analysis selector, enable the planets and relevant datasets,
and set P, t0, radius ratio, inclination and scaled axis or shared density.
For joint fits, follow :doc:`rvtran` for shared phase and epoch. **TLS** searches
for candidate transit signals; configure its range before running and inspect
individual events and aliases before adopting a period.

Passbands and nuisance parameters
---------------------------------

Each light curve has its own offset, jitter and optional linear/quadratic
baseline. **Limb-dark. param.** selects uniform, linear, quadratic or nonlinear
limb darkening. **L-D grouping** links coefficients for justified common passbands;
apply grouping deliberately and verify the target dataset indices. Passband
coefficients should not be shared solely because files belong to the same star.

**Dilution** uses the target's fraction D of the total light::

   observed_model = 1 + D * (undiluted_model - 1)

D = 1 means no contamination. Smaller D reduces depth. This is not the ratio of
contaminating to target flux. Enter a value and check **Fit** to vary it; an
unchecked value remains fixed. Set bounds and optional prior under the
right-hand **Limits and Priors → Dilution**. No separate Apply step is required.
Dilution can be strongly correlated with radius ratio.

Model and validation
--------------------

Initialize, inspect **Tran.** and **Tran. o-c**, fit, and examine the phased view
and event coverage. Native models support independent Keplerian and Newtonian
N-body trajectories; supported joint inference uses their Fortran likelihood.
Legacy batman/TTVFast models remain available for other configurations. Record
the actual backend, not just the selected optimizer. See :doc:`rvtran`.

Dense plotting grids differ from observation-time likelihood calculations.
Explicit native API options support finite exposures and supersampling; the
GUI joint-fit defaults are instantaneous samples. If exposure integration matters,
configure it explicitly through the API and verify convergence of the chosen
sampling. A smooth displayed curve does not establish accurate exposure averaging.

Shared stellar density and its priors
-------------------------------------

In **Model opt. → Parameterisation → Stellar rho**, the shared density coordinate
uses **kg/m³**. Its bounds and optional Gaussian/Jeffreys prior come from
**Limits and Priors → Stellar**, rather than any planet's a/Rstar limits.
New sessions default to **100–5000 kg/m³**; saved bounds are retained. The unused
per-planet scaled-axis bounds/priors are disabled in density mode.

Switching into density mode initializes the shared value from **Stellar param.**
(default 1000 kg/m³). The first enabled planet's density field and the Stellar
value are synchronized. Switching back restores the previous scaled-axis values.
The shared coordinate is packed only once even for multiple transiting planets.
The same Stellar bounds/prior metadata is used by SciPy, MCMC and nested sampling;
native LM/Simplex uses its hard bounds with the Gaussian likelihood objective
explained in :doc:`rvtran`. Parameter/prior table exports use the density label
and Stellar prior too.

An out-of-bounds error lists the parameter, starting value and allowed range.
Correct the starting value or the scientific limits deliberately; no automatic
clipping to a bound is applied.
