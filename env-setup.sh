#!/bin/bash

#################
# Run unpriveleged for vagrant provisioning
# Don't rely on shared folders
#################

if [ -z "$1" ]; then
    echo usage: $0 provisioned file directory?
    echo "using ."
    TOP_LOC="."
else
    TOP_LOC="$1"
fi

wget "https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh" -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda

MINICONDA_PATH_EXPORT_CMD='export PATH=$HOME/miniconda/bin:$PATH'

if grep -q "$MINICONDA_PATH_EXPORT_CMD" "$HOME/.profile";
then
    echo "Miniconda already exported to path in .profile, I will not add it again"
else
    echo $MINICONDA_PATH_EXPORT_CMD >> $HOME/.profile
fi
source $HOME/.profile

ENV_YML="$TOP_LOC/environment.yml"
REQ_TXT="$TOP_LOC/requirements.txt"

if [ ! -f $ENV_YML -a -f $REQ_TXT ];then
 echo Cannot find environment.yml or requirements.txt
 exit 1
fi

echo Configuring conda
conda config --set always_yes yes --set changeps1 no
echo Installing conda-build and anaconda-client
conda install conda-build anaconda-client
echo Updating conda
conda update -q conda
echo conda info
conda info -a
echo Creating ease conda env
conda env create -f $ENV_YML
echo Activating ease-env
source activate ease-env
echo Installing extra requirements
pip install -r $REQ_TXT

