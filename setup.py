from setuptools import setup

APP = ['pdf2jpg.py']
OPTIONS = {'includes': ["pdf2image", "os", "Pillow", "tkinter", "stitching", "poppler-utils", "time"],
           'packages': ["pdf2image"],
           'iconfile':'pdficon.icns'
           }

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    resources=["/opt/homebrew/bin/pdftoppm"]
)
