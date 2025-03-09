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


## Recommendations for Copyright notice author

Suppose a file has multiple authors.  Is it acceptable if the
copyright line in the source file says:

```
// Copyright 2025 The P4 Consortium
```

and then have a top level file CONTRIBUTING in the repository that
lists individual contributors?


## Recommendations for Copyright notice year

Is it acceptable for a year in a copyright notice to be
`2013-present`?

If a source file was originally added in 2024, then modified in 2025,
is it acceptable to leave the year as `2024`?  Or should it be changed
to `2024-2025`?

Should that extend to things like `2024-2025, 2027, 2030` if the file
is modified only in years 2025, 2027, and 2030?


## Is it acceptable for a repository to have a mix of some files with one license, and other files with other licenses?

We very much hope the answer is yes.

For example, we expect we will need to have a very small number of
source files in this repository https://github.com/p4lang/p4c be
licensed under GPL-2.0-only, because of one of these reasons:

+ They are test programs written in Python that import the
  GPL-2.0-only Scapy module.
+ They are C source files that are expected to be compiled, loaded
  into the Linux kernel via EBPF, and executed.

We expect 99% or so of the source files in that repository to be
licensed under the Apache-2.0 license.

Responses from [1]:

+ It may be acceptable, but not recommended unless all licenses are
  compatible.  For example, if you have some GPL licensed files and
  the rest of the repo is under Apache, there is a higher risk for a
  license conflict by your team or by a downstream user.  I recommend
  that you put the GPL files in a separate repo if possible, or at
  least put them in a separate directory, and then clearly make note
  if this in both the LICENSE and README files.
+ Also, you must be sure that the GPL files are not combined in any
  way with the rest of your project code.  If they are completely
  stand-alone executables they should be OK (or mixed with other GPL
  code as you describe), otherwise they will contaminate your
  codebase.


## If yes, what should the top level LICENSE file contain?

Is a file like this one acceptable, which mentions all licenses used
by any file in the repository, and a way to distinguish which source
files use which license?

+ https://github.com/p4lang/p4app-TCP-INT/blob/main/LICENSE

Response from [1]:

+ The top level repo license you have is OK.  I also recommend that
  you have a NOTICE.md file with license info for any files which are
  not authored by your project.


## Anything else we should do for such mixed-license repositories?


## What are recommended rules for mixing different license files?

From our limited research, it appears that it is very legally
questionable whether mixing GPL-2.0-only and Apache-2.0 files in the
same executable program is allowed.

+ https://github.com/p4lang/p4c/pull/5110/files#diff-f137a4759c2186ea8e241cf59e0610f4f0d03f343b48b0bb68d0e79f9797e019

Our tentative conclusion: Do not mix such licenses.

Response from [1]:

+ Most experts consider these 2 licenses [Apache-2.0 and GPL-2.0-only]
  to be incompatible.  At best all code will need to be released under
  GPL2 and more likely it causes a direct license conflict and is not
  allowed.


We believe "Program A released under license X" being combined with
the code of "Program/library B released under license Y" in any of
these ways:

+ C/C++ include, static linking, or dynamic linking
+ Python import

is acceptable to release program A under license X for the following
combinations of licenses X, Y:


| license X  | license Y is Apache-2.0 | license Y is BSD-3-Clause, BSD-2-Clause, MIT, FSFAP, BSL-1.0 | license Y is GPL-2.0-only |
| ---------- | ---------- | -------------------------------------- | ------------ |
| Apache-2.0 | yes (same) | yes (compatible)                       | no (legally questionable) |
| BSD-3-Clause, BSD-2-Clause, MIT, FSFAP, BSL-1.0 | yes (compatible) | yes (compatible) | no (program A must be released as GPL-2.0-only) |
| GPL-2.0-only | no (legally questionable) | yes (compatible)      | yes (same) |

Example 1: Several standalone test Python programs in the
https://github.com/p4lang/p4c repository import the Scapy library,
released as GPL-2.0-only.  We will make these test Python programs
GPL-2.0-only.  There are only six of these files as of 2025-Feb-28 in
that repository.  There are more such Python test programs in other
https://github.com/p4lang repositories that are for educational
purposes, so not as critical as the p4c repo.

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
Apache-2.0 is _not_ one of them.  Another example would be to release
`ptf` under a dual license of Apache-2.0 or GPL-2.0-only, at the
user's choice.

Question for P4 Consortium engineers: Are there _other_ Python
modules, currently released under Apache-2.0, that are similar to
`ptf` as described above?  It seems likely that there are.


### Important exceptions: LGPL and GCC runtime libraries

We frequently make use of header files and dymamic linking to shared
libraries released under the LGPL-2.1 license, and include header
files released with the "GCC Runtime Library Exception", e.g. Linux
header files that have this text in their comments:

```
Under Section 7 of GPL version 3, you are granted additional
permissions described in the GCC Runtime Library Exception, version
3.1, as published by the Free Software Foundation.
```

Those wishing to release executable binaries without being required to
release source code should avoid statically linking to libraries
released under the LGPL, by only dynamically linking to them.
Alternately, they can statically link with other compatible libraries
that provide similar functionality, e.g. `musl libc`.

+ https://www.musl-libc.org/


### EBPF program laoded into Linux kernel

These should be GPL-2.0-only.


### Programs included by generated EBPF programs

These should be GPL-2.0-only or BSD-3-Clause.

We plan to make them BSD-3-Clause if they are included from EBPF
programs, and also from user-space programs that will interact with
the in-kernel EBPF programs.


# References

[1] 2025-Feb-23 email from Jeff Shapiro, a license specialist at the
    Linux Fopundation, but not an intellectual property lawyer.
