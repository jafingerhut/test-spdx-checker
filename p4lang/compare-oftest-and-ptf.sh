#! /bin/bash

if [ ! -d oftest ]
then
    git clone https://github.com/floodlight/oftest
    cd oftest
    git checkout 23ab62fc31df6cb35e57ce37e4e9331048547fa2
    cd ..
fi
OFTEST=$PWD/oftest

if [ ! -d ptf ]
then
    git clone https://github.com/p4lang/ptf
    cd ptf
    git checkout 41a3934a5a16a432a56ed272016bc366c09bca5d
    cd ..
fi
PTF=$PWD/ptf

DIFF="diff -c"
${DIFF} -r $OFTEST/platforms $PTF/platforms
${DIFF} $OFTEST/oft $PTF/ptf

for f in \
    dataplane.py \
    base_tests.py \
    netutils.py \
    testutils.py \
    __init__.py \
    pcap_writer.py \
    afpacket.py \
    packet.py \
    parse.py
do
    ${DIFF} $OFTEST/src/python/oftest/$f $PTF/src/ptf/$f
done

${DIFF} $OFTEST/src/python/oftest/ofutils.py $PTF/src/ptf/ptfutils.py

# No corresponding file in $OFTEST for $PTF/src/ptf/thriftutils.py
