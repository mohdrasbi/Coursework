#! /bin/bash

hadoop fs -mkdir gutenberg

hadoop jar ../target/wordcount.jar WordCount.final_version.drive s3://csci5253-gutenberg-dataset/ gutenberg/output

# hadoop fs -cat gutenberg/output/final/part-r-00000 | more 
