Helper windows and detailed plot tools
======================================

The dataset processing windows operate on a selected file/slot. Open them through
the corresponding dataset's data-options button during normal use. Load a dataset before executing processing actions. The
:doc:`screenshots` walkthrough shows where the dataset and accessory panels sit
in the complete window. Optional filter families may be disabled when their dependencies are
unavailable.

Transit detrending
------------------

Choose a normalization (none/mean/median as offered), a filter family and its
method. Time-windowed filters use the window length; spline and polynomial
methods use their own complexity controls; GP/regression choices require their
optional packages. **Break tolerance** controls segmentation across time gaps.
Use the transit mask with a valid ephemeris and an appropriate window to protect
transits from the trend estimator. **Try!** recomputes the preview; it is not the
main-window orbital Fit.

The lower view can display detrended data or GLS of the input, model or corrected
data. Compare all of them to identify a filter removing the signal of interest.
**Remove outliers** enables point rejection; **Add ROI box**, **Remove inside ROI**
and **Remove outside ROI** select/remove regions. Recompute after changing the
selection. Binning uses a width in days. **Add/Remove BJD** changes timestamps by
the entered offset; this arithmetic does not convert time standards.

The helper's **Apply Dilution fact.** is a data-processing operation. Distinguish
it from the fit model's per-dataset dilution in :doc:`transit`; avoid correcting
the same contamination twice. **Print stat** reports processing diagnostics.
**Save detr. data** writes the processed product; retain its raw input and record
the preprocessing settings. Closing/applying a helper may update its parent's
working dataset, so inspect the main plot and refit afterward.

RV and activity processing
--------------------------

These windows provide normalization/trend previews, point/region rejection,
binning, timestamp offsets, GLS diagnostics, reset, statistics and saved products.
Choose a trend justified by instrumental/stellar effects; subtracting a flexible
trend can absorb a planetary signal. RV and activity quantities have different
units even where the controls share a layout. **Reset** restores the helper's
stored starting data; an exported overwrite is a separate filesystem action.
After removing observations, recompute the preview before closing and publishing
the result. The application can require this to keep array lengths consistent.
The main-window Stop button does not supervise these helpers' independent jobs.

RV phase options
----------------

From **Extra Plots → Phased RV plots**, select a planet and **Phase options…**.
**Normalize phase to -0.5 … +0.5** changes the phase coordinate.
**Use mean osculating period from integration** uses a time-weighted period from
a cached integration of the fitted system; run orbital evolution first when
needed. It launches no integration itself. **Period adjustment +/- [days]** adds
a display-only period offset. **Show model as points** can reveal the spread in
an N-body component. **Reset this planet to fitted period** removes its display
adjustments. None of these operations refits the data or changes the residuals.

Cornerplots and sample correlations
-----------------------------------

Choose the sampled coordinates to display, their labels and presentation.
**Truths as** selects reference markers: median, mean, mode, max-lnL sample,
max-lnL GUI or no marker. A reference line is not an independent measurement.
Derived mass, semimajor axis and radius require their underlying sampled
coordinates and stellar assumptions. Solar/Jupiter/Earth choices change displayed
units. Flux-to-ppm changes the display scale. Derived h/k orbital coordinates
and angular centering need the matching parameterization; do not interpret a
wrap at 360 degrees as two physical modes without checking circular statistics.

Use **Plot opt. → Cornerplot** for styling and the sample-correlation controls for
coordinate selection/labels. Check whether a posterior is weighted (nested
sampling) before interpreting marginal summaries. An empty dialog before sampling
is expected. Generating a cornerplot cannot establish chain convergence.
