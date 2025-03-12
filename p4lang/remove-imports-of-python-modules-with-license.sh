#! /bin/bash

# This script is intended to be run in a way similar to this, on an
# input file that contains Python lines of source code containing the
# word 'import'.  The intent is to remove lines that only import
# modules that are distributed with a license that is given as a
# command line option, using the SPDX License Identifier string to
# specify the license.

# (First assign SPDX the name of the test-spdx-checker root directory.)
# find . ! -type d -print0 | xargs -0 egrep '\bimport\b' | $SPDX/p4lang/remove-imports-of-python-modules-with-license.sh Apache-2.0

# A more complete example:
# find . ! -type d -print0 | xargs -0 egrep '\bimport\b' | $SPDX/p4lang/remove-imports-of-python-standard-modules.sh | $SPDX/p4lang/remove-imports-of-python-modules-with-license.sh Apache-2.0 | $SPDX/p4lang/remove-imports-of-python-modules-with-license.sh BSD-3-Clause | $SPDX/p4lang/remove-imports-of-python-modules-with-license.sh MIT

# Here is a list of the strings it checks for, each on a line by
# themselves, sorted, for easier human reading:

if [ $# -ne 1 ]
then
    1>&2 echo "usage: $0 <license-id>"
    1>&2 echo ""
fi

LICENSE_ID="$1"

# TODO: Which license are these released under:
#
# IPython
# nose2
# ntf - Apache-2.0?
# pcap - imported by ptf/src/ptf/dataplane.py
# pexpect
# pygraphviz
# pytest
# socketio
# tabulate
# tkinter
# traitlets
# yaml

case ${LICENSE_ID} in
    Apache-2.0)
	# grpc
	# p4
	# p4.config
	# p4.config.v1
	# p4.tmp
	# p4.v1
	# ptf
	# ptf.base_tests
	# ptf.mask
	# ptf.packet
	# ptf.pcap_writer
	# ptf.testutils
	# ptf.thriftutils
	# pyroute2
	#
	# pattern:
	# grpc|p4|p4.config|p4.config.v1|p4.tmp|p4.v1|ptf|ptf.base_tests|ptf.mask|ptf.packet|ptf.pcap_writer|ptf.testutils|ptf.thriftutils|pyroute2
	egrep -v 'import (grpc|p4|p4.config|p4.config.v1|p4.tmp|p4.v1|ptf|ptf.base_tests|ptf.mask|ptf.packet|ptf.pcap_writer|ptf.testutils|ptf.thriftutils|pyroute2)( as .*)?\s*$' | egrep -v 'from (grpc|p4|p4.config|p4.config.v1|p4.tmp|p4.v1|ptf|ptf.base_tests|ptf.mask|ptf.packet|ptf.pcap_writer|ptf.testutils|ptf.thriftutils|pyroute2) import '
	;;
    BSD-3-Clause)
	# jsl
	# matplotlib - "Matplotlib only uses BSD compatible code"
	# mininet
	# mininet.\S+
	# netaddr
	# networkx
	# numpy
	# pandas
	# ply - TODO: verify it is BSD-3-Clause
	# ply.lex - TODO: verify it is BSD-3-Clause
	# ply.yacc - TODO: verify it is BSD-3-Clause
	# psutil
	# pcap (from a module named pypcap in here: https://github.com/pynetwork/pypcap but the module name is just 'pcap')
	# seaborn
	#
	# pattern:
	# jsl|matplotlib|mininet|mininet.\S+|netaddr|networkx|numpy|pandas|ply|ply.lex|ply.yacc|psutil|pcap|seaborn
	egrep -v 'import (jsl|matplotlib|mininet|mininet.\S+|netaddr|networkx|numpy|pandas|ply|ply.lex|ply.yacc|psutil|pcap|seaborn)( as .*)?\s*$' | egrep -v 'from (jsl|matplotlib|mininet|mininet.\S+|netaddr|networkx|numpy|pandas|ply|ply.lex|ply.yacc|psutil|pcap|seaborn) import '
	;;
    GPL-2.0-only)
	# scapy
	# scapy.\S+
	egrep -v 'import (scapy|scapy.\S+)( as .*)?\s*$' | egrep -v 'from (scapy|scapy.\S+) import '
	;;
    MIT)
	# jsonschema
	# nnpy
	egrep -v 'import (jsonschema|nnpy)( as .*)?\s*$' | egrep -v 'from (jsonschema|nnpy) import '
	;;
    *)
	1>&2 echo "Unsupported license id: ${LICENSE_ID}"
	exit 1
	;;
esac

