#!/usr/bin/env python3
"""Generate a navigable full-window tab gallery from actual Qt captures."""
from pathlib import Path
from collections import defaultdict
import json
import shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/source'
IMAGES=SOURCE/'images/current'
GROUPS={
 'Scientific plots':('tab-plots','Scientific plot tabs'),
 'Physical parameters':('tab-parameters','Physical parameter tabs'),
 'Gaussian processes':('tab-gp','GP and magnetic-cycle tabs'),
 'Bounds and priors':('tab-priors','Bounds and prior tabs'),
 'Model and inference':('tab-inference','Model, optimizer and sampling tabs'),
 'Plot appearance':('tab-appearance','Plot-option tabs'),
 'Datasets':('tab-data','Dataset tabs'),
 'Accessories':('tab-tools','Accessory tabs'),
 'New activity workflows':('tab-activity','New activity workflows and file names'),
}
def heading(title,character='='):return title+'\n'+character*len(title)+'\n\n'
def main():
 metadata=json.loads((IMAGES/'tab-gallery-manifest.json').read_text())
 assert metadata.get('placeholder'), 'Only empty GUI placeholders may be generated automatically.'
 groups=defaultdict(list)
 for item in metadata['screenshots']:groups[item['group']].append(item)
 index=heading('Every tab in context')
 index+=('These are actual full-window Qt captures of version '+metadata['version']+'. '
  'Each accessible tab in the maintained main-window Designer form is opened separately, '
  'including nested parameter, prior, kernel, plot-option and dataset tabs. '
  'Use the chapter links below to avoid scrolling through unrelated workflows. '
  'The compact :doc:`screenshots` walkthrough remains the starting point.\n\n'
  'These are **empty GUI placeholders**. No observations, invented data, fitted models, posterior samples or orbital histories are loaded. '
  'The author will supply real screenshots/examples to replace them. Default fields and disabled controls are shown as they appear in an empty session. '
  'No private session or physical monitor capture is used.\n\n'
  'The six numbered regions are menus, scientific plots, session/calculation controls, '
  'parameters/options, accessory tools, and dataset controls. '
  'Each image includes a brief explanation of the selected tab and important actions. '
  'Click an image for full resolution.\n\n')
 index+=f"The current capture contains **{len(metadata['screenshots'])} full-window views**.\n\n"
 index+='.. toctree::\n   :maxdepth: 1\n\n'
 for group,(filename,title) in GROUPS.items():
  if not groups[group]:continue
  index+='   '+filename+'\n'
  text=heading(title)+'See :doc:`tab-gallery` for the capture conventions and six numbered regions.\n\n.. contents:: Open tabs\n   :local:\n   :depth: 1\n\n'
  for item in groups[group]:
   anchor=item.get('widget',Path(item['file']).stem)
   text+='.. _gui-tab-'+anchor+':\n\n'+heading(item['title'],'-')
   text+=f".. figure:: images/current/{item['file']}\n   :alt: Empty GUI placeholder with {item['title']} open and brief numbered annotations.\n   :width: 100%\n\n   Empty GUI placeholder, awaiting an author-provided real example. {item['description']}\n\n"
  (SOURCE/(filename+'.rst')).write_text(text)
 (SOURCE/'tab-gallery.rst').write_text(index)
 by_widget={item.get('widget'):item for item in metadata['screenshots']}
 aliases={'overview':'RV_time_series_tab','workflow-transit':'tab_timeseries_tra',
          'workflow-inference':'mcmc_param_tab','workflow-dynamics':'N_body_tab',
          'activity-gp':'tab_activity_joint_gp','magnetic-cycle':'tab_magnetic_cycle'}
 walkthrough=[]
 for alias,widget in aliases.items():
  item=by_widget[widget]
  shutil.copyfile(IMAGES/item['file'],IMAGES/(alias+'.png'))
  record=dict(item,file=alias+'.png')
  if alias not in ('activity-gp','magnetic-cycle'):walkthrough.append(record)
  else:
   provenance=dict(metadata,screenshots=[record])
   (IMAGES/(alias+'-provenance.json')).write_text(json.dumps(provenance,indent=2))
 (IMAGES/'manifest.json').write_text(json.dumps(walkthrough,indent=2))
 (IMAGES/'provenance.json').write_text(json.dumps(metadata,indent=2))

 qso=IMAGES/'qso-provenance.json'
 if qso.exists():
  qso_metadata=json.loads(qso.read_text())
  assert qso_metadata.get('placeholder'), 'QSO figure must also be an empty placeholder.'
  record=qso_metadata['screenshots'][0]
  text=heading('QSO mode')
  text+='Launch the shared application in quasar mode::\n\n   python -m exostriker -QSO\n\n'
  text+=('The QSO interface retains **Data**, **Test data**, **Sample corr.**, sine parameters and its '
   'existing GP/SciPy workflows. Exoplanet-only stellar/transit/astrometry/dynamical pages are hidden. '
   'The joint stellar activity GP, magnetic-cycle page, **Select activity indicators** button and '
   'activity-model width/color controls are hidden too. Generic Test data styling, residuals about '
   'the mean, crosshairs, legends and correlation controls remain available. '
   '**Edit file names** keeps its QSO Data-only form.\n\n'
   'Tab filtering preserves the original shared widgets, indices and numerical values; it does not '
   'rename a newly added exoplanet tab into a QSO feature.\n\n')
  text+=f".. figure:: images/current/{record['file']}\n   :alt: Actual QSO launch with only the shared GP page visible and exoplanet activity entry points hidden.\n   :width: 100%\n\n   Empty GUI placeholder from an actual -QSO launch. {record['description']}\n"
  (SOURCE/'qso-mode.rst').write_text(text)
if __name__=='__main__':main()
