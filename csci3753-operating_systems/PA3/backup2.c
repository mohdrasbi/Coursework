#include "multi-lookup.h"

void *requesters(void *arg)
{	
	struct reqthread *th = (struct reqthread *)arg;

	char line[1025];
	int serviced = 0;
	
	while(EOF != fscanf(th->datafile, "%[^\n]\n", line))
	{	
		if(serviced == 0)
		{
			th->filesServiced ++;
			serviced ++;
		}

		sem_wait(th->space);
		pthread_mutex_lock(th->mutex);

		th->sharedArray[*th->index] = strdup(line);

		int space_left, domains_left;
		sem_getvalue(th->domain, &domains_left);
		sem_getvalue(th->space, &space_left);
		//printf("Requester - id:%d, index:%d, space left:%d, domains left:%d, domain name:%s\n", th->id, *th->index, space_left, domains_left+1, line);

		*th->index = (*th->index + 1) % th->arrSize;

		pthread_mutex_unlock(th->mutex);
		sem_post(th->domain);

		
	}

	pthread_exit(NULL);
}

void *resolvers(void *arg)
{
	//printf("resolvers\n");
	struct resthread *th = (struct resthread *)arg;

	char *line;
	int completed;

	while(1)
	{
		sem_getvalue(th->domain, &completed);
		if(end_of_files(th->dataFiles, th->numFiles) && completed == 0)
		{
			break;
		}

		sem_wait(th->domain);
		pthread_mutex_lock(th->mutex);

		line = th->sharedArray[*th->index];
		th->sharedArray[*th->index] = strdup("");

		int space_left, domains_left;
		sem_getvalue(th->domain, &domains_left);
		sem_getvalue(th->space, &space_left);
		//printf("Resolver - id:%d, index:%d, space left:%d, domains left:%d, domain name:%s\n", th->id, *th->index, space_left, domains_left, line);

		// char tmp[1025] = "www.";
		// strcat(tmp, line);
		int ip = dnslookup(line, th->ipStr, 15);
		if(ip == -1)
		{
			printf("[%s]\n", line);
			fprintf(th->logfile, "%s,\n", line);
		}
		else
		{
			fprintf(th->logfile, "%s,%s\n", line, th->ipStr);
		}
		*th->index = (*th->index + 1) % th->arrSize;

		pthread_mutex_unlock(th->mutex);
		sem_post(th->space);
	}

	pthread_exit(NULL);
}

int end_of_files(FILE **files, int numFiles)
{
	for(int i = 0; i < numFiles; i++)
	{
		if(!feof(files[i]))
			return 0;
	}

	return 1;
}


int main(int argc, char **argv)
{
	int numReq = (int)*argv[1] - 48;
	int numRes = (int)*argv[2] - 48;
	char *reqLog = argv[3];
	char *resLog = argv[4];

	int numFiles = argc - 5;

	int size = 20;
	char *arr[size];
	int indexInArr = 0;
	int indexOutArr = 0;

	//open log files
	FILE *reqLogFile = fopen(reqLog, "w");
	FILE *resLogFile = fopen(resLog, "w");


	//error handling
	int bogusOut = 0;
	if(!reqLogFile)
	{
		printf("ERROR: Can't open serviced file.\n");
		bogusOut = 1;
	}

	if(!resLogFile)
	{
		printf("ERROR: Can't open results file.\n");
		bogusOut = 1;
	}

	if(bogusOut == 1)
		exit(EXIT_FAILURE);


	int count = 0;
	for(int i = 5; i < numFiles+5; i++)
	{
		if(fopen(argv[i], "r") == NULL)
		{
			printf("ERROR: Can't open %s file\n", argv[i]);
			count ++;
		}
	}


	//make array of open files
	numFiles = numFiles - count;
	FILE **dataFiles = malloc(sizeof(FILE*) * numFiles);
	for(int i = 0; i < numFiles; i++)
	{
		if(fopen(argv[i+5], "r") != NULL)
		{
			dataFiles[i] = fopen(argv[i+5], "r");
		}
	}


	//Initilize mutexes and semaphores
	pthread_mutex_t arr_mutex = PTHREAD_MUTEX_INITIALIZER;
	pthread_mutex_t arr_mutex2 = PTHREAD_MUTEX_INITIALIZER;
	pthread_mutex_t req_mutex = PTHREAD_MUTEX_INITIALIZER;
	sem_t domain;
	sem_t space;
	sem_init(&domain, 0, 0);
	sem_init(&space, 0, 20);

	//Requester threads
	pthread_t reqid[numReq];
	struct reqthread args[numReq];

	//Resolver threads
	pthread_t resid[numRes];
	struct resthread args2[numRes];

	//index of data files from argv
	int index = 0;

	//check that each file is assigned to one thread at least
	int check = 0;

	//initialize filesServiced in requesters and resolvers structs
	for(int i = 0; i < numReq; i++)
		args[i].filesServiced = 0;



	if(numReq < numFiles)
	{
		while(check == 0)
		{		
			for(int i = 0; i < numReq; i++)
			{
				//printf("check: %d, file: %s\n", check, argv[index + 5]);
				if(index == numFiles - 1)
				{
					check = 1;
				}

				args[i].datafile = dataFiles[index];
				args[i].filename = argv[index + 5];
				args[i].sharedArray = arr;
				args[i].index = &indexInArr;
				args[i].arrSize = size;
				args[i].id = i;
				args[i].logfile = reqLogFile;
				args[i].mutex = &arr_mutex;
				args[i].domain = &domain;
				args[i].space = &space;
				pthread_create(&reqid[i], NULL, requesters, &args[i]);

				if(index >= numReq-1)
				{
					printf("check:%d\n", check);
					for(int i = 0; i < numRes; i++)
					{
						args2[i].sharedArray = arr;
						args2[i].index = &indexOutArr;
						args2[i].arrSize = size;
						args2[i].logfile = resLogFile;
						args2[i].dataFiles = dataFiles;
						args2[i].numFiles = numReq;
						args2[i].mutex = &arr_mutex2;
						args2[i].domain = &domain;
						args2[i].space = &space;
						args2[i].id = i;
						pthread_create(&resid[i], NULL, resolvers, &args2[i]);
					}
					for(int i = 0; i < numReq; i++)
					{
						printf("join requestor:%d, file:%s\n", i, args[i].filename);
						pthread_join(reqid[i], NULL);
					}
					for(int i = 0; i < numRes; i++)
					{
						printf("join resolver:%d\n", i);
						pthread_join(resid[i], NULL);
					}

				}
				index ++;
			}
		}

	}
	else
	{		
		for(int i = 0; i < numReq; i++)
		{
			if(index > numFiles - 1)
				index = 0;
			printf("check: %d, file: %s\n", check, argv[index + 5]);

			args[i].datafile = dataFiles[index];
			args[i].filename = argv[index + 5];
			args[i].sharedArray = arr;
			args[i].index = &indexInArr;
			args[i].arrSize = size;
			args[i].id = i;
			args[i].logfile = reqLogFile;
			args[i].mutex = &arr_mutex;
			args[i].domain = &domain;
			args[i].space = &space;
			pthread_create(&reqid[i], NULL, requesters, &args[i]);

			index ++;
		}

		for(int i = 0; i < numRes; i++)
		{
			args2[i].sharedArray = arr;
			args2[i].index = &indexOutArr;
			args2[i].arrSize = size;
			args2[i].logfile = resLogFile;
			args2[i].dataFiles = dataFiles;
			args2[i].numFiles = numFiles;
			args2[i].mutex = &arr_mutex2;
			args2[i].domain = &domain;
			args2[i].space = &space;
			args2[i].id = i;
			pthread_create(&resid[i], NULL, resolvers, &args2[i]);
		}

		for(int i = 0; i < numReq; i++)
		{
			pthread_join(reqid[i], NULL);
		}

		for(int i = 0; i < numRes; i++)
		{
			pthread_join(resid[i], NULL);
		}
	}

	//write to requestors log file
	for(int i = 0; i < numReq; i++)
	{
		pthread_mutex_lock(&req_mutex);
		fprintf(reqLogFile, "Thread %d serviced %d files\n", i, args[i].filesServiced);
		pthread_mutex_unlock(&req_mutex);
	}

}