# Introduction


# C/C++ libaries

This article lists several libraries that are used by at least one
p4lang project, what their license is, and the Github page for the
project, if it has one.

+ Abseil Common Libraries (C++)
  + https://github.com/abseil/abseil-cpp
  + SPDX license: Apache-2.0
  + License: https://github.com/abseil/abseil-cpp/blob/master/LICENSE
  + Used by repositories: p4c-executables
+ bdwgc - The Boehm-Demers-Weiser conservative C/C++ Garbage Collector
  (also known as bdw-gc, boehm-gc, libgc)
  + https://github.com/ivmai/bdwgc
  + License: "MIT-style" https://github.com/ivmai/bdwgc/blob/master/LICENSE
  + Used by repositories: p4c-executables
+ behavioral-model - BMv2 software switch
  + https://github.com/p4lang/behavioral-mode
  + SPDX license: Apache-2.0
  + Used by repositories: p4c-tests-only
+ Boost C++ Libraries
  + https://github.com/boostorg/boost
  + https://www.boost.org
  + SPDX license: BSL-1.0
  + Used by repositories: p4c-executables
+ GoogleTest
  + https://github.com/google/googletest.git
  + SPDX license: BSD-3-Clause
  + License: https://github.com/google/googletest/blob/main/LICENSE
  + Used by repositories: p4c-tests-only
+ Inja - A Template Engine for Modern C++
  + https://github.com/pantor/inja.git
  + SPDX license: MIT ?
  + License: https://github.com/pantor/inja/blob/main/LICENSE
  + Used by repositories: p4c (executables?  OK if so, since MIT license is compatible)
+ libbpf
  + SPDX liecnse: (LGPL-2.1 OR BSD-2-Clause)
  + License: https://github.com/libbpf/libbpf/blob/master/LICENSE
  + Used by repositories: p4c-executables (at least ebpf back end?
    BSD-2-Clause license is compatible, so fine even if linked into
    p4c-executables)
+ P4Runtime
  + https://github.com/p4lang/p4runtime
  + SPDX license: Apache-2.0
  + Used by repositories: p4c-executables
+ Protocol buffers - 
  + https://github.com/protocolbuffers/protobuf
  + SPDX license: BSD-3-Clause
  + License: https://github.com/protocolbuffers/protobuf/blob/main/LICENSE
    + I have ediff'ed that license file and it is nearly word-for-word
      identical with BSD-3-Clause, except for "Google Inc" in place of
      "the copyright owner".
  + Used by repositories: p4c-executables
+ spdlog - Fast C++ logging library
  + https://github.com/gabime/spdlog
  + SPDX license: MIT ?
  + License: https://github.com/gabime/spdlog/blob/v1.x/LICENSE
  + Used by repositories: p4c-executables (at least Tofino back end)
+ Z3 - The Z3 Theorem Prover
  + https://github.com/Z3Prover/z3
  + SPDX license: MIT
  + Used by repositories: p4c-executables (at least p4testgen)


# Python modules

## Python modules with a PyPI page

+ grpc
  + https://pypi.org/project/grpc/
  + SPDX License: Apache-2.0
  + License: https://github.com/grpc/grpc/blob/master/LICENSE
+ jsl
  + JSL is a Python DSL for defining JSON Schemas.
  + https://pypi.org/project/jsl/
  + https://github.com/aromanovich/jsl
  + SPDX License: BSD-3-Clause
  + License: https://github.com/aromanovich/jsl/blob/master/LICENSE
+ jsonschema
  + An implementation of JSON Schema validation for Python
  + https://pypi.org/project/jsonschema/
  + https://github.com/python-jsonschema/jsonschema
  + SPDX License: MIT
  + License: https://github.com/python-jsonschema/jsonschema/blob/main/COPYING
+ matplotlib
  + https://pypi.org/project/matplotlib/
  + "Matplotlib only uses BSD compatible code"  https://matplotlib.org/stable/project/license.html
+ numpy
  + https://pypi.org/project/numpy/
  + SPDX License: BSD-3-Clause
  + License: https://github.com/numpy/numpy/blob/main/LICENSE.txt
+ pandas
  + https://pypi.org/project/pandas/
  + SPDX License: BSD-3-Clause
  + License: https://github.com/pandas-dev/pandas/blob/main/LICENSE
+ ply
  + Python Lex-Yacc
  + https://pypi.org/project/ply/
  + https://github.com/dabeaz/ply
  + License: Looks like BSD-3-Clause (TODO verify)
+ pyroute2
  + https://pypi.org/project/pyroute2/
  + SPDX license: (GPL-2.0-or-later OR Apache-2.0)
  + License: https://github.com/svinota/pyroute2/blob/master/LICENSE
+ schemas part of jsonschema?
  + https://pypi.org/project/schemas/
+ scapy - GPL-2.0-only
  + https://pypi.org/project/scapy/
  + https://github.com/secdev/scapy
  + SPDX license: GPL-2.0-only
  + License: https://github.com/secdev/scapy/blob/master/LICENSE
+ seaborn
  + https://pypi.org/project/seaborn/
  + https://github.com/mwaskom/seaborn
  + SPDX License: BSD-3-Clause
  + License: https://github.com/mwaskom/seaborn/blob/master/LICENSE.md
  + Other licenses: https://github.com/mwaskom/seaborn/tree/master/licences


## Standard modules included with Python, licensed same as Python

Standard Python packages documented on official Python docs page, so
they should all be under the same license as Python itself:

+ argparse
+ codecs
+ collections
+ copy
+ datetime
+ difflib
+ enum
+ errno
+ fnmatch
+ functools
+ getopt
+ glob
+ importlib
+ inspect
+ itertools
+ json
+ logging
+ math
+ multiprocessing
+ operator
+ os
+ os.path
+ pathlib
+ queue
+ random
+ re
+ shlex
+ shutil
+ signal
+ socket
+ stat
+ string
+ subprocess
+ sys
+ sysconfig
+ tempfile
+ testutils
+ threading
+ time
+ traceback
+ typing
+ unicodedata
+ uuid
+ xml


# TODO: Golang packages



# SPDX license identifers

+ Apache-2.0 "Apache License 2.0" https://spdx.org/licenses/Apache-2.0.html
+ BSD-2-Clause "BSD 2-Clause "Simplified" License" https://spdx.org/licenses/BSD-2-Clause.html
+ BSD-3-Clause "BSD 3-Clause "New" or "Revised" License" https://spdx.org/licenses/BSD-3-Clause.html
+ BSL-1.0 "Boost Software License 1.0" https://spdx.org/licenses/BSL-1.0.html
+ FSFAP "FSF All Permissive License" https://spdx.org/licenses/FSFAP.html
+ GPL-2.0-only "GNU General Public License v2.0 only" https://spdx.org/licenses/GPL-2.0-only.html
+ MIT "MIT License" https://spdx.org/licenses/MIT.html


## Boost BSL-1.0

I have checked on 2025-Feb-15 that the contents of the two licenses on
these two pages are identical except for whitespace differences.

+ https://www.boost.org/users/license.html
+ https://spdx.org/licenses/BSL-1.0.html

```
Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```
