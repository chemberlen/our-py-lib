'''
Created on Jun 26, 2015 Fri - 22:58:49

@author: LKumaresan
'''

from distutils.core import setup
import os
import sys
from glob import glob
import py2exe


# import shutil
#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = os.path.dirname(parentFolder2)
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      currentFolder,
                      # currentFolder + '\qtui',
                      # currentFolder + '\main',
                      # currentFolder + '\core'
                      # parentFolder1 + '\lib\Controls',
                      # "C:/Windows/winsxs/x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91"
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(modulePath)

sys.path.append('J:\Python\CommonLib\src')
sys.path.append('J:\Python\CommonLib\src\kmxPyQt')

dllpath = r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4148_none_5090ab56bcba71c2'

sys.path.append(dllpath)
data_files = [
    ## Instruct setup to copy the needed DLL files into the build directory
    ("Microsoft.VC90.CRT", glob(dllpath + r'\*.*')),
]

# PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'pepper.py'
APPNAME = 'Pepper'
DESCRIPTION = 'app created by template'
COMPANY_NAME = 'kumaresan studio'
COPYRIGHT = 'kumar'
VERSION = '1.0.0'
USE_ICON = True
ICON_FILE = 'appicon.ico'
FOLDER_SUFFIX = 'bin'
RELEASE_OWNER = 'LKumaresan'
BUNDLE_LEVEL = 3  # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = False
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
EXCLUDES = []
DLL_EXCLUDES = []
INCLUDES = ['sip', 'PyQt5.QtPrintSupport', 'PyQt5', 'win32com.client','numpy']
PACKAGES = ['kmxPyQt.devConsole3', 'PyQt5', 'win32com']

"""
EXCLUDES = ["PyQt5.uic.port_v3", "PyQt5.uic.port_v3.ascii_upper", "PyQt5.uic.port_v3.load_plugin", "PyQt5.uic.port_v3.proxy_base",
"PyQt5.uic.port_v3.encode_utf8", "PyQt5.uic.port_v3.string_io", "PyQt5.uic.port_v3.invoke", "uic.port_v3.ascii_upper",
"uic.port_v3.load_plugin", "uic.port_v3.proxy_base", "uic.port_v3.encode_utf8", "uic.port_v3.string_io",
"uic.port_v3.invoke", "uic.port_v3"]
"""

# PY2EXE PROCESS...
appVariable = {
                'name': APPNAME,
                'version': VERSION,
                'company_name': COMPANY_NAME,
                'copyright': COPYRIGHT,
                'description': DESCRIPTION
              }

if MAIN_SCRIPT_FILE: appVariable['script'] = MAIN_SCRIPT_FILE
if USE_ICON: appVariable['icon_resources'] = [(0, ICON_FILE)]

opVars = {
            "py2exe":{
                        "packages":PACKAGES,
                        "includes":INCLUDES,
                        "excludes":EXCLUDES,
                        "bundle_files": BUNDLE_LEVEL,
                        "dll_excludes":DLL_EXCLUDES,
                        "compressed": DO_COMPRESS,
                        "dist_dir":str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE) - 3]) + '_' + FOLDER_SUFFIX,
                     }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable], options=opVars, zipfile=1)
    else:
        setup(console=[appVariable], options=opVars)
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable], options=opVars, zipfile=1)
    else:
        setup(windows=[appVariable], options=opVars)

print ("\n\nEvery thing is fine!")
