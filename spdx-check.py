#! /usr/bin/env python3

# Copyright 2025 Andy Fingerhut
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import collections
import json
import os
import re

# TODO: This value should be read from the config file
default_license = 'Apache-2.0'

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
This program reads source files in a specified directory, and
recursively all of its subdirectories, checking that they have
SPDX-License-Identifier comment lines with the expected software
license ids.
""")
parser.add_argument('--root-dir', dest='rootdir', type=str)
parser.add_argument('--config-file', dest='configfile', type=str)
parser.add_argument('--verbosity', dest='verbosity', type=int, default=0)
args, remaining_args = parser.parse_known_args()

config = {}
if args.configfile:
    with open(args.configfile, 'r') as f:
        contents = f.read()
    config = json.loads(contents)

if 'ignored_suffixes' in config:
    config['ignored_suffixes'] = set(config['ignored_suffixes'])
else:
    config['ignored_suffixes'] = set()

def suffix_after_dot(s):
    """If the input string s contains a '.' character, return a string
    that is the part of s after the last '.' character.  If the input
    string contains no '.' character, return None."""
    match = re.search(r"\.([^.]*)$", s)
    if match:
        suffix = match.group(1)
    else:
        suffix = None
    return suffix

# Comment characters in various programming languages / configuration
# file formats:

# // - C, C++, Java, P4
# /* - C, C++, Java, P4
# # - Bash, Python
# " - Vim configuration file
# ;; - Emacs Elisp

def spdx_line_errors_warnings(lines):
    license_id_lines = []
    malformed_id_lines = []
    for line in lines:
        line = line.rstrip()
        if args.verbosity >= 4:
            partial_match = 'SPDX-License-Identifier' in line
            print("dbg partialmatch %s: %s" % (partial_match, line))
        if 'SPDX-License-Identifier' in line:
            match = re.search(r"""^\s*(#|\*|//|/\*|"|;;)?\s*SPDX-License-Identifier:\s+(.*)$""", line)
            if match:
                if args.verbosity >= 3:
                    print("dbg fullmatch True: %s" % (line))
                license_id_lines.append(line)
                license = match.group(2)
            else:
                if args.verbosity >= 3:
                    print("dbg fullmatch False: %s" % (line))
                malformed_id_lines.append(line)
    errors = []
    warnings = []
    if len(license_id_lines) > 1:
        msg = ("Found more than one (%d) SPDX-License-Identifier line"
               "" % (len(license_id_lines)))
        errors.append(msg)
    elif len(license_id_lines) == 0:
        msg = "Found no SPDX-License-Identifier line"
        errors.append(msg)
    if len(malformed_id_lines) != 0:
        msg = ("Found %d lines with SPDX-License-Identifier but incorrect syntax"
               "" % (len(malformed_id_lines)))
    if len(errors) == 0:
        errors = None
    if len(warnings) == 0:
        warnings = None
    if errors:
        license = None
    return errors, warnings, license


def walk_directory(path, config):
    spdx_errors = {}
    spdx_errors_filename_suffixes = collections.defaultdict(int)
    spdx_warnings = {}
    spdx_good = {}
    spdx_ignored_suffix = {}
    exception_reading = {}
    for root, dirs, files in os.walk(path):
        # TODO: The skipping of directories by name should be
        # configured in the config file in some way, not hard-coded.
        if (root[-5:] == '/.git') or ('/.git/' in root):
            # Ignore any files in a directory named .git, or its
            # subdirectories.
            if args.verbosity >= 3:
                print("Skipping .git directory: %s" % (root))
            continue
        for file_name in files:
            fullname = os.path.join(root, file_name)
            suffix = suffix_after_dot(file_name)
            #print("Suffix: %s File: %s" % (suffix, fullname))
            if suffix in config.get('ignored_suffixes', {}):
                spdx_ignored_suffix[fullname] = suffix
                continue
            try:
                with open(fullname, 'r') as f:
                    contents = f.read()
                lines = contents.splitlines()
            except Exception as e:
                exception_reading[fullname] = e
                continue
            # TODO: Generalize the following line to make the expected
            # license depend upon a configurable list of expected
            # licenses for a subset of the files.
            #expected_license = default_license
            if args.verbosity >= 3:
                print("Checking file: %s" % (fullname))
            errors, warnings, license = spdx_line_errors_warnings(lines)
            if errors:
                spdx_errors[fullname] = errors
                key = suffix
                if suffix is None:
                    key = "(none)"
                spdx_errors_filename_suffixes[key] += 1
            if warnings:
                spdx_warnings[fullname] = warnings
            if not (errors or warnings):
                spdx_good[fullname] = license

    for fullname in sorted(exception_reading.keys()):
        print("EXCEPTION: while reading file '%s': %s"
              "" % (fullname, exception_reading[fullname]))
    if args.verbosity >= 2:
        for fullname in sorted(spdx_ignored_suffix.keys()):
            print("IGNORED SUFFIX: %s: %s" % (spdx_ignored_suffix[fullname],
                                              fullname))
    if args.verbosity >= 1:
        for fullname in sorted(spdx_errors.keys()):
            for msg in spdx_errors[fullname]:
                print("ERROR: %s: %s" % (fullname, msg))
        for fullname in sorted(spdx_warnings.keys()):
            for msg in spdx_warnings[fullname]:
                print("WARNING: %s: %s" % (fullname, msg))
    if args.verbosity >= 2:
        for fullname in sorted(spdx_good.keys()):
            print("GOOD: %s: %s" % (spdx_good[fullname], fullname))

    print("Found %d files where exception occurred while reading its contents" % (len(exception_reading)))
    print("Found %d files where SPDX check was skipped because of file name suffix" % (len(spdx_ignored_suffix)))
    print("Found %d files with errors" % (len(spdx_errors)))
    for suffix in sorted(spdx_errors_filename_suffixes.keys()):
        print("    %d error files has file name suffix '.%s'"
              "" % (spdx_errors_filename_suffixes[suffix], suffix))
    print("Found %d files with warnings" % (len(spdx_warnings)))
    print("Found %s files with neither errors nor warnings" % (len(spdx_good)))


rootdir = "."
if args.rootdir:
    rootdir = args.rootdir

walk_directory(rootdir, config)
