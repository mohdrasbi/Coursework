spark-submit wordcount.py s3n://output-tweets/ output AKIAJE2HJ767MV2AWT7A CFfQKZ1DchRovVj80fkHVctXQTeWEKFDkPPIDRJE
hadoop fs -cat output/part-* | more
