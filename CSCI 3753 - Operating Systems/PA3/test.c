#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>


int main()
{
	char t[20] = "123";
	strcat(t, "111");

	printf("%s\n", t);
}