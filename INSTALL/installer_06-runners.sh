#! /bin/bash

dir_test="/home/ubuntu/workspace/.c9/runners2"
file_test="Python2Anaconda.run"
dir_path=$dir_test"/"$file_test
if [ -d "$dir_test" ]; then

    if [ -e $dir_path ];then
        echo "Found file "$dir_path
        echo "DO NOTHING...... "
    else
        echo "Did not find file "$dir_path
        cp -R ./$file_test $dir_path
    fi
    
    echo $dir_test
else
    echo "Dir not available "$dir_path
    mkdir $dir_test
    cp -R ./$file_test $dir_path
    echo "Copy file "$dir_path
fi

# isntall test unit
sudo pip install pytest