#! /usr/bin/env python3

# Copyright 2025 Andy Fingerhut
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import collections
import json
import os
import re
import subprocess
import sys

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
parser.add_argument('--addlicense-file', dest='addlicense_file', type=str)
parser.add_argument('--addlicense-author', dest='addlicense_author', type=str)
parser.add_argument('--verbosity', dest='verbosity', type=int, default=0)
args, remaining_args = parser.parse_known_args()

config = {}
if args.configfile:
    with open(args.configfile, 'r') as f:
        contents = f.read()
    config = json.loads(contents)
else:
    print("Must provide '--config-file <filename>' command line argument.")
    sys.exit(1)

config['ignored_suffixes'] = set(config.get('ignored_suffixes', []))
config['other_licenses'] = config.get('other_licenses', {})

if 'default_license' not in config:
    print("top level keys found in config file:")
    for k in sorted(config.keys()):
        print("    %s" % (k))
    print("config file must define a key 'default_license' with a string value.",
          file=sys.stderr)
    sys.exit(1)

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

def license_string(s):
    if s is None:
        return "(none)"
    return s

# Comment characters in various programming languages / configuration
# file formats:

# // - C, C++, Java, P4
# /* - C, C++, Java, P4
# # - Bash, Python
# " - Vim configuration file
# ;; - Emacs Elisp
# % - LaTeX source file

def spdx_line_errors_warnings(lines, expected_license, config, verbose=False):
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
        if args.verbosity >= 5:
            partial_match = 'SPDX-License-Identifier' in line
        if 'SPDX-License-Identifier' in line:
            match = re.search(r"""^\s*(#|\*|//|/\*|"|;;|%)?\s*SPDX-License-Identifier:\s+(.*)$""", line)
            if match:
                license = match.group(2)
                # In C/C++/Java files, there might be "*/" at the end
                # of the line.  If so, remove it from the license
                # found.
                match = re.search(r"""^(.*?)\s*\*\/\s*$""", license)
                if match:
                    license = match.group(1)
                license_id_lines.append(line)
            else:
                malformed_id_lines.append(line)
        if verbose:
            print("dbg line='%s'" % (line))
        for sig in generated_file_signatures:
            if verbose:
                print("dbg sig='%s' match=%s" % (sig, sig in line))
            if sig in line:
                generated_file_lines.append(line)
    errors = []
    warnings = []
    if all_lines_blank:
        # No error for files where all lines are blank
        pass
    elif len(generated_file_lines) > 0:
        # No error for auto-generated files.
        generated_file = True
        pass
    elif len(license_id_lines) > 1:
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
    return errors, warnings, all_lines_blank, generated_file, license


# Determine the author name and year that the file was first
# committed, via 'git log <filename>', and finding the last
# (i.e. oldest) commit, which should be the one that added the file.

def get_file_first_commit_info(fullname):
    cmd = ['git', 'log', fullname]
    got_exception = False
    try:
        completed = subprocess.run(cmd, capture_output=True,
                                   encoding='utf-8')
        prev_line_was_author = False
        num_commits = 0
        author = None
        year_str = None
        for line in completed.stdout.splitlines():
            if prev_line_was_author:
                match = re.search(r"""^Date:\s*(.*)\s*$""", line)
                if match:
                    prev_line_was_author = False
                    fulldate = match.group(1)
                    # Example date output from git log:
                    # Sun Jan 26 17:28:18 2025 -0500
                    match = re.search(r"""^\S+\s+\S+\s+\S+\s+\S+\s+(\d+)\s+\S+\s*$""", fulldate)
                    if match:
                        year_str = match.group(1)
            match = re.search(r"""^Author:\s*(.*)\s*$""", line)
            if match:
                author = match.group(1)
                num_commits += 1
                prev_line_was_author = True
                # Remove email address in angle brackets, if present
                match = re.search(r"""^(.*?)\s*<.*>\s*$""", author)
                if match:
                    author = match.group(1)
            else:
                prev_line_was_author = False
    except Exception as e:
        got_exception = True
        print("dbg e=%s" % (e))
    return got_exception, num_commits, author, year_str


def walk_directory(path, config):
    exit_status = 0
    spdx_errors = {}
    spdx_errors_filename_suffixes = collections.defaultdict(int)
    filenames_without_suffix = []
    spdx_warnings = {}
    auto_generated_file = {}
    symbolic_links = {}
    empty_file = {}
    spdx_unexpected_license = {}
    spdx_good = {}
    spdx_good_count_by_license = collections.defaultdict(int)
    spdx_ignored_suffix = {}
    exception_reading = {}
    ignore_directories = config.get('ignore_directories', [])
    ignore_paths = config.get('ignore_paths', [])
    ignore_files = config.get('ignore_files', {})
    all_directories = []
    skipped_directories = []
    for root, dirs, files in os.walk(path):
        all_directories.append(root)
        dir_without_rootdir = root[len(path)+1:]
        #print("dbg path='%s' (len %d) root='%s' dir_without_rootdir='%s'"
        #      "" % (path, len(path), root, dir_without_rootdir))
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
            for tmp_path in ignore_paths:
                if dir_without_rootdir.startswith(tmp_path):
                    skip_dir = True
                    break
        if skip_dir:
            if args.verbosity >= 4:
                print("Skipping directory: %s" % (root))
            skipped_directories.append(root)
            continue
        if args.verbosity >= 4:
            print("Checking directory: %s (without rootdir %s)" % (root, dir_without_rootdir))
        for file_name in files:
            fullname = os.path.join(root, file_name)
            if os.path.islink(fullname):
                # Ignore symbolic links.  If they point at no file at
                # all, then it would fail to read their contents.  If
                # they do point at a file in the directory tree, then
                # we will find them and read them by their
                # non-symbolic-link path name elsewhere in the file
                # scan.
                symbolic_links[fullname] = True
                continue
            fullname_without_rootdir = os.path.join(dir_without_rootdir,
                                                    file_name)
            if fullname_without_rootdir in ignore_files:
                continue
            suffix = suffix_after_dot(file_name)
            if suffix in config['ignored_suffixes']:
                spdx_ignored_suffix[fullname] = suffix
                continue
            try:
                with open(fullname, 'r') as f:
                    contents = f.read()
                lines = contents.splitlines()
            except Exception as e:
                exception_reading[fullname] = e
                continue
            if fullname_without_rootdir in config['other_licenses']:
                expected_license = config['other_licenses'][fullname_without_rootdir]['expected']
            else:
                expected_license = config['default_license']
            if args.verbosity >= 4:
                print("Checking file: %s" % (fullname))
            extra_debug = False
            #if fullname_without_rootdir == "go/p4/config/v1/p4info.pb.go":
            #    extra_debug = True
            errors, warnings, all_lines_blank, generated_file, license = spdx_line_errors_warnings(lines, expected_license, config, extra_debug)
            if errors:
                spdx_errors[fullname] = errors
                key = suffix
                if suffix is None:
                    key = "(none)"
                    filenames_without_suffix.append(fullname)
                spdx_errors_filename_suffixes[key] += 1
            if warnings:
                spdx_warnings[fullname] = warnings
            if all_lines_blank:
                empty_file[fullname] = True
            elif generated_file:
                auto_generated_file[fullname] = True
            elif not (errors or warnings):
                if license == expected_license:
                    spdx_good[fullname] = license
                    spdx_good_count_by_license[license_string(license)] += 1
                else:
                    spdx_unexpected_license[fullname] = {
                        'expected': expected_license,
                        'found': license
                    }

    for fullname in sorted(exception_reading.keys()):
        print("EXCEPTION: while reading file '%s': %s"
              "" % (fullname, exception_reading[fullname]))
        exit_status = 1
    if args.verbosity >= 3:
        for fullname in sorted(spdx_ignored_suffix.keys()):
            print("IGNORED SUFFIX: %s: %s" % (spdx_ignored_suffix[fullname],
                                              fullname))
    if args.verbosity >= 2:
        for fullname in sorted(spdx_errors.keys()):
            for msg in spdx_errors[fullname]:
                print("ERROR: %s: %s" % (fullname, msg))
        for fullname in sorted(spdx_warnings.keys()):
            for msg in spdx_warnings[fullname]:
                print("WARNING: %s: %s" % (fullname, msg))
        for fullname in sorted(spdx_unexpected_license.keys()):
            print("UNEXPECTED: %s: Expected license '%s' but found '%s'"
                  "" % (fullname,
                        spdx_unexpected_license[fullname]['expected'],
                        spdx_unexpected_license[fullname]['found']))
    if args.verbosity >= 3:
        for fullname in sorted(spdx_good.keys()):
            print("GOOD: %s: %s" % (spdx_good[fullname], fullname))

    if args.verbosity >= 1:
        print("%d files where exception occurred while reading its contents" % (len(exception_reading)))
        print("%d directories skipped out of %d directories total"
              "" % (len(skipped_directories), len(all_directories)))
        print("%d files where SPDX check was skipped because of file name suffix" % (len(spdx_ignored_suffix)))
    if args.verbosity >= 3:
        for fname in filenames_without_suffix:
            print("    NOTE file without suffix: %s" % (fname))
    if args.verbosity >= 1:
        print("%d files with signature lines indicating they were auto-generated."
              "" % (len(auto_generated_file)))
        print("%d symbolic links (contents ignored)."
              "" % (len(symbolic_links)))
        print("%d empty (all whitespace) files."
              "" % (len(empty_file)))
        print("%s files with neither errors nor warnings" % (len(spdx_good)))
        if args.verbosity >= 2:
            for license in sorted(spdx_good_count_by_license.keys()):
                print("    %d with license: %s"
                      "" % (spdx_good_count_by_license[license],
                            license))
        print("")
        print("%d files with warnings" % (len(spdx_warnings)))
        print("%s files with unexpected licenses" % (len(spdx_unexpected_license)))
        print("%d files with errors" % (len(spdx_errors)))
        for suffix in sorted(spdx_errors_filename_suffixes.keys()):
            print("    %d error files has file name suffix '.%s'"
                  "" % (spdx_errors_filename_suffixes[suffix], suffix))
    if args.addlicense_file:
        addlicense_script_lines = []
        for fullname in sorted(spdx_errors.keys()):
            got_exception, num_commits, author, year_str = get_file_first_commit_info(fullname)
            # If the user specified the --addlicense-author option,
            # use the author specified there instead of what was found
            # in the commit log.
            if args.addlicense_author:
                author = args.addlicense_author
            if got_exception:
                msg = ("# got exception trying to get git log of file: %s"
                       "" % (fullname))
                addlicense_script_lines.append(msg)
            else:
                msg = ("# %d commits found for file: %s"
                       "" % (num_commits, fullname))
                addlicense_script_lines.append(msg)
                if author is None or year_str is None:
                    msg = ("# author=%s year_str=%s at least one is None, so no addlicense command"
                           "" % (author, year_str))
                    addlicense_script_lines.append(msg)
                else:
                    msg = ("addlicense -c '%s' -l apache -s -y %s '%s'"
                           "" % (author, year_str, fullname))
                    addlicense_script_lines.append(msg)
        with open(args.addlicense_file, 'w') as f:
            print("#! /bin/bash", file=f)
            print("", file=f)
            for line in addlicense_script_lines:
                print(line, file=f)
    if len(spdx_unexpected_license) != 0 or len(spdx_errors) != 0:
        exit_status = 1
    return exit_status


rootdir = "."
if args.rootdir:
    rootdir = args.rootdir

exit_status = walk_directory(rootdir, config)
#if args.verbosity >= 1:
#    print("dbg exit_status=%d" % (exit_status))
sys.exit(exit_status)
