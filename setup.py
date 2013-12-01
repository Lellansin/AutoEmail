from distutils.core import setup  
import py2exe  
  
setup(
	version = "1.0",
	name = "Auto Email",
	description = "Auto Email Assistant",
    options = {  
      "py2exe": {  
        "dll_excludes": ["MSVCP90.dll"],  
        "includes":["sip"]
      }
    },
    windows=[{"script": "main.py"}]
 )
 