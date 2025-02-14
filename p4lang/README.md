# Introduction

This article contains a list of questions, and hopefully soon
authoritative answers, to guide the choice of what software licenses
to use for source files in all repositories in the
https://github.com/p4lang Github organization.

The P4 Consortium's preferred choice of software license is Apache
2.0.

There must be a compelling reason to choose a different license for
any source file.

Using Apache 2.0 enables source files with that license to be combined
with proprietary source code written by various corporations and
individuals, and for those entities to release binaries of programs
that were compiled from those Apache 2.0 licensed source files
(e.g. of a proprietary P4 compiler for a corporation's custom ASIC
design).


## Is it acceptable for a repository to have a mix of some files with one license, and other files with other licenses?

We very much hope the answer is yes.

For example, we expect we will need to have a very small number of
source files in this repository https://github.com/p4lang/p4c be
licensed under GPL-2.0-only, because of one of two reasons:

+ They are test programs written in Python that import the GPL v2
  Scapy library.
+ They are C source files that are expected to be compiled, loaded
  into the Linux kernel via EBPF, and executed.

We expect 99% or so of the source files in that repository to be
licensed under the Apache-2.0 license.


## If yes, what should the top level LICENSE file contain?

Is a file like this one acceptable, which mentions all licenses used
by any file in the repository, and a way to distinguish which source
files use which license?

+ https://github.com/p4lang/p4app-TCP-INT/blob/main/LICENSE


## Anything else we should do for such mixed-license repositories?


## What are recommended rules for mixing different license files?

From our limited research, it appears that it is very legally
questionable whether mixing GPL-2.0-only and Apache-2.0 files in the
same executable program is allowed.

+ https://github.com/p4lang/p4c/pull/5110/files#diff-f137a4759c2186ea8e241cf59e0610f4f0d03f343b48b0bb68d0e79f9797e019

Our tentative conclusion: Do not mix such licenses.

We believe "Program A released under license X" being combined with the code of "Program/library B released under license Y" in any of these ways:

+ C/C++ include, static linking, or dynamic linking
+ Python import

is acceptable to release program A under license X for the following
combinations of licenses X, Y:


| license X  | license Y is Apache-2.0 | license Y is BSD-3-Clause, BSD-2-Clause, MIT, FSFAP | license Y is GPL-2.0-only |
| ---------- | ---------- | -------------------------------------- | ------------ |
| Apache-2.0 | yes (same) | yes (compatible)                       | no (legally questionable) |
| BSD-3-Clause, BSD-2-Clause, MIT, FSFAP | yes (compatible) | yes (compatible) | no (program A must be released as GPL-2.0-only)
| GPL-2.0-only | no (legally questionable) | yes (compatible)      | yes (same) |

Example 1: Several test Python programs in the
https://github.com/p4lang/p4c repository import the Scapy library,
released as GPL-2.0-only.  We will make these test Python programs
GPL-2.0-only.

Example 2: We want to support the ability of a Python test program A
to import the Scapy library (see Example 1), and also import the
Python `ptf` module in https://github.com/p4lang/ptf

Because of Example 1, A should be licensed as GPL-2.0-only.  Releasing
`ptf` under the BSD-3-Clause license would allow this.

Example 3: We also want to support the ability of a Python test
program B that does _not_ import the Scapy library to import `ptf`,
and to release B under an Apache-2.0 or BSD-3-Clause license
(developer's choice).

Releasing `ptf` under the BSD-3-Clause license would allow this.

Note: There are other choices of license besides BSD-3-Clause for
`ptf` that support both Example 2 and Example 3, but note that
Apache-2.0 is _not_ one of them.


### EBPF program laoded into Linux kernel

These should be GPL-2.0-only.


### Programs included by generated EBPF programs

These should be GPL-2.0-only or BSD-3-Clause.

We plan to make them BSD-3-Clause if they are included from EBPF
programs, and also from user-space programs that will interact with
the in-kernel EBPF programs.
