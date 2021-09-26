#include <stdio.h>
#include <string.h>
#include "casa.h"
#include "utile.h"

extern FILE* f;
extern int NRDE,NREE,NRE;
int rezultate_complete;

void test(int j,int i,int ref)
{
 if((i>=ref)&&(j==0))
  error("Depasire nr. max. etaje !");
 if((i>=ref)&&(j==1))
  error("Depasire nr. max. elemente/etaj !");
 if((i>=ref)&&(j==2))
  error("Depasire nr. max. drept./element !");
}

void DateIn(PCLADIRE pc)
{
 int bi,i,j,k,rot;
 float bd,sc,deltaO,d1,d2,b,h,gri1,gri2;
 fscanf(f,"%f",&bd);
 sc=bd;
 fscanf(f,"%d",&bi);
 rot=bi;
 fscanf(f,"%f",&bd);
 deltaO=bd;
 fscanf(f,"%f",&bd);
 pc->forta=bd;
 fscanf(f,"%f",&bd);
 pc->Gseism=bd;
 fscanf(f,"%d",&bi);
 rezultate_complete=bi;
 fscanf(f,"%f",&bd);
 pc->ks=bd;
 fscanf(f,"%f",&bd);
 pc->beta=bd;
 fscanf(f,"%f",&bd);
 pc->epsilon=bd;
 fscanf(f,"%d",&bi);
 pc->mm=bi;   /*     Marca mortarului */
 fscanf(f,"%d",&bi);
 pc->mc=bi;   /* si a caramizilor. */
 do; while(fgetc(f)!='=');
 fgets(pc->mesaj1,80,f);
 fgets(pc->mesaj2,80,f);
 fgets(pc->titludesen,80,f);
 pc->mesaj1[strlen(pc->mesaj1)-1]='\0';
 pc->mesaj2[strlen(pc->mesaj2)-1]='\0';
 pc->titludesen[strlen(pc->titludesen)-1]='\0';
 pc->nre=bi=1;
 test(0,bi,NRE);
 for(i=0;i<pc->nre;i++)
 {
  fscanf(f,"%d",&bi);pc->ve[i].nre=bi;   /* nr elemente pe etaj i */
  test(1,bi,NREE);
  for(j=0;j<pc->ve[i].nre;j++)
  {
   fscanf(f,"%s",&(pc->ve[i].ve[j].nume));
   fscanf(f,"%d",&bi);pc->ve[i].ve[j].tip=bi;  /* tipul spaletului */
   fscanf(f,"%f",&bd);pc->ve[i].ve[j].h=bd;     /* inaltimea H */

                            /* Forta pe elem. */
   fscanf(f,"%f",&bd);pc->ve[i].ve[j].n=bd;
                            /* Forta pe elem. pentru seism */
   fscanf(f,"%f",&bd);pc->ve[i].ve[j].nseism=bd;
                            /* Numar dreptunghiuri. */
   fscanf(f,"%d",&bi);
       pc->ve[i].ve[j].nrd=bi;

   test(2,bi,NRDE);  /* nr dreptunghiuri pe elem */
   for(k=0;k<pc->ve[i].ve[j].nrd;k++)
   {
    fscanf(f,"%f",&bd);b=bd*sc;
    fscanf(f,"%f",&bd);h=bd*sc;
    fscanf(f,"%f",&bd);d1=bd*sc;
    fscanf(f,"%f",&bd);d2=bd*sc;
    if(rot==-1)
    {
     pc->ve[i].ve[j].vd[k].d1=d2+0.5*h;
     pc->ve[i].ve[j].vd[k].d2=-d1+deltaO-0.5*b;
     pc->ve[i].ve[j].vd[k].b=h;
     pc->ve[i].ve[j].vd[k].h=b;
    }
    if(rot==0)
    {
     pc->ve[i].ve[j].vd[k].d1=d1+0.5*b;
     pc->ve[i].ve[j].vd[k].d2=d2+0.5*h;
     pc->ve[i].ve[j].vd[k].b=b;
     pc->ve[i].ve[j].vd[k].h=h;
    }
    if(rot==1)
    {
     pc->ve[i].ve[j].vd[k].d1=-d2+deltaO-0.5*h;
     pc->ve[i].ve[j].vd[k].d2=d1+0.5*b;
     pc->ve[i].ve[j].vd[k].b=h;
     pc->ve[i].ve[j].vd[k].h=b;
    }
   }
                            /* Grosime inima elem. */
    fscanf(f,"%f",&gri1);fscanf(f,"%f",&gri2);
    if(rot)
     pc->ve[i].ve[j].gri=gri2*sc;
    else
     pc->ve[i].ve[j].gri=gri1*sc;
  }
 }
}

#pragma warn -par

void convert(int i,int j,char* s)
{
 if(i==1)
  switch(j)
  {
   case 0:strcpy(s,"C200");break;
   case 1:strcpy(s,"C150");break;
   case 2:strcpy(s,"C125");break;
   case 3:strcpy(s,"C100");break;
   case 4:strcpy(s,"C75");break;
   case 5:strcpy(s,"C50");
  }
 else
  switch(j){
   case 0:strcpy(s,"M50");break;
   case 1:strcpy(s,"M25");break;
   case 2:strcpy(s,"M10");break;
   case 3:strcpy(s,"M4");
  }
}

void Antet(FILE *f)
{
 fprintf(f,"\n  Program  :   'ZIDARIE'.\n\n"
             "  Autori   :   prof. dr. ing. Radu Agent\n"
             "               ing. Nicolae Mihaila\n"
             "               ing. Stefan Epure\n");
}


void SalvareDate(PCLADIRE pc,char nfo[60])
{
 int i,j,k;
 FILE* fo;
 char mcs[6],mms[6];

 if((fo=fopen(nfo,"wt"))==NULL)
  error("Disc R/O sau plin.");

 Antet(fo);
 fprintf(fo,"\n  Denumire : %s\n",pc->mesaj1);
   fprintf(fo,"             %s\n",pc->mesaj2);

 fprintf(fo,"\n  Unitatile de masura sunt:\n");
     fprintf(fo,"\n  Lungimi  :  <cm>"
                "\n  Arii     :  <cm2>"
                "\n  Forte    :  <tone>"
                "\n  Eforturi :  <daN/cm2>"
                "\n  Momente  :  <t*m>");

 fprintf(fo,"\n\n\n\t\t  D A T E L E  D E  I N T R A R E: \n\n");
 fprintf(fo,"\n\n Materiale : ");
 convert(1,pc->mc,mcs);
 fprintf(fo,  "\n\n  Marca de caramida folosita este %s.",mcs);
 convert(2,pc->mm,mms);
 fprintf(fo,  "\n  Marca de mortar folosit este %s.\n",mms);
 fprintf(fo,"\n\n Coeficientii seismici : ks=%5.1f  beta=%5.1f  epsilon=%5.1f",
         pc->ks,pc->beta,pc->epsilon);
 fprintf(fo,"\n\n\n Geometria:        < Fata de sistemul de referinta al nivelului. >");
 fprintf(fo,"\n");

 for(i=0;i<pc->nre;i++)
 {
  for(j=0;j<pc->ve[i].nre;j++)
  {
   fprintf(fo,"\n\n\n      Elementul %s are %d dreptunghiuri. "
              ,pc->ve[i].ve[j].nume,pc->ve[i].ve[j].nrd);
   fprintf(fo,"\n\n             b          h          d1         d2\n");
   for(k=0;k<pc->ve[i].ve[j].nrd;k++)
    fprintf(fo,"\n  %2d  %#10.0f %#10.0f %#10.0f %#10.0f", k+1,pc->ve[i].ve[j].vd[k].b,pc->ve[i].ve[j].vd[k].h,
          pc->ve[i].ve[j].vd[k].d1,pc->ve[i].ve[j].vd[k].d2);

   fprintf(fo,"\n\n   Grosime inima                 : %7.2f",pc->ve[i].ve[j].gri);
   fprintf(fo,"\n   Forta in element              : %7.3f",pc->ve[i].ve[j].n);
   fprintf(fo,"\n   Forta in element pentru seism : %7.3f", pc->ve[i].ve[j].nseism);
  }
 }
 if(rezultate_complete)
  fprintf(fo,"\n\n\n\n\n\n\t\t    R  E  Z  U  L  T  A  T  E  L  E");
 else
  fprintf(fo,"\n\n\n\n\n\t    R  E  Z  U  L  T  A  T  E  L  E");
 for(i=0;i<pc->nre;i++)
 {    
  if(rezultate_complete)
  {
   fprintf(fo,"\n\n     Centrul de greutate     :        d1 =%6.2f          d2 =%6.2f",
         pc->ve[i].d1cg,pc->ve[i].d2cg);
   fprintf(fo,"\n\n     Centrul de rigiditate   : d1cr-d1cm =%6.2f   d2cr-d2cm =%6.2f",
         pc->ve[i].d1cr,pc->ve[i].d2cr);
  }
  else
  fprintf(fo,"\n\n     Incarcarea pe nivel     :         N = %8.3f",pc->G);
    fprintf(fo,"\n     Incarcarea pentru seism :    Nseism = %8.3f",pc->Gseism);
    fprintf(fo,"\n          Aria zidurilor     :         A = %8.0f \n",pc->ve[i].arie);


  for(j=0;j<pc->ve[i].nre;j++)
  {
   fprintf(fo,"\n\n\n                 Elementul   %s",
              pc->ve[i].ve[j].nume);
   if(rezultate_complete)
   {
    fprintf(fo,"\n\n    Arie       y1        y2        Arin        Icgd1     Icgd2  "
              "     W1cg         W2cg \n");
    fprintf(fo, "\n%6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.4e  %6.4e  ",
            pc->ve[i].ve[j].arie,pc->ve[i].ve[j].y1,pc->ve[i].ve[j].y2,
            pc->ve[i].ve[j].arin,pc->ve[i].ve[j].icgd1,pc->ve[i].ve[j].icgd2,pc->ve[i].ve[j].w1cg,
            pc->ve[i].ve[j].w2cg);
    fprintf(fo,"\n\n   Sigma0     tau0fc    tau0uc      Mf1         Mf2       Ac1,2        xu1        xu2        \n");
    fprintf(fo, "\n%6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.4e  %6.4e  %6.4e  ",
            pc->ve[i].ve[j].sigma0,pc->ve[i].ve[j].tau0fc,pc->ve[i].ve[j].tau0uc,
            pc->ve[i].ve[j].mf1,pc->ve[i].ve[j].mf2,pc->ve[i].ve[j].ac,
            pc->ve[i].ve[j].xu1,pc->ve[i].ve[j].xu2);
    fprintf(fo,"\n\n    c1         c2        Qf1        Qf2         Mu1       Mu2          Qu1         Qu2        \n");
    fprintf(fo, "\n%6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.4e  %6.4e  "
                "%6.4e  ",
            pc->ve[i].ve[j].c1,pc->ve[i].ve[j].c2,pc->ve[i].ve[j].qf1,
            pc->ve[i].ve[j].qf2,pc->ve[i].ve[j].mu1,pc->ve[i].ve[j].mu2,
            pc->ve[i].ve[j].qu1,pc->ve[i].ve[j].qu2);
    fprintf(fo,"\n\n  Qficap      Qui        Ql        Qcap1      Qcap2      psi1       psi2        %Arie \n");
    fprintf(fo, "\n%6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.3e  %6.4e  %6.4e",
            pc->ve[i].ve[j].qfic,pc->ve[i].ve[j].qui,pc->ve[i].ve[j].ql,
            pc->ve[i].ve[j].qcap1,pc->ve[i].ve[j].qcap2,pc->ve[i].ve[j].psi1,
            pc->ve[i].ve[j].psi2,pc->ve[i].ve[j].proc_arie);
    }
    else
   {
        fprintf(fo,"\n\n   Arie     Arie inima");
        fprintf(fo, "\n%7.0f    %7.0f",pc->ve[i].ve[j].arie,pc->ve[i].ve[j].arin);
        fprintf(fo,"\n\n   Sigma0    tau0fc     tau0uc");
        fprintf(fo,"\n%7.2f    %7.2f    %7.2f",
          pc->ve[i].ve[j].sigma0,pc->ve[i].ve[j].tau0fc,pc->ve[i].ve[j].tau0uc);
        fprintf(fo,"\n\n    Qf1       Qf2       Qficap");
        fprintf(fo,"\n%8.3f   %8.3f   %8.3f",pc->ve[i].ve[j].qf1,pc->ve[i].ve[j].qf2,
                                        pc->ve[i].ve[j].qfic);
        fprintf(fo,"\n\n    Qu1       Qu2         Qui        Ql");
        fprintf(fo, "\n%8.3f   %8.3f   %8.3f  %8.3f",
                pc->ve[i].ve[j].qu1,pc->ve[i].ve[j].qu2,
                pc->ve[i].ve[j].qui,pc->ve[i].ve[j].ql);
        fprintf(fo,"\n\n   Qcap1      Qcap2");
        fprintf(fo,"\n%8.3f   %8.3f",pc->ve[i].ve[j].qcap1,pc->ve[i].ve[j].qcap2);
        fprintf(fo,"\n\n   Psi1       Psi2");
        fprintf(fo,"\n %6.2f     %6.2f",pc->ve[i].ve[j].psi1,pc->ve[i].ve[j].psi2);
    }
  }
  fprintf(fo,"\n\n\n\n\n\t      C O N C L U Z I I   C A L C U L\n");

  fprintf(fo,"\n\n        Qcap.1= %8.3f          Qcap.2= %8.3f",
             pc->qc1,pc->qc2);

  fprintf(fo,"  \n   Psi mediu 1= %8.2f     Psi mediu 2= %8.2f",
             pc->ve[i].psimed1,pc->ve[i].psimed2);
  fprintf(fo,"\n\n    Gradul de acoperire al structurii:\n"
                 "\n                R1= %7.2f"
                 "\n                R2= %7.2f",
             pc->R1,pc->R2);

 }
 fprintf(fo,"\n\n\n Sfarsit.\n\n");
 fclose(fo);
}













