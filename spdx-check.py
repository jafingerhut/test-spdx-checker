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
# % - LaTeX source file

def spdx_line_errors_warnings(lines, config):
    license_id_lines = []
    malformed_id_lines = []
    generated_file_lines = []
    generated_file_signatures = config.get('generated_file_signature', [])
    license = None
    generated_file = False
    all_lines_blank = True
    for line in lines:
        line = line.rstrip()
        if line != "":
            all_lines_blank = False
        if args.verbosity >= 4:
            partial_match = 'SPDX-License-Identifier' in line
        if 'SPDX-License-Identifier' in line:
            match = re.search(r"""^\s*(#|\*|//|/\*|"|;;|%)?\s*SPDX-License-Identifier:\s+(.*)$""", line)
            if match:
                license_id_lines.append(line)
                license = match.group(2)
            else:
                malformed_id_lines.append(line)
        for sig in generated_file_signatures:
            if sig in line:
                generated_file_lines.append(line)
    errors = []
    warnings = []
    if len(license_id_lines) > 1:
        msg = ("Found more than one (%d) SPDX-License-Identifier line"
               "" % (len(license_id_lines)))
        errors.append(msg)
    elif len(generated_file_lines) > 0:
        # No error for auto-generated files.
        generated_file = True
        pass
    elif all_lines_blank:
        # No error for files where all lines are blank
        pass
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
    return errors, warnings, all_lines_blank, generated_file, license


def walk_directory(path, config):
    spdx_errors = {}
    spdx_errors_filename_suffixes = collections.defaultdict(int)
    filenames_without_suffix = []
    spdx_warnings = {}
    auto_generated_file = {}
    spdx_good = {}
    spdx_ignored_suffix = {}
    exception_reading = {}
    ignore_directories = config.get('ignore_directories', [])
    ignore_paths = config.get('ignore_paths', [])
    skipped_directories = []
    for root, dirs, files in os.walk(path):
        dir_without_rootdir = root[len(path)+1:]
        skip_dir = False
        # A string in the list ignore_directories is one where if it
        # is any part of the directory part of a path name, the
        # directory is skipped.  For example if you put "third-party"
        # into the list of ignore_directories, then all of these paths
        # would be skipped:
        #
        #     ./other/target-syslibs/third-party
        #     ./other/target-utils/third-party
        #     ./other/open-p4studio/pkgsrc/bf-diags/third-party
        #     ./other/open-p4studio/pkgsrc/bf-utils/third-party
        #     ./other/open-p4studio/pkgsrc/bf-drivers/third-party
        for dir in ignore_directories:
            if root.endswith('/' + dir) or (('/' + dir + '/') in root):
                skip_dir = True
                break
        # A string in the list ignore_paths is one where it is only
        # skipped if it matches the _beginning_ of a relative path
        # name in the walk.  For example, if ignore_paths contains the
        # string ".github", then these directories would be skipped:
        #
        #     .github
        #     .github/workflows
        #
        # but this one would not be skipped:
        #
        #     workflows/.github
        if not skip_dir:
            for path in ignore_paths:
                if dir_without_rootdir.startswith(path):
                    skip_dir = True
                    break
        if skip_dir:
            if args.verbosity >= 3:
                print("Skipping directory: %s" % (root))
            skipped_directories.append(root)
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
            errors, warnings, all_lines_blank, generated_file, license = spdx_line_errors_warnings(lines, config)
            if errors:
                spdx_errors[fullname] = errors
                key = suffix
                if suffix is None:
                    key = "(none)"
                    filenames_without_suffix.append(fullname)
                spdx_errors_filename_suffixes[key] += 1
            if warnings:
                spdx_warnings[fullname] = warnings
            if generated_file:
                auto_generated_file[fullname] = True
            elif not (errors or warnings):
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

    print("%d files where exception occurred while reading its contents" % (len(exception_reading)))
    print("%d directories skipped" % (len(skipped_directories)))
    print("%d files where SPDX check was skipped because of file name suffix" % (len(spdx_ignored_suffix)))
    print("%d files with errors" % (len(spdx_errors)))
    for suffix in sorted(spdx_errors_filename_suffixes.keys()):
        print("    %d error files has file name suffix '.%s'"
              "" % (spdx_errors_filename_suffixes[suffix], suffix))
    for fname in filenames_without_suffix:
        print("    ERROR file without suffix: %s" % (fname))
    print("%d files with warnings" % (len(spdx_warnings)))
    print("%d files with signature lines indicating they were auto-generated."
          "" % (len(auto_generated_file)))
    print("%s files with neither errors nor warnings" % (len(spdx_good)))


rootdir = "."
if args.rootdir:
    rootdir = args.rootdir

walk_directory(rootdir, config)
