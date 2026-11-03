"""Ricrea le sei schermate illustrative Windows 11 / Office."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name('gallery-windows.py')),run_name='__main__')
