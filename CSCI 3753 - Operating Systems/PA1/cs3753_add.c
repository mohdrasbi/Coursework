#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/uaccess.h>

asmlinkage long sys_cs3753_add(int num1, int num2, int *result)
{
int temp = num1 + num2;
copy_to_user(result, &temp, sizeof temp);
printk(KERN_ALERT "%d + %d = %d", num1, num2, temp);
return 0;
}
