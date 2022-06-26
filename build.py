import os
import sys

import PyInstaller.__main__

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

# Not an integral part of the project
# invoke this script to build the project
# Please add references for all non-script files that are used by the program
# *.ui files in root folder are automatically accounted

# collect all *.ui files automatically
ui_files = [f'--add-data={file};.' for file in os.listdir('.') if '.ui' in file]

# Allow specifiying a entrypoint, used by vscode config for console/noconsole build
try:
    entry_script = sys.argv[1]
except IndexError:
    entry_script = 'mainwindow.py'

PyInstaller.__main__.run([
    entry_script,
    '--name=DigiFerro',
    '--icon=icon.png',
    '--onefile',
    # Support excel files via pandas
    '--hiddenimport=openpyxl',
    # Program icon
    '--add-data=icon.png;.',
    # Qt UI files
    *ui_files,
    # Control image
    '--add-data=preprocess/baseline.jpg;preprocess',
    # Program Guide
    '--add-data=DigiFerro_Guide.pdf;.',
    # PDF Exporter
    '--add-data=wkhtmltopdf.exe;.',
    # Report HTML template
    '--add-data=report_template.htm;.',
])
