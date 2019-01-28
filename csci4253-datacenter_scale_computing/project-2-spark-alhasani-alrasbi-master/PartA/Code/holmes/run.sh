hadoop fs -mkdir holmes
hadoop fs -copyFromLocal input holmes/

spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.0 ../parta.py holmes/input holmes/output

hadoop fs -cat holmes/output/part-00000 | more
