#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

#define DEVICE "/dev/simple_char_driver"


int main()
{
	char command;
	int file = open(DEVICE, O_RDWR);
	int size, offset, whence;
	char *data;
	while(1)
	{
		printf("r to read\nw to write\ns to seek\ne to exit\n");
		printf("Enter command: ");	
		//getchar();
		scanf("%c", &command);
		if(command == 'r')
		{
				//getchar();
				printf("Enter number of bytes: ");
				//size = getchar();
				scanf("%d", &size);
				char *buffer = malloc(size);
				read(file, buffer, size);
				printf("Data read from the device:\n %s\n", buffer);
		}
		else if(command == 'w')
		{
				getchar();
				printf("Enter data you want to write to the device: ");
				scanf("%[^\n]%*c", data);
				write(file, data, strlen(data));
		}
		else if(command == 's')
		{
				printf("Enter an offset value: ");
				//getchar();
				scanf("%d", &offset);
				printf("Enter a value for whence: ");
				//getchar();
				scanf("%d", &whence);
				lseek(file, offset, whence);

		}
		else if(command == 'e')
		{
			return 0;
		}
		getchar();
	}
}
