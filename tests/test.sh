#!/bin/bash

# Should run in a Python virtual environment ideally

TESTDIR=`dirname $0`
cd $TESTDIR
HOSTNAME=$(hostname)


echo "Checking installation..." >&2

GOOD=1

which clamservice 2>/dev/null
if [ $? -ne 0 ]; then
   echo "ERROR: clamservice not found" >&2
   exit 2
fi

echo "Starting piereling webservice" >&2
clamservice -d piereling.piereling 2> servicetest.server.log &
echo "waiting 10 seconds to be sure it started..." >&2
sleep 10

cd tests

echo "Testing txt2folia..." >&2
if ! curl -v -X PUT http://$HOSTNAME:8080/txt2folia; then
    echo "  ERROR: unable to create project">&2
    GOOD=0
fi
if ! curl -v -F "inputtemplate=txt2folia_in" -F "file=@test.txt" http://$HOSTNAME:8080/txt2folia/input/test.txt; then
    echo "  ERROR: unable to upload input file">&2
    GOOD=0
fi
if ! curl -v -X POST http://$HOSTNAME:8080/txt2folia/; then
    echo "  ERROR: unable to start project">&2
    GOOD=0
else
    sleep 5 #five seconds should hopefully be enough for processing (saves more complex polling)
    mkdir output
    if ! curl -v http://$HOSTNAME:8080/txt2folia/output/test.folia.xml; then
        echo "  ERROR: unable to get output">&2
        GOOD=0
    fi
    cd ..
    rm -Rf output
    #delete the project so we don't pollute the server
    curl -v -X DELETE http://$HOSTNAME:8080/txt2folia
fi



if [ $GOOD -eq 1 ]; then
    echo "Done, all tests passed!" >&2
    exit 0
else
    echo "TESTS FAILED!!!!" >&2
    exit 1
fi


