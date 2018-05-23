#ifndef MULTILOOKUP_H
#define MULTILOOKUP_H

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <semaphore.h>
#include "multi-lookup.h"
#include "PA3/util.h"
#include "PA3/util.c"


struct reqthread
{
	FILE *datafile;
	FILE *logfile;
	char *filename;
	char **sharedArray;
	int *index;
	int arrSize;
	int id;
	int filesServiced;
	pthread_mutex_t *mutex;
	sem_t *domain;
	sem_t *space;
};

struct resthread
{
	char **sharedArray;
	int *index;
	int arrSize;
	FILE *logfile;
	char ipStr[30];
	FILE **dataFiles;
	int numFiles;
	int id;
	pthread_mutex_t *mutex;
	sem_t *domain;
	sem_t *space;
};

void *requesters(void *arg);
void *resolvers(void *arg);
int end_of_files(FILE **files, int numFiles);




#endif
