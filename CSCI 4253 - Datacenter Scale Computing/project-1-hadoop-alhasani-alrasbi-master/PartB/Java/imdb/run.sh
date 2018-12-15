#! /bin/bash

hadoop fs -mkdir imdb
hadoop fs -copyFromLocal input imdb

hadoop jar ../target/wordcount.jar WordCount.final_version.drive imdb/input imdb/output

hadoop fs -cat imdb/output/final/part-r-00000 | more 
