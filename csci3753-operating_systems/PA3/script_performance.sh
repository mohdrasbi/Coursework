#!/bin/bash

make clean
make 

./multi-lookup 1 1 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt
./multi-lookup 1 3 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt
./multi-lookup 3 1 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt
./multi-lookup 3 3 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt
./multi-lookup 5 5 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt
./multi-lookup 8 5 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt >> performance.txt

./performance.py multi-lookup 