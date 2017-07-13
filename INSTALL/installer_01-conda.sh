
#! /bin/bash

#installer miniconda2 that work 

#Downloading Miniconda 64Bits for Linux https://conda.io/miniconda.html
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh

#Changing file permission for execution
chmod a+x Miniconda2-latest-Linux-x86_64.sh

#Installing Miniconda
./Miniconda2-latest-Linux-x86_64.sh

echo "------------------------------------------------------------------------------"
echo "ATTENTION"
echo "Please close the terminal and reopen and run installer_02-conda.sh script now"
echo "------------------------------------------------------------------------------"