import PyInstaller.__main__

# Not an integral part of the project
# invoke this script to build the project

PyInstaller.__main__.run([
    'mainwindow.py',
    '--name=DigiFerro',
    '--icon=icon.png',
    '--onefile',
    # Support excel files via pandas
    '--hiddenimport=openpyxl',
    # Program icon
    '--add-data=icon.png;.',
    # Qt UI files
    '--add-data=mainwindow.ui;.',
    '--add-data=history.ui;.',
    '--add-data=openfile.ui;.',
    '--add-data=graph.ui;.',
    '--add-data=login.ui;.',
    '--add-data=createaccount.ui;.',
    # Control image
    '--add-data=preprocess/baseline.jpg;preprocess',
    # Program Guide
    '--add-data=DigiFerro_Guide.pdf;.',
    # PDF Exporter
    '--add-data=wkhtmltopdf.exe;.',
])
