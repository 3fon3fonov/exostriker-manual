First RV analysis
=================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

This example follows the bundled ``examples/51Peg_RV.py`` rather than an obsolete
session download. The data are in ``exostriker/datafiles``.

1. Start a new session and give it a recognizable name. Open **RV data** and
   load ``51Peg_ELODIE.dat`` and ``51Peg_HARPS.dat`` into separate dataset slots.
   Keep separate velocity offsets and jitters for the instruments.
2. Set the stellar mass under **Stellar param.**. The example uses an illustrative
   fixed value of 1 solar mass; substitute an appropriate measured value for
   scientific work.
3. Enable Planet 1 in **Planet param.** and choose **Keplerian** and **RV**.
   Start with P = 4.230785 days, K = 55 m/s, e = 0, omega = 0 degrees,
   M0 = 180 degrees, inclination = 90 degrees, and node = 0 degrees.
   Enable fitting for P, K, and M0; keep e and omega fixed for this circular model.
4. Initialize the two instrumental offsets near the respective medians of their
   input velocities. ELODIE and HARPS have very different zero points.
   Set finite parameter bounds in **Limits and Priors**. The script provides
   concrete example bounds for both planets and noise parameters.
5. Click **Initialize** and inspect the model before **Fit**. Refine the known
   short period locally; a large period perturbation over a long time baseline
   can move the optimizer into an alias.
6. Fit offsets and orbital parameters, then include nonnegative jitters when
   maximizing likelihood. Inspect **RVs o-c**, **GLS o-c**, and the phased RV plot.
   A good-looking curve alone does not validate the noise model.
7. Open **Fit statistics info**, inspect convergence and residuals, save a
   ``.ses`` file, and export the model/data. Use :doc:`otbfpu` for uncertainties.

The reproducible script alternative, from the checkout root, is::

   python examples/51Peg_RV.py

See ``examples/README.md`` for script options and output locations. Keep original
input data and the source revision with your results.
