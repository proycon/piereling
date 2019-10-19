#!/bin/bash

# Should run in a Python virtual environment ideally
bold=$(tput bold)
boldred=${bold}$(tput setaf 1) #  red
boldgreen=${bold}$(tput setaf 2) #  green
green=${normal}$(tput setaf 2) #  green
yellow=${normal}$(tput setaf 3) #  yellow
blue=${normal}$(tput setaf 4) #  blue
boldblue=${bold}$(tput setaf 4) #  blue
normal=$(tput sgr0)

TESTDIR=`dirname $0`
cd $TESTDIR
HOSTNAME=$(hostname)


echo "Checking installation..." >&2

ALLGOOD=1 #falsify

which clamservice 2>/dev/null
if [ $? -ne 0 ]; then
   echo "ERROR: clamservice not found" >&2
   exit 2
fi

#kill any existing webservices
kill $(ps aux | grep 'piereling' | awk '{print $2}') 2>/dev/null
sleep 2

echo "Starting piereling webservice" >&2
clamservice -d piereling.piereling 2> servicetest.server.log &
echo "waiting 10 seconds to be sure it started..." >&2
sleep 10

cd tests

function test2folia() {
    echo "${boldblue}Testing $1...${normal}" >&2
    echo "----------------------------------------------" >&2
    local OK=1
    if ! curl -v -X PUT http://$HOSTNAME:8080/$1; then
        echo "  ${boldred}ERROR: unable to create project${normal}">&2
        OK=0
    fi
    if ! curl -v -F "inputtemplate=${1}_in" -F "file=@$2" http://$HOSTNAME:8080/$1/input/$2; then
        echo "  ${boldred}ERROR: unable to upload input file${normal}">&2
        OK=0
    fi
    if ! curl -v -X POST http://$HOSTNAME:8080/$1/; then
        echo "  ${boldred}ERROR: unable to start project${normal}">&2
        OK=0
    else
        if [ -z "$4" ]; then
            sleep 5 #five seconds should hopefully be enough for processing (saves more complex polling)
        else
            sleep $4
        fi
        mkdir output
        cd output
        if ! curl -v http://$HOSTNAME:8080/$1/output/$3 > $3; then
            echo "  ${boldred}ERROR: unable to get output${normal}">&2
            OK=0
        else
            cat $3
            if ! foliavalidator $3; then
                echo "  ${boldred}ERROR: folia output failed to validate${normal}">&2
                OK=0
            fi
        fi
        cd ..
        rm -Rf output
        #delete the project so we don't pollute the server
        curl -v -X DELETE http://$HOSTNAME:8080/$1
        if [ $OK -eq 1 ]; then
            echo "${boldgreen}Done testing $1: SUCCESS!${normal}"
        else
            echo "${boldred}Done testing $1: FAILURE!${normal}"
            ALLGOOD=0
        fi
    fi
}


test2folia txt2folia test.txt test.folia.xml
test2folia txt2folia test2.txt test2.folia.xml
test2folia rst2folia test.rst test.folia.xml
test2folia md2folia test.md test.folia.xml 7
test2folia docx2folia test.docx test.folia.xml 7
test2folia odt2folia test.docx test.folia.xml 7
test2folia foliavalidator partial-legacy.1.5.folia.xml partial-legacy.1.5.folia.xml 10
test2folia foliaupgrade partial-legacy.1.5.folia.xml partial-legacy.1.5.folia.xml 10

echo "Stopping piereling service" >&2
kill $(ps aux | grep 'piereling' | awk '{print $2}') 2>/dev/null
sleep 2


if [ $ALLGOOD -eq 1 ]; then
    echo "${boldgreen}Done, all tests passed!${normal}" >&2
    exit 0
else
    echo "${boldred}TESTS FAILED!!!!${normal}" >&2
    exit 1
fi


