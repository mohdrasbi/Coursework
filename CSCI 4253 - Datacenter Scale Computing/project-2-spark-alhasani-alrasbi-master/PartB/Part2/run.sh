spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.0 part2.py

echo '=================================='
echo 'Run the following command to get the output for each bucket:'
echo 'Note: n in bucketn is the bucket number [1, 2, 3, 4, 5]'
echo 'hadoop fs -cat bucketn/output/part-00000'
echo '=================================='
