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

if [ "$1" == "-v" ]; then
    VERBOSE=1
else
    VERBOSE=0
fi

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

CURLARGS=""
if [ $VERBOSE -eq 1 ]; then
    CURLARGS="-v"
else
    CURLARGS="-s"
fi


cd tests
rm -Rf output.* #delete previous outputs

function test2folia() {
    echo "${boldblue}Testing $1...${normal}" >&2
    echo "----------------------------------------------" >&2
    local OK=1
    echo " (creating project)">&2
    if ! curl $CURLARGS -X PUT http://$HOSTNAME:8080/$1 > curlout; then
        cat curlout>&2
        echo "  ${boldred}ERROR: unable to create project${normal}">&2
        OK=0
    fi
    echo " (uploading input $2)">&2
    if ! curl $CURLARGS -F "inputtemplate=${1}_in" -F "file=@$2" http://$HOSTNAME:8080/$1/input/$2 > curlout; then
        cat curlout>&2
        echo "  ${boldred}ERROR: unable to upload input file${normal}">&2
        OK=0
    else
        echo " (running project)">&2
        if ! curl $CURLARGS -X POST http://$HOSTNAME:8080/$1/ > curlout; then
            cat curlout>&2
            echo "  ${boldred}ERROR: Unable to start project${normal}">&2
            OK=0
        else
            if grep 'errors="yes"' curlout > /dev/null; then
                echo "  ${boldred}ERROR: Failed to start project${normal}">&2
                OK=0
            else
                mkdir output.$1
                cd output.$1
                echo " (obtaining status)">&2
                while true; do
                    sleep 1
                    if curl $CURLARGS http://$HOSTNAME:8080/$1/ > stat; then
                        if grep 'code="2"' stat > /dev/null; then
                            sleep 3
                            break
                        fi
                    else
                        cat stat >&2
                        echo "  ${boldred}ERROR: Obtaining status failed${normal}">&2
                        OK=0
                        break
                    fi
                done
                echo " (downloading output $3)">&2
                if ! curl $CURLARGS http://$HOSTNAME:8080/$1/output/$3 > $3; then
                    echo "  ${boldred}ERROR: unable to get output${normal}">&2
                    OK=0
                else
                    cat $3
                    extension="${3#*.}"
                    if [[ $extension == "folia.xml" ]]; then
                        echo " (validating FoLiA output)">&2
                        if ! foliavalidator $3; then
                            echo "  ${boldred}ERROR: folia output failed to validate${normal}">&2
                            OK=0
                        fi
                    fi
                fi
                #delete the project so we don't pollute the server
                curl $CURLARGS http://$HOSTNAME:8080/$1/output/error.log > $1.log
                curl $CURLARGS -X DELETE http://$HOSTNAME:8080/$1 > curlout
                cd ..
            fi
        fi
    fi
    if [ $OK -eq 1 ]; then
        echo "${boldgreen}Done testing $1: SUCCESS!${normal}"
    else
        echo "${boldred}Done testing $1: FAILURE!${normal}"
        ALLGOOD=0
    fi
}


test2folia txt2folia test.txt test.folia.xml
test2folia txt2folia test2.txt test2.folia.xml
test2folia rst2folia test.rst test.folia.xml
test2folia md2folia test.md test.folia.xml
test2folia docx2folia test.docx test.folia.xml
test2folia odt2folia test.odt test.folia.xml
test2folia html2folia test.html test.folia.xml
test2folia mediawiki2folia test.wiki.txt test.wiki.folia.xml
test2folia latex2folia test.tex test.folia.xml
test2folia conllu2folia test.conllu test.folia.xml
test2folia naf2folia test.naf.xml test.folia.xml
test2folia pdf2folia test.pdf test.folia.xml
test2folia foliavalidator legacytest.folia.xml legacytest.log
test2folia foliaupgrade legacytest.folia.xml legacytest.folia.xml

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


