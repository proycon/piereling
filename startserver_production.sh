#!/bin/bash
if [ ! -z "$VIRTUAL_ENV" ]; then
    python setup.py install
else
    echo "No virtual environment detected, you have to take care of running setup.py install or setup.py develop yourself!">&2
fi
HOSTNAME=$(hostname)
echo "Detected hostname: $HOSTNAME">&2
if [ ! -f "piereling.$HOSTNAME.ini" ]; then
        echo "Expected uwsgi configuration piereling.$HOSTNAME.ini not found. Did you make one for the host you are running on?">&2
        exit 2
fi
uwsgi piereling.$HOSTNAME.ini || cat piereling.uwsgi.log
