# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

setup(
    console=['CherryWeChatSwever.py'],
    options={
        "py2exe": {
            "packages": [ "ext.mako","ext.cherrypy"],
            "bundle_files": 1,
            "compressed": True,
            #"includes": ['lxml._elementpath']
            "includes": includes
        }
    },
    zipfile=None
)