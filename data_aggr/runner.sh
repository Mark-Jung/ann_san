#!/bin/sh
trainfile="train.csv"
testfile="test.csv"
if [ -f $trainfile ] ; then
    rm $trainfile
fi
if [ -f $testfile ] ; then
    rm $testfile 
fi
python main.py
