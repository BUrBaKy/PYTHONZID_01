#include<stdlib.h>
#include<conio.h>
#include<alloc.h>
#include "utile.h"

void error(char s[50])
{
 cprintf("\n\r\n\r %s . Program oprit, apasati o tasta.",s);
 getch();
 exit(1);
}


void printmem(char mesaj[50])
{
 unsigned long memorie;
 memorie=farcoreleft();
 cprintf("\n\r%s SPATIU HEAP= %lu octeti",mesaj,memorie);
}


void test_heap(void)
{
 if(heapcheck()==_HEAPCORRUPT)
  error("Heapul near este corupt !");
}


float min3(float a,float b,float c)
{
 return min2(a,min2(b,c));
}
