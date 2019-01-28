Name: Mohamed Al-Rasbi
Identity key: moal7202
Email: moal7202@colorado.edu

Files:
cs3753_add.c : contains system call funtion
Makefile : contains object files' names of system calls
syscall_64.tbl : system calls table, contains system calls and their numbers
syscalls.h : contains functions names of system calls
syslog: log file
test_add.c : test function for the system call I created

Where located in my VM:
/home/kernel/linux-hwe-4.13.0/arch/x86/kernel/csc3753_add.c
/home/kernel/linux-hwe-4.13.0/arch/x86/kernel/Makefile
/home/kernel/linux-hwe-4.13.0/arch/x86/entry/syscalls/syscall_64.tbl
/home/kernel/linux-hwe-4.13.0/include/linux/syscalls.h
/var/log/syslog

Instuctions for building:
I did the instructions in the writeup for compiling the kernel, and worked for me.
About the function in cs3753_add.c, I created a variable called temp to store the sum, logged that variable to kernel, and used copy_to_user function to copy the value of temp to *result. I did all that because if I do otherwise I get Killed error when I run the test program for the system call.


