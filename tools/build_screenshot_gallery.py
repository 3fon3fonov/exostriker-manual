#!/usr/bin/env python3
"""Build the annotated screenshot walkthrough from its manifest (no Qt needed)."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/source'
IMAGES = SOURCE / 'images/current'


def title(value, level='='):
    return value + '\n' + level * len(value) + '\n\n'


def main():
    manifest = json.loads((IMAGES / 'manifest.json').read_text())
    gallery = title('Annotated GUI walkthrough')
    gallery += ('These are annotated **empty GUI placeholders**, awaiting real examples supplied by the author. '
                'Each full-window view keeps the layout consistent as different tabs are opened. '
                'No observations, invented data or fitted models are shown. '
                'Numbers identify the same six regions in every image. '
                'See :doc:`tab-gallery` for every accessible tab, grouped by workflow.\n\n')
    for item in manifest:
        gallery += title(item['title'], '-')
        gallery += f".. figure:: images/current/{item['file']}\n   :alt: {item['title']}, with six numbered regions explained below.\n   :width: 100%\n\n   Empty GUI placeholder with the relevant tabs open.\n\n"
        for number, description in enumerate(item['callouts'], 1):
            gallery += f'{number}. {description}\n'
        gallery += '\n'
    gallery += title('Activity and QSO workflows', '-')
    gallery += ('See :doc:`tab-activity` for the new activity time-series, residual GLS, correlation options and file-name editing placeholders. '
                'See :doc:`activity` for the joint GP and magnetic-cycle controls, and :doc:`qso-mode` for the separate QSO presentation.\n')
    (SOURCE / 'screenshots.rst').write_text(gallery)


if __name__ == '__main__':
    main()
