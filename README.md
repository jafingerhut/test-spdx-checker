# Introduction

This repository contains the source code of a simple Python program
`spdx-check.py` that tests source files for the existence of
'SPDX-License-Identifier' lines, and prints errors and/or warnings
messages if it finds files that do not contain them, contain more than
one, or contain other issues.

More information about SPDX-License-Identifier lines in source files:
+ https://spdx.dev/learn/handling-license-info/
+ https://spdx.org/licenses/

This repository also contains some dummy source files that exercise
`spdx-check.py`, and checks that it produces the expected output.
