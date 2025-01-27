# Introduction

This directory contains early testing versions of spdx-check.py
configuration files for use with various Github repositories in the
https://github.com/p4lang organization.

Their file names are of the form:

+ spdx-checker-config-REPONAME.json

where REPONAME is replaced with the name of the repository, e.g. `p4c`
for https://github.com/p4lang/p4c


# File types where it is difficult or impossible to include SPDX-License-Identifier lines

A few p4lang repositories use `.patch` or `.diff` as a file name
suffix for files containing the output of `diff` or similar programs
that can be applied via the command `patch`.  These cannot have
comments added to them.

Text files with a file name suffix like `.txt` are almost never source
files.  They are usually documentation.  It is reasonable that they do
not include SPDX-License-Identifier lines.

Similarly for Github Markdown files with suffix `.md`.  It _is_
possible to put comments in them that do not appear when displayed on
Github web pages, but this seems like an unnecessary step to take for
documentation files.

JSON data files cannot have comments [1].  These most often have a
file name suffix of `.json`, but in p4lang repositories some of them
use a suffix of `.conf`, e.g. when the file is used as input to a P4
DPDK or Tofino bf_switchd program.

[1] https://www.freecodecamp.org/news/comments-in-json/

`.gitignore` files might be able to have comments, but it seems like
busy-work to include SPDX-License-Identifier lines in such files.
Similarly for `.gitmodules` files.

Binary image and document file formats _might_ in some cases provide a
way to embed comments in them, but since they are not program source
files, even when it is possible it seems like busy-work to try to
include SPDX-License-Identifier lines within such a file.  Common
suffixes for these used within p4lang repositories include:

+ `.a` - executable code archive
+ `.DS_Store` - Apple Desktop Service Store
+ `.docx` - Microsoft Word 2007+
+ `.eot` - Embedded OpenType
+ `.gif`
+ `.gpg` - OpenPGP Public Key
+ `.gz`
+ `.ico` - MS Windows icon resource
+ `.jar` - Java Archive, uses Zip archive format
+ `.jpg`
+ `.mov` - ISO Media, Apple QuickTime movie
+ `.mp4`
+ `.odg` - OpenDocument Drawing
+ `.odp` - OpenDocument Presentation
+ `.otf` - OpenType font data
+ `.pdf`
+ `.png`
+ `.pptx`
+ `.so` - binary shared object library
+ `.ttf` - TrueType Font data
+ `.vsdx` - Microsoft Visio
+ `.whl` - Zip archive data used by Python/pip
+ `.woff` - Web Open Font Format
+ `.woff2` - Web Open Font Format (Version 2)
+ `.zip`

Other binary data file formats appearing in at least some p4lang
repositories:

+ `.pcap`
+ `.bin`

Some text data file formats are at least tricky to add comments to, or
very specific to the library used to manipulate the file format.  It
also seems more trouble than it is worth to require that they have an
SPDX-License-Identifier line:

+ `.adoc` - AsciiDoc source file, used for P4 specification documents
+ `.csv`
+ `.drawio` - based on XML.  See `.xml`.
+ `.graphml` - based on XML.  See `.xml`.
+ `.htm`
+ `.html`
+ `.less` - several in p4lang.github.io repo.  Some kind of HTML / web
  page development data file format, I think.
+ `.mdk` - Madoko source files, still used in some older repos that we
  might never update.
+ `.p4-error` - An expected output file used only for CI testing in p4c repo.
+ `.p4-stderr` - An expected output file used only for CI testing in p4c repo.
+ `.spec` - An expected output file produced as output from `p4c-dpdk`
  compiler back end.  Mostly checked in only when used for CI testing
  in p4c repo.
+ `.svg` - based on XML.  See `.xml`.
+ `.toml` - Based on Windows INI file format.  Can have comments, but
  only appears to be used in p4lang repos for developers of languages
  like Python and Rust, for the development tools of those programming
  languages.
+ `.xml` - possible to have comments, but seems low value to add
  SPDX-License-Identifier comments
