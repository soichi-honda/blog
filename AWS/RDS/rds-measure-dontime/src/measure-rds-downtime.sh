#! /bin/bash

## Input sleeptime you want.
sleepTime=1

endpoint=$1
executionUser=$2
password=$3

dbStatus=""

mysqladmin ping -h ${endpoint} -u ${executionUser} -p${password} 2>&1 | grep alive > /dev/null 2>&1
if [ $? = 0 ]; then
    echo "DB status is alive"
    date
    echo "---------"
    dbStatus="alive"
    sleep ${sleepTime}
elif [ $? != 0 ]; then
    echo "DB status is dead"
    date
    echo "---------"
    dbStatus="dead"
    sleep ${sleepTime}
fi

while true; do
    mysqladmin ping -h ${endpoint} -u ${executionUser} -p${password} 2>&1 | grep alive > /dev/null 2>&1
    if [ $? = 0 ]; then
        if [ ${dbStatus} = "alive" ]; then
            sleep ${sleepTime}
        elif [ ${dbStatus} = "dead" ]; then
            echo "DB status has been alive"
            date
            echo "---------"
            dbStatus="alive"
            sleep ${sleepTime}
        fi
    elif [ $? != 0 ]; then
        if [ ${dbStatus} = "alive" ]; then
            echo "DB status has been dead"
            date
            echo "---------"
            dbStatus="dead"
            sleep ${sleepTime}
        elif [ ${dbStatus} = "dead" ]; then
            sleep ${sleepTime}
        fi
    fi
done
