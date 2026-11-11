#!/usr/bin/env python3
"""Compatibility entry point for empty GP/cycle placeholders.

Real examples are supplied by the author. --magnetic-cycle remains accepted;
both page aliases are generated from the empty tab-gallery capture.
"""
from pathlib import Path
import subprocess
import sys
TOOLS=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(TOOLS/'capture_gui.py')],check=True)
