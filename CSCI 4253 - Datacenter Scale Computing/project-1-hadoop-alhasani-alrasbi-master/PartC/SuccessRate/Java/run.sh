#! /bin/bash

hadoop fs -mkdir SuccessRate
hadoop fs -copyFromLocal input SuccessRate

hadoop jar first_job/target/SuccessRate-0.0.1-SNAPSHOT.jar partc.SuccessRate.drive SuccessRate/input/buys.txt SuccessRate/first_job_output_buys
hadoop jar first_job/target/SuccessRate-0.0.1-SNAPSHOT.jar partc.SuccessRate.drive SuccessRate/input/clicks.txt SuccessRate/first_job_output_clicks

hadoop jar second_job/target/SuccessRate2-0.0.1-SNAPSHOT.jar partc.SuccessRate2.drive SuccessRate/first_job_output_clicks/final/part-r-00000 SuccessRate/first_job_output_buys/final/part-r-00000 SuccessRate/final_output

hadoop fs -cat SuccessRate/final_output/final/part-r-00000 | more
