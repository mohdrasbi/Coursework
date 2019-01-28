Name: Mohamed Al-Rasbi
ID: moal7202

How to run the file?
1. Open terminal
2. cd to AlRasbi_PA3 directory
3. run the command: make (which will compile the program)
4. to run the program: ./multi-lookup 4 3 serviced.txt results.txt names1.txt names2.txt names3.txt names4.txt names5.txt 
argv[1]: 4 is the number of requestor threads
argv[2]: 3 is the number of resolver threads
argv[3]: serviced.txt is the log file for requestor threads
argv[4]: results.txt is the log file for resolver threads
argv[5..n]: names1.txt..etc are the data files 