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

We hope the answer is yes.


## If so, what should the top level LICENSE file contain?

Is a file like this one acceptable?

+ https://github.com/p4lang/p4app-TCP-INT/blob/main/LICENSE


## Anything else we should do for such mixed-license repositories?


## What are recommended rules for mixing different license files?

From our limited research, it appears that it is very legally
questionable whether mixing GPL v2 and Apache 2.0 files in the same
executable program is allowed.

+ https://github.com/p4lang/p4c/pull/5110/files#diff-f137a4759c2186ea8e241cf59e0610f4f0d03f343b48b0bb68d0e79f9797e019

Our tentative conclusion: Do not mix such licenses.

We believe it is acceptable for a GPLv2 program to include a
BSD-3-Clause library/header file.

Rules we hope to follow are described in the following subsections.


### One of our programs includes a GPL-2.0-only library

If A includes B, and B is GPL-2.0-only (chosen by someone else),
release A as GPL-2.0-only.

Example: Several test Python programs in the
https://github.com/p4lang/p4c repository import the Scapy library,
released as GPL-2.0-only.  We will make these test Python programs
GPL-2.0-only.

+ https://github.com/p4lang/p4c/pull/5111


### One of our programs includes a GPL-2.0-only library, and also one of our libraries

If A includes both B and C, and B is GPL-2.0-only (chosen by someone
else), release A as GPL-2.0-only, and C as BSD-3-Clause.  This allows
another program D to include C, with D released as Apache-2.0.

Example: A few Python test programs in p4lang repositories import
Scapy, and also a p4lang library https://github.com/p4lang/ptf We will
make those test Python programs GPL-2.0-only, and the ptf package
BSD-3-Clause.


### EBPF program laoded into Linux kernel

These should be GPL-2.0-only.


### Programs included by generated EBPF programs

These should be GPL-2.0-only or BSD-3-Clause.

We plan to make them BSD-3-Clause if they are included from EBPF
programs, and also from user-space programs that will interact with
the in-kernel EBPF programs.
