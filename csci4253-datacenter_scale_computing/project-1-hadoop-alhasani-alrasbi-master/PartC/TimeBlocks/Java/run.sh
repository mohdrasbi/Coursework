#! /bin/bash

hadoop fs -mkdir TimeBlocks
hadoop fs -copyFromLocal input TimeBlocks

hadoop jar target/TimeBlocks.jar partc.buys.drive TimeBlocks/input TimeBlocks/output

hadoop fs -cat TimeBlocks/output/final/part-r-00000 | more
