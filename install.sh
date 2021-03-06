#!/bin/bash

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $dir

virtualenv -p python3 ~/venvs/scrum-progress
source ~/venvs/scrum-progress/bin/activate
if [ -d /usr/pgsql-9.3/bin ]; then
  export PATH=$PATH:/usr/pgsql-9.3/bin
fi
pip install -r requirements.txt

#Create the logging directory as it is required by default
if [ ! -d $dir/logs ]; then
	mkdir $dir/logs
fi
