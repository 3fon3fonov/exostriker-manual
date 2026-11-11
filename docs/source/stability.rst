Orbital evolution and stability
===============================

See :doc:`screenshots` for annotated full-window views of the relevant panels.

.. _stability:

**N-body** configures integrations independently from selecting an interacting
likelihood model. A good fit is not necessarily dynamically stable. The AMD
indicator is a fast diagnostic rather than a guarantee of long-term behavior.

In **General**, select the available SWIFT or REBOUND integration configuration,
span, numerical step, output interval and enabled planets. SWIFT options include
SyMBA, MVS and the GR variant where supported. Choose the numerical method for
the encounter/eccentricity regime and check the units displayed by each field.
**Test arbitary configuration** allows explicit starting configurations;
**Integrate mcmc/Nest. Samp.** explores saved posterior draws rather than only the
best fit. Set sample selection/count and integration settings before execution.
Run with **Run orb. evol**.

**Orb. Evol. → Orb. elem.** plots semimajor axes, eccentricities, arguments of
periastron, inclinations/nodes and energy diagnostics. **Orb. view** displays the
trajectories. **Res. angles** includes period evolution/ratios, delta omega and
resonant-angle combinations. Choose the planet pair and integer coefficients
appropriate to the proposed resonance. A period ratio near a rational number
alone is insufficient: examine libration/circulation over a sufficient baseline.

Check energy/angular-momentum drift where relevant, repeat with a smaller time
step, inspect close encounters and compare integration horizons. Output cadence
is not the integration step. Stability over the chosen finite integration does
not prove indefinite stability or establish posterior probability of stability.

**Plot opt. → N-body** changes axes, lines/markers, colors, opacity, angle folding,
range/hold and pair/planet selectors using existing history arrays. Per-planet
colors are local to each plot and saved in the session. Styling changes do not
rerun the integration. Main-window Stop discards an unfinished orbital history.
