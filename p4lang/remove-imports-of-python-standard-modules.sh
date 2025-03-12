#! /bin/bash

# This script is intended to be run in a way similar to this, on an
# input file that contains Python lines of source code containing the
# word 'import'.  The intent is to remove lines that only import
# modules that are included as part of Python, and thus distributed
# under the same license as Python.

# find . ! -type d -print0 | xargs -0 egrep '\bimport\b' | $SPDX/p4lang/remove-imports-of-python-standard-modules.sh

# Here is a list of the strings it checks for, each on a line by
# themselves, sorted, for easier human reading:

# __future__
# argparse
# asyncio
# atexit
# binascii
# builtins
# codecs
# collections
# concurrent
# copy
# csv
# ctypes
# datetime
# difflib
# enum
# errno
# fcntl
# filecmp
# fileinput
# fnmatch
# functools
# getopt
# glob
# hashlib
# importlib
# inspect
# io
# ipaddress
# itertools
# json
# keyword
# logging
# math
# multiprocessing
# operator
# os
# os, sys
# os.path
# pathlib
# pdb
# pickle
# platform
# pprint
# pty
# pydoc
# queue
# random
# re
# readline
# select
# setuptools
# six
# shlex
# shutil
# signal
# socket
# socket, sys
# stat
# string
# struct
# subprocess
# sys
# sysconfig
# tarfile
# tempfile
# testutils
# textwrap
# threading
# time
# traceback
# types
# typing
# unicodedata
# unittest
# unittest.mock
# uuid
# warnings
# xml
# xml.etree.ElementTree


egrep -v 'import (__future__|argparse|asyncio|atexit|binascii|builtins|codecs|collections|concurrent|copy|csv|ctypes|datetime|difflib|enum|errno|fcntl|filecmp|fileinput|fnmatch|functools|getopt|glob|hashlib|importlib|inspect|io|ipaddress|itertools|json|keyword|logging|math|multiprocessing|operator|os|os, sys|os.path|pathlib|pdb|pickle|platform|pprint|pty|pydoc|queue|random|re|readline|select|setuptools|six|shlex|shutil|signal|socket|socket, sys|stat|string|struct|subprocess|sys|sysconfig|tarfile|tempfile|testutils|textwrap|threading|time|traceback|types|typing|unicodedata|unittest|unittest.mock|uuid|warnings|xml|xml.etree.ElementTree)( as .*)?\s*$' | egrep -v 'from (__future__|argparse|asyncio|atexit|binascii|builtins|codecs|collections|concurrent|copy|csv|ctypes|datetime|difflib|enum|errno|fcntl|filecmp|fileinput|fnmatch|functools|getopt|glob|hashlib|importlib|inspect|io|ipaddress|itertools|json|keyword|logging|math|multiprocessing|operator|os|os, sys|os.path|pathlib|pdb|pickle|platform|pprint|pty|pydoc|queue|random|re|readline|select|setuptools|six|shlex|shutil|signal|socket|socket, sys|stat|string|struct|subprocess|sys|sysconfig|tarfile|tempfile|testutils|textwrap|threading|time|traceback|types|typing|unicodedata|unittest|unittest.mock|uuid|warnings|xml|xml.etree.ElementTree) import ' | egrep -v '\.py:# '
