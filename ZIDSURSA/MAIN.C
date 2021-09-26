#include<stdio.h>
#include<alloc.h>
#include<conio.h>
#include<stdlib.h>
#include<graphics.h>
#include<string.h>
#include "casa.h"
#include "inout.h"
#include "calcule.h"
#include "depanare.h"
#include "desenare.h"
#include "utile.h"
#include "svga16.h"
#include "gifsave.h"

#pragma warn -par

FILE *f, *ft;

int NRDE,NREE,NRE,invers,SVga,GIF;

void DeschidereFisierIntrare(char *);

void DimensionIn(void);

void InchidereFisierIntrare(void);

void zidarie(int,char *,char *);

void liniecomanda(int args,char *argv[])
{
 printf("\n Program 'zidarie',  (c) 1994 Stefan Epure");
 if(args<2)
 {
  printf("\n Sintaxa este :  zidarie 'fisier intrare' 'fisier iesire'.\n");
  exit(1);
 }
 if(args==4)
 {
  if(!strcmp(argv[3],"SVGA"))
   SVga=1;
  else
   SVga=0;
  if(!strcmp(argv[3],"GIF"))
   GIF=1;
  else
   GIF=0;
 }
 invers=0;
}

int main(int args,char* argv[])
{
 liniecomanda(args,argv);
 zidarie(args,argv[1],argv[2]);
 return 0;
}

extern int xmin,xmax,ymin,ymax,borderx,bordery;

int maxx,maxy;
        // limitele ecranului in modul grafic selectat
extern double ax,bx,ay,by;


int huge DetectVGA16()
{
/*
  int Vid;

  printf("\n\nSelectati modul video : \n");
  printf("  0) 320x200x16\n");
  printf("  1) 640x200x16\n");
  printf("  2) 640x350x16\n");
  printf("  3) 640x480x256\n");
  printf("  4) 800x600x16\n");
  printf("  5) 1024x768x16\n\n>");
  scanf("%d",&Vid);
  return Vid;
*/
  return 5;
}



void zidarie(int args, char nfi[60],char nfo[60])
{
 PCLADIRE casa;
 int i,j;
 int gd=DETECT,gm;
 char nfgif[60];

 clrscr();

 DeschidereFisierIntrare(nfi);

 DimensionIn();

 /*
                      Alocarile de memorie.
 */
#ifdef DEPANARE
 printmem("\n Memorie initiala.");
#endif
 if((casa=(cladire*)farcalloc(1,sizeof(struct cladire)))==NULL)
  error("Nu este memorie suficienta.");
 casa->nre=NRE;
                        /* etaje */
 if(((casa->ve)=(etaj*)farcalloc(NRE,sizeof(struct etaj)))==NULL)
  error("Nu este memorie suficienta.");
 for(i=0;i<NRE;i++)
 {
  casa->ve[i].nre=NREE;
  if(((casa->ve[i]).ve=(PELEMENT) farcalloc(NREE,sizeof(struct element)))==NULL)
   error("Nu este memorie suficienta.");  /* elem etaj i */
  for(j=0;j<NREE;j++)
  {
   casa->ve[i].ve[j].nrd=NRDE;
   if((casa->ve[i].ve[j].vd=(PDREPTUNGHI) farcalloc(NRDE,sizeof(struct dreptunghi)))==NULL)
    error("Nu este memorie suficienta.");
  }
 }

 test_heap();
#ifdef DEPANARE
 printmem("\n Memorie ramasa dupa alocare cladire.");
#endif

 printf("\n\n Citire date cladire.");
 DateIn(casa);
 printf("  Ok.\n");

 InchidereFisierIntrare();

 if(args!=2)
 {
  printf("\n Calcule.");
  calcule(casa);
  printf("  Ok.\n");
 }

 if(args!=2) SalvareDate(casa,nfo);

 if(SVga)
 {
 installuserdriver("Svga16",DetectVGA16);
 registerfarbgidriver(Svga16_fdriver);
 }
 else
 registerfarbgidriver(EGAVGA_driver_far);

 initgraph(&gd, &gm, "");

 setcolor(WHITE);
 setbkcolor(BLACK);
 maxx=maxy=getmaxy();

 limite(casa);

 for(i=0;i<casa->nre;i++)
 {
  cleardevice();
  settextjustify(LEFT_TEXT,BOTTOM_TEXT);
  desenareetaj(args,i,casa);
/*if(args!=2)
  {
     punct(casa->ve[i].d1cg,casa->ve[i].d2cg,"C.G.");
     punct(casa->ve[i].d1cg+casa->ve[i].d1cr,
        casa->ve[i].d2cg+casa->ve[i].d2cr,"C.R.");
  }*/
  axe();
/*  border();*/
  if(GIF)
  {
   strcpy(nfgif,nfi);
   strcat(nfgif,".gif");
   GIF_DumpEga10(nfgif);
  }
  getch();
 }
 closegraph();
 if(args!=2)
 {
  printf("\n OK. Rezultatele sunt in '%s'\n",nfo);
  if(GIF)
   printf("\n     Desenul este in '%s'\n",nfgif);
 }
}


void DeschidereFisierIntrare(char nf[60])
{
#ifndef DEPANARE
 if((f=fopen(nf,"r"))==NULL)
  error("Nu gasesc fisierul de intrare indicat.");
#endif
#ifdef DEPANARE
 if((f=fopen("test.inp","r"))==NULL)
  error("Nu gasesc fisierul test.inp  .");
#endif
}


void ElimCom(void)
{
 char ch;
 while((ch=fgetc(f))!=EOF)
 {
  if(ch==':')
   do;while(fgetc(f)!='\n');
  else
   fputc(ch,ft);
 }
}

void d2d1(FILE *f,FILE *fd)
{
 int bi,nret,nre,nrd,i,j,k;
 float bd,b,h,d1,d2;
 fscanf(f,"%d",&bi);
  fprintf(fd," %d",bi);
 fscanf(f,"%d",&bi);
  fprintf(fd," %d",bi);
 fscanf(f,"%d",&bi);
  fprintf(fd," %d",bi);
 fscanf(f,"%d",&bi);
  fprintf(fd," %d",bi);
 fscanf(f,"%d",&bi);
  fprintf(fd," %d",bi);
 fscanf(f,"%d",&nret);
  fprintf(fd," %d",nret);
 for(i=0;i<nret;i++)
 {
  fscanf(f,"%d",&nre);
   fprintf(fd," %d",nre);
  for(j=0;j<nre;j++)
  {
   fscanf(f,"%d",&bi);
    fprintf(fd," %d",bi);
   fscanf(f,"%f",&bd);
    fprintf(fd," %f",bd);
   fscanf(f,"%f",&bd);
    fprintf(fd," %f",bd);
   fscanf(f,"%d",&nrd);
    fprintf(fd," %d",nrd);
   for(k=0;k<nrd;k++)
   {
    fscanf(f,"%f",&b);
    fscanf(f,"%f",&h);
    fscanf(f,"%f",&d1);
    fscanf(f,"%f",&d2);
     fprintf(fd," %f",h);
     fprintf(fd," %f",b);
     fprintf(fd," %f",d2);
     fprintf(fd," %f",d1);
   }
                            /* Grosime inima elem. */
   fscanf(f,"%f",&bd);
    fprintf(fd," %f",bd);
  }
 }
}

void DimensionIn(void)
{
 ft=fopen("temp.1","wt");
 ElimCom();
 fclose(ft);fclose(f);
 f=fopen("temp.1","rt");
 if(invers) ft=fopen("temp.2","wt");
 if(invers)
 {
  d2d1(f,ft);
  fclose(ft);
 }
 fclose(f);
 if(invers)
  f=fopen("temp.2","rt");
 else
  f=fopen("temp.1","rt");
 fscanf(f,"%d",&NRE);fscanf(f,"%d",&NREE);fscanf(f,"%d",&NRDE);
 NRE++;NREE++;NRDE++;
}

void InchidereFisierIntrare(void)
{
 fclose(f);
 remove("temp.1");
 if(invers)
  remove("temp.2");
}
