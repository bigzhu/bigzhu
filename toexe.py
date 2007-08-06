#@+leo-ver=4-encoding=gb2312,.
#@+node:@file d:/BIGZHU/Python/python_project/toexe.py
#@@language python
"""打包生成exe文件,执行 toexe.py py2exe"""
from distutils.core import setup
import py2exe
import os
file = os.getcwd()+"\\get_cmfu.py"
setup(console=[file])
#@nonl
#@-node:@file d:/BIGZHU/Python/python_project/toexe.py
#@-leo
