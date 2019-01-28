#include <stdio.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdlib.h>
#include <linux/kernel.h>

int main()
{
	int num1 = 123;
	int num2 = 7;
	int *result = malloc(sizeof(int));
	long res = syscall(334, num1, num2, result);
	printf("%d\n", *result);
	return res;
}	
