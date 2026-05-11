#! /bin/bash

INSTALLDIR="$HOME/forks/test-spdx-checker"
export PATH="${INSTALLDIR}:${PATH}"

REPO="ptf"
REPO="tutorials"
REPO="p4-guide"
REPO="p4-constraints"
REPO="p4runtime-shell"
REPO="PI"
REPO="behavioral-model"
REPO="tdi"
REPO="p4-dpdk-target"
REPO="pna"
REPO="p4c"
REPO="p4runtime"
REPO="p4mlir-incubator"
REPO="open-p4studio"
REPO="p4-spec"
ROOTDIR="$HOME/forks/${REPO}-1"

#ROOTDIR="$HOME/forks/${REPO}"
#ROOTDIR="$HOME/clones/${REPO}"
CONFIG_FILE="${INSTALLDIR}/config-files/spdx-checker-config-${REPO}.json"
ADDLICENSE_FILE="${INSTALLDIR}/addlicense-${REPO}.sh"
REUSE_FILE="${INSTALLDIR}/reuse-${REPO}.sh"

spdx-check.py --root-dir "${ROOTDIR}" --config-file "${CONFIG_FILE}" --addlicense-file "${ADDLICENSE_FILE}" --reuse-file "${REUSE_FILE}" --verbosity 2
