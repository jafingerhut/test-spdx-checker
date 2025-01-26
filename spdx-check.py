#! /usr/bin/env python3

# Copyright 2025 Andy Fingerhut
# SPDX-License-Identifier: BSD-3-Clause

import os
import re

default_license = 'Apache-2.0'
#verbosity = 2
verbosity = 0

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

def spdx_line_errors_warnings(lines, expected_license):
    license_id_lines = []
    malformed_id_lines = []
    for line in lines:
        line = line.rstrip()
        if verbosity >= 4:
            partial_match = 'SPDX-License-Identifier' in line
            print("dbg partialmatch %s: %s" % (partial_match, line))
        if 'SPDX-License-Identifier' in line:
            match = re.search(r"^\s*(#|\*|//|/\*)?\s*SPDX-License-Identifier:\s+(.*)$", line)
            if match:
                if verbosity >= 3:
                    print("dbg fullmatch True: %s" % (line))
                license_id_lines.append(line)
                license = match.group(2)
            else:
                if verbosity >= 3:
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


def walk_directory(path, default_license):
    spdx_errors = {}
    spdx_warnings = {}
    spdx_good = {}
    for root, dirs, files in os.walk(path):
        #print("Current directory:", root)
        #for dir_name in dirs:
        #    print("Subdirectory:", dir_name)
        if (root[-5:] == '/.git') or ('/.git/' in root):
            # Ignore any files in a directory named .git, or its
            # subdirectories.
            if verbosity >= 3:
                print("Skipping .git directory: %s" % (root))
            continue
        for file_name in files:
            suffix = suffix_after_dot(file_name)
            fullname = os.path.join(root, file_name)
            #print("Suffix: %s File: %s" % (suffix, fullname))
            try:
                with open(fullname, 'r') as f:
                    contents = f.read()
                lines = contents.splitlines()
            except Exception as e:
                print("Exception occurred while reading file '%s': %s"
                      "" % (fullname, e))
                continue
            # TODO: Generalize the following line to make the expected
            # license depend upon a configurable list of expected
            # licenses for a subset of the files.
            expected_license = default_license
            if verbosity >= 3:
                print("Checking file: %s" % (fullname))
            errors, warnings, license = spdx_line_errors_warnings(
                lines, expected_license)
            if errors:
                spdx_errors[fullname] = errors
            if warnings:
                spdx_warnings[fullname] = warnings
            if not (errors or warnings):
                spdx_good[fullname] = license

    if verbosity >= 1:
        for fullname in sorted(spdx_errors.keys()):
            for msg in spdx_errors[fullname]:
                print("ERROR: %s: %s" % (fullname, msg))
        for fullname in sorted(spdx_warnings.keys()):
            for msg in spdx_warnings[fullname]:
                print("WARNING: %s: %s" % (fullname, msg))
        for fullname in sorted(spdx_good.keys()):
            print("GOOD: %s: %s" % (spdx_good[fullname], fullname))
    print("Found %d files with errors" % (len(spdx_errors)))
    print("Found %d files with warnings" % (len(spdx_warnings)))
    print("Found %s files with neither errors nor warnings" % (len(spdx_good)))


walk_directory("./", default_license)
