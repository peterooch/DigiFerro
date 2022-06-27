# DigiFerro

This program is a solution for digitization of ferrography workloads, which includes among other things automatic analysis of images, actions to take, record keeping, graph generation.

## Authors
Baruch Rutman (@peterooch)  
Roi Amzallag (@roiamz)

### Required Packages
OpenCV for Python, PyQt5, NumPy, pandas, openpyxl, joblib, matplotlib, scikit-image, jinja2, pdfkit

To export reports to pdf format [`wkhtmltopdf`](https://wkhtmltopdf.org/) is also required.

In addition there is a build script (`build.py`) that uses PyInstaller to package the project into a single file.

To install all packages you can use the following command:
```
pip install -r requirements.txt
```

It is recommended to use a virtual enviroment if you want to package the program using PyInstaller to avoid issues.

The program was built and tested with Python 3.9 on Windows 10.

### Program usage

To run the program via the source code you can click on `mainwindow.pyw` to run it via the python interpreter without a console window.
Click on `mainwindow.py` to run with a console window.

For logging in there is a default admin account with username `admin` and password `admin`.

User guide can be opened via the menubar: Help -> Help
