#! /bin/bash

hadoop fs -mkdir ItemClick
hadoop fs -copyFromLocal input ItemClick

hadoop jar target/ItemClick.jar partc.item_click.drive ItemClick/input ItemClick/output

hadoop fs -cat ItemClick/output/final/part-r-00000 | more 
