#!/bin/sh

set -e

if [ x${PEGASUS_LLNL_WORK_HOME} == x ]; then
    echo "Please set PEGASUS_LLNL_WORK_HOME to check out of pegasus-llnl repo"
    exit
fi
export PATH=${PEGASUS_LLNL_WORK_HOME}/bin:${PATH}
source /usr/workspace/wsb/alemm/pegasus/pegasus-user-env.sh 
