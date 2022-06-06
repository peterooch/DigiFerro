import PyInstaller.__main__

# DigiFerro
# Programmers:
# Baruch Rutman
# Roi Amzallag

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
    '--add-data=changepassword.ui;.',
    '--add-data=usermanagement.ui;.',
    '--add-data=history_edit.ui;.',
    # Control image
    '--add-data=preprocess/baseline.jpg;preprocess',
    # Program Guide
    '--add-data=DigiFerro_Guide.pdf;.',
    # PDF Exporter
    '--add-data=wkhtmltopdf.exe;.',
    # Report HTML template
    '--add-data=report_template.htm;.',
])
