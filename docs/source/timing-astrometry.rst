Timing, durations and astrometry
================================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

Transit timings
---------------

**TTVs** assigns each file to an included planet and enables its measurements.
The text format is ``N mid_time sigma_time`` with time/error in days::

   # N    BJD           sigma_days
   1      2458000.5     0.0022
   2      2458020.5     0.0023
   4      2458060.5     0.0021

Numbers are **one-based model conjunction numbers** from the configured search
start. Keep gaps for missing transits; do not renumber N=4 as N=3. Set the epoch
slightly before the first modeled event and **End of Model** beyond the last
observation. In RV+TTV, uncheck **first RV** under **Model opt. → Models → RV Model**
when entering a specific epoch. Include perturbing planets even without their
own measured transit times. Convert minutes to days by dividing by 1440.

Optional columns 4–7 are the depth observable, its error, duration in days and
its error. **Check the backend convention before preparing these columns.**
The current native joint duration/depth path preserves a legacy definition:
duration is an instantaneous straight-chord T14 estimate and its so-called
"depth" prediction is the uniform-disk mid-transit **flux**, 1 minus blocked
fraction. It is not a fractional flux loss and does not include limb darkening,
dilution or finite-exposure averaging. Do not copy an ordinary fitted transit
depth into that column without the appropriate conversion. Some offline help
still calls this fractional depth; the native joint implementation's convention
takes precedence. Omit these columns for a timing-only analysis.

Enable timing/duration/depth components deliberately. Supply the required stellar
density and radius ratio for summary observables. Initialize and inspect **TTVs**
and **TDVs**, then fit using an appropriate backend. Reduce the integration step
and compare predicted times to the measurement errors. Missing model events can
signal a wrong epoch, numbering, planet assignment or non-transiting geometry.
The dedicated native timing evaluator and plot selector are described in :doc:`api`.

Astrometry
----------

**Astrometry → Imaging** loads relative measurements with five columns:
``BJD x sigma_x y sigma_y``. Supply coordinates and errors in a consistent
angular unit and sky convention. Specify planet assignment and dataset use.
Do not substitute separation/position angle without converting them and their
uncertainties into the expected coordinate convention.

**Hipparcos/Gaia** supplies the absolute-astrometry workflow, with its own mission
inputs and stellar reference parameters in **Astrom. param.**. Match reference
epochs, parallax, proper motion and the input catalog/scan conventions. Absolute
astrometry measures stellar/photocentre motion; imaging usually measures relative
companion position. They require different physical interpretations.

The **Fit** checkbox beside each Hipparcos/Gaia input controls whether that
mission contributes to the likelihood. Select Hipparcos alone, Gaia alone,
or both. All fitted planets contribute to the stellar motion for either
mission; the hidden legacy planet selector does not restrict the model.
Unchecked datasets can remain loaded and displayed, but are excluded from
the fit score and the observation counts used for AIC/BIC and statistics.
Choices are saved with the session. New imports are enabled by default;
older sessions initially retain all previously used absolute datasets.

Use **Astr.** or **RV+Astr.**, initialize and inspect absolute and imaging plots,
then fit through the supported astrometric/SciPy path. Native RV/transit joint
likelihood does not include astrometry. A zero-companion astrometric baseline
can be useful before introducing orbital motion.

The active ExTRA low-level ``astrometry.orbit`` interface uses radians, days and
mas, with east (RA*) then north output. GUI angles are in degrees. Stellar-reflex
and relative-orbit sign/node conventions require conversion; do not pass a GUI
orbital row directly to low-level ExTRA on the assumption they are identical.
The checkout's ``docs/EXTRA_CONVENTIONS_AUDIT.md`` records the tested mapping and
its limits. Verify predictions against a known orientation before scientific use.
