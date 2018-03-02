#!/usr/bin/env python

from __future__ import print_function

import sys
import glob
import os.path
from distutils.core import setup

assert sys.version_info[0]==2 and sys.version_info[1]>=7,\
    "you must install and use OCRopus with Python version 2.7 or later, but not Python 3.x"

#pretraining = [c for c in glob.glob("pretraining/models/*.pyrnn.gz")]
#pretraining.extend("pretraining/whitelist.txt")
scripts = [c for c in glob.glob("ocropus-*") if "." not in c and "~" not in c]
scripts.extend([c for c in glob.glob("mptv/mptv-*") if "." not in c and "~" not in c])

print(scripts)

setup(
    name = 'mptv',
    version = 'v1.3.3',
    author = "Christian Reul",
    description = "Bla",
    packages = ["ocrolib"],
    #data_files= [('share/mptv', pretraining)],
    scripts = scripts,
    )
