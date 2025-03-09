# Introduction

The `ptf` library [1] is often used for writing automated tests for P4
programs.

[1] https://github.com/p4lang/ptf

This article attempts to address these questions:

+ What software license is it legal to release `ptf`'s source files
  under?
+ What software license should be used on Python source files that
  import `ptf`?


# Summary of current best guess at correct answers

TODO


# Origin of `ptf` package

The `ptf` repository [1] had its first commit of source files in
2015-Sep.

The commit comment says that it is a subset of code copied from a
project named `oftest`, which is still available in 2025 in a public
Github repo [2].  As of 2025-Feb, `oftest` has not been updated since
2021.

[2] https://github.com/floodlight/oftest

I have done a comparison of these versions of the repositories:

[3] https://github.com/floodlight/oftest commit
```
commit 23ab62fc31df6cb35e57ce37e4e9331048547fa2 (HEAD)
Author: Harshmeet Singh <harshmeet.singh@bigswitch.com>
Date:   Tue Aug 25 15:42:36 2015 -0700
```

[4] https://github.com/p4lang/ptf commit
```
commit 41a3934a5a16a432a56ed272016bc366c09bca5d (HEAD)
Author: Antonin Bas <antonin@barefootnetworks.com>
Date:   Tue Sep 15 16:54:18 2015 -0700
```

[4] is the first commit of the `ptf` repository.  The commit mentioned
at [3] is about as close in date as I can find to the first commit of
the `ptf` repository.

WARNING: I have searched the entire commit history of [3] from that
commit back to the beginning of the repository's history, using the
command `git log -p .`.  I have searched the output of that command
for the "copyleft signal" terms listed below.  The list below shows
the only files that mention any of those terms anywhere in their
history:

+ `src/python/oftest/mpls.py` - This file is not in [4], so no issue
  here.
+ `src/python/oftest/netutils.py` - see below for a from-scratch
  replacement that has been developed for this file in 2025.
+ `doc/Doxyfile` - This is not part of the files copied to [4], so no
  issue here.
+ an older version of `src/python/setup.py` mentioned GPL, but was
  later removed.  Also this file was not copied to [4].

Copyleft signal terms:
+ gnu, case insensitive
+ gpl, case insensitive
+ 'general public', case insensitive

WARNING: Files in [4] that are under copyleft licenses:

+ src/python/oftest/netutils.py - See below for a proposed Apache-2.0
  replacement.

Files:

+ [3] platforms/eth.py vs. [4] file platforms/eth.py - mostly the same
+ [3] platforms/local.py vs. [4] file platforms/local.py - identical
+ [3] platforms/remote.py vs. [4] file platforms/remote.py - identical
+ [3] oft vs. [4] ptf - many small changes, but many more lines copied
  unchanged than there are changed.  Clearly derived.
+ [3] src/python/oftest/dataplane.py vs. [4] src/ptf/dataplane.py -
  most lines identical.  A few small changes.  Clearly derived.
+ [3] src/python/oftest/base_tests.py vs. [4] src/ptf/base_tests.py -
  many lines deleted from [3] to make [4], but many remaining lines
  identical.  Clearly derived.
+ [3] src/python/oftest/netutils.py vs. [4] src/ptf/netutils.py -
  identical files.  NOTE: The original from oftest says it is copied
  and modified from a source file in Scapy, so is GPLv2.  The file in
  [2] that it was copied from also says it is GPLv2 (committed by Dan
  Talayco in 2010!).  See https://github.com/p4lang/ptf/pull/211 for a
  proposed change to this file that reimplements the functions used
  elsewhere, especially `set_promisc`, with versions that can be
  released under Apache-2.0.
+ [3] src/python/oftest/testutils.py vs. [4] src/ptf/testutils.py -
  Several functions removed, several functions added, several methods
  modified, but clearly [4] is derived from [3].
+ [3] src/python/oftest/__init__.py vs. [4] src/ptf/__init__.py -
  identical
+ [3] src/python/oftest/pcap_writer.py vs. [4]
  src/ptf/pcap_writer.py - identical
+ [3] src/python/oftest/afpacket.py vs. [4] src/ptf/afpacket.py -
  identical
+ [3] src/python/oftest/packet.py vs. [4] src/ptf/packet.py - [4] is a
  superset of [3], adding run-time dynamic checking for Scapy support
  of a few additional types of headers.
+ [3] src/python/oftest/parse.py vs. [4] src/ptf/parse.py - [4] is a
  subset of [3], but that subset is identical to part of [3].
+ [3] src/python/oftest/ofutils.py vs. [4] src/ptf/ptfutils.py -
  identical except for 2 lines that differ only in renaming 'oft' to
  'ptf'.
+ [3] (nothing) vs. [4] src/ptf/thriftutils.py - This file is new in
  [4], and all of the Python function names it contains exist nowhere
  in [3].  Originally committed by Antonin Bas in 2015, so seems
  likely it was written by him.


# The license under which most of the `oftest` repository is released

As mentioned in the previous section, a few files in `oftest` are
copyleft.

However, most of them are released under this license:

+ [5] https://github.com/floodlight/oftest/blob/master/LICENSE

That document contains this URL:

+ http://www.openflowswitch.org/wp/legal/

As of 2025-Feb, that URL gets a 404 Page not found response.

Here is a version of that page retrieved and stored by the Internet
Archive Wayback Machine on 2011-Feb-12:

+ [6] https://web.archive.org/web/20110212091439/http://www.openflowswitch.org/wp/legal/

I have compared the latest version of [5] against [6], and the license
portion of it is identical.  One has a copyright year of 2008 and the
other 2010.

TODO: Which of the licenses on SPDX's license list [7] is this license
most similar to?

+ [7] https://spdx.org/licenses/
