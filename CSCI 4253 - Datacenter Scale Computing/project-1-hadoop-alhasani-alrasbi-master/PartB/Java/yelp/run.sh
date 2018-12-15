#! /bin/bash

hadoop fs -mkdir yelp

hadoop jar ../target/wordcount.jar WordCount.final_version.drive s3://wordcount-datasets/ yelp/output

hadoop fs -cat yelp/output/final/part-r-00000 | more 
