#! /bin/bash

hadoop fs -mkdir holmes
hadoop fs -copyFromLocal input holmes

hadoop jar ../target/wordcount.jar WordCount.final_version.drive holmes/input holmes/output

hadoop fs -cat holmes/output/final/part-r-00000 | more 
