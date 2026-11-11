#!/usr/bin/env python3
"""Capture empty full-window placeholders; never fabricate observation data."""
from pathlib import Path
import subprocess
import sys
TOOLS=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(TOOLS/'capture_tab_gallery.py')],check=True)
subprocess.run([sys.executable,str(TOOLS/'capture_tab_gallery.py'),'--qso'],check=True)
subprocess.run([sys.executable,str(TOOLS/'build_tab_gallery.py')],check=True)
subprocess.run([sys.executable,str(TOOLS/'build_screenshot_gallery.py')],check=True)
