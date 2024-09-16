import subprocess
import os
import sys
from osgeo import gdal

import rasterio
import numpy as np
import numpy.ma as ma
import tkinter as tk
from tkinter import filedialog

tk_version = tk.TkVersion

# Create a dictionary with the library names and their versions
libraries = {
    'subprocess': 'builtin',
    'os': 'builtin',
    'sys': 'builtin',
    'gdal': gdal.__version__,
    'rasterio': rasterio.__version__,
    'numpy': np.__version__,
    'tkinter': tk_version

}

# Open a text file in write mode
with open(r"C:\Users\CP\anaconda3\envs\IHC_env\ihc_libraries.txt", 'w') as f:
    # Write each library and its version to the file
    for lib, version in libraries.items():
        f.write(f"{lib}: {version}\n")

print("Library versions have been written to libraries_versions.txt")

