#include <math.h>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include "casa.h"
#include "depanare.h"
#include "utile.h"

extern int NRE,NRDE,NREE;


void lat(PELEMENT el,int i,float* bi,float* hi,float* d2i,float *d2cgli,
                      float *d1i, float *d1cgli)
{
  *bi=el->vd[i].b;      /* b */
  *hi=el->vd[i].h;      /* h */
  *d2i=el->vd[i].d2;    /* d2 */
  *d2cgli=el->d2cgl;    /* d2 CG el. in local */
  *d1i=el->vd[i].d1;    /* d2 */
  *d1cgli=el->d1cgl;    /* d2 CG el. in local */
}

void pas3(PELEMENT el)
{
 int i,nrd;
 float
 sd1,sd2,ariei[30],disti,d2cg[40],d1cg[40],max,min,
 bi,hi,d2i,d2cgli,d1i,d1cgli;


 nrd=el->nrd;
 el->arie=sd1=sd2=0.0;
 for(i=0;i<nrd;i++)
 {
  lat(el,i,&bi,&hi,&d2i,&d2cgli,&d1i,&d1cgli);
  ariei[i]=bi*hi;  /*    b*h     */
  sd1+=ariei[i]*(el->vd[i].d2);          /* momentele statice */
  sd2+=ariei[i]*(el->vd[i].d1);
  (el->arie)+=ariei[i];
 }
 (el->d1cgl)=sd2/(el->arie);
 (el->d2cgl)=sd1/(el->arie);
 (el->icgd1)=(el->icgd2)=0.0;
 for(i=0;i<nrd;i++)
 {
  lat(el,i,&bi,&hi,&d2i,&d2cgli,&d1i,&d1cgli);
  d2cg[i]=d2i-d2cgli;
  d1cg[i]=d1i-d1cgli;
  (el->icgd1)+=bi*pow(hi,3.0)/12.0+ariei[i]*d2cg[i]*d2cg[i];
  (el->icgd2)+=hi*pow(bi,3.0)/12.0+ariei[i]*d1cg[i]*d1cg[i];
 }
 max=-1.0e35;min=1.0e35;
 for(i=0;i<nrd;i++)
 {
  lat(el,i,&bi,&hi,&d2i,&d2cgli,&d1i,&d1cgli);
  disti=d2cg[i]-hi/2;
  if(disti<min)
   min=disti;
  disti=d2cg[i]+hi/2;
  if(disti>max)
   max=disti;
 }
 (el->y2)=-min;    /*         distantele y1, y2 */
 (el->y1)=max;
 (el->arin)=(-min+max)*(el->gri);  /* aria inimii */
 (el->w1cg)=fabs((el->icgd1)/(el->y1));
 (el->w2cg)=fabs((el->icgd1)/(el->y2));
 (el->r1)=(el->w2cg)/(el->arie);
 (el->r2)=(el->w1cg)/(el->arie);
}

void pas5(PELEMENT el)
{
 (el->sigma0)=(el->n)*1.0e3/(el->arie); /* 1t*1000/cm2-> kg/cm2 */
}


void pas71(PCLADIRE casa)
{
 float
  tabel2[4][6]={{44.0,36.0,34.0,30.0,26.0,20.0},
              {36.0,30.0,28.0,26.0,22.0,18.0},
              {32.0,26.0,24.0,20.0,18.0,14.0},
              {28.0,24.0,22.0,18.0,14.0,12.0}},

     tabel3[4]={2.7,1.8,0.9,0.45};

 (casa->rc)=tabel2[casa->mm][casa->mc];  /*       Rc in daN/cm2           */
 (casa->rt)=tabel3[casa->mm];            /*       Rt in daN/cm2           */
}


void pas72(PCLADIRE casa,PELEMENT el)
{
 float /*          daN/cm2                                                */
       tabel40[13]={0.5,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0},

   tabel41[4][13]={{1.9,2.1,2.3,2.6,2.8,3.0,3.2,3.4,3.5,3.7,3.9,4.0,4.2},
                   {1.3,1.5,1.7,1.9,2.1,2.3,2.5,2.6,2.8,2.9,3.0,3.2,3.3},
                   {0.7,0.8,1.0,1.2,1.3,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2},
                   {0.4,0.5,0.7,0.8,0.9,1.0,1.1,1.2,1.2,1.3,1.4,1.5,1.5}},

tabel42[6][4][13]={
                   {      /*       c200     */
                    {0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7},
                    {0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2},
                    {0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6},
                    {0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9}},
                   {      /*       c150     */
                    {0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7},
                    {0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2},
                    {0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6},
                    {0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9}},
                   {      /*       c125     */
                    {0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7},
                    {0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2},
                    {0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6},
                    {0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9}},
                   {      /*       c100     */
                    {0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7},
                    {0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2},
                    {0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6},
                    {0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9}},
                   {     /*        c75      */
                    {0.1,0.3,0.6,1.0,1.3,1.6,2.0,2.3,2.6,3.0,3.3,3.6,4.0},
                    {0.1,0.3,0.6,0.9,1.2,1.5,1.7,2.0,2.3,2.6,2.9,3.2,3.5},
                    {0.1,0.2,0.4,0.7,0.9,1.1,1.3,1.6,1.8,2.1,2.3,2.5,2.7},
                    {0.1,0.2,0.3,0.5,0.7,0.9,1.0,1.2,1.4,1.6,1.8,2.0,2.1}},
                   {    /*         c50      */
                    {0.2,0.4,0.7,1.1,1.5,1.9,2.3,2.7,3.1,3.5,3.9,4.3,4.6},
                    {0.2,0.3,0.7,1.0,1.3,1.6,2.0,2.3,2.6,3.0,3.3,3.6,4.0},
                    {0.1,0.2,0.5,0.8,1.0,1.3,1.5,1.8,2.1,2.3,2.6,3.8,3.1},
                    {0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4}}},

   sig0;
   int
    linie,i,col,mc,it;

   sig0=el->sigma0;
   linie=(casa->mm);
   mc=(casa->mc);
   col=-1;
   for(i=0;i<12;i++)
    if((sig0>=tabel40[i])&&(sig0<tabel40[i+1]))
     col=i;
   if(col==-1)
   {
    it=0;
    if(sig0<=tabel40[0])
     col=0;
    else
     col=12;
   }
   else
    it=1;

    /* Interpolare liniara in tabel pentru calculul Tau0fcap.in daN/cm2 */

   if(it)
   {
    (el->tau0fc)=tabel41[linie][col]+(sig0-tabel40[col])*
               (tabel41[linie][col+1]-tabel41[linie][col])/
               (tabel40[col+1]-tabel40[col]);

    /* Interpolare liniara in tabel pentru calculul Tau0ucap.in daN/cm2 */
    (el->tau0uc)=tabel42[mc][linie][col]+(sig0-tabel40[col])*
                (tabel42[mc][linie][col+1]-tabel42[mc][linie][col])/
                (tabel40[col+1]-tabel40[col]);
   }
   else
   {
    (el->tau0fc)=tabel41[linie][col];
    (el->tau0uc)=tabel42[mc][linie][col];
   }

}


void pas8(PELEMENT el)
{
 (el->mf1)=(el->n)*(el->r1)/100.;   /* T*m */
 (el->mf2)=(el->n)*(el->r2)/100.;
}

void pas9(PELEMENT el,PCLADIRE casa)
{
 (el->ac)=(el->sigma0)/(casa->rc)*(el->arie);
}


void pas1011(PELEMENT el)
{
 float
  x1,x2,x,pas,bi,hi,d2i,
  da,ar,arie_impusa,ms;
 int i,nrd;

 pas=0.01;   /*  1 mm   */
 nrd=el->nrd;
 arie_impusa=el->ac;   /* coordonatele sunt masurate fata de CG elem */
 x=el->y1;            /* extremitate de sus */
 ar=0.0;
 ms=0.0;
 do              /* pentru capatul de sus 'coord d2 maxima' */
 {
  x-=pas;
  for(i=0;i<nrd;i++)
  {
   d2i=el->vd[i].d2;
   hi=el->vd[i].h;
   x1=d2i+hi/2-(el->d2cgl);
   x2=d2i-hi/2-(el->d2cgl);
   if((x<x1)&&(x>x2))
   {
    bi=(el->vd[i].b);
    da=pas*bi;
    ar+=da;
    ms+=da*x;
   }
  }
 }
 while(ar<arie_impusa);
 (el->xu1)=(el->y1)-(x+0.5*pas);
 (el->c1)=(el->y1)-ms/ar;

 x=0.0;
 ar=0.0;
 ms=0.0;

 x=-el->y2;
 ar=0.0;
 ms=0.0;
 do              /* pentru capatul de jos 'coord d2 minima' */
 {
  x+=pas;
  for(i=0;i<nrd;i++)
  {
   d2i=el->vd[i].d2;
   hi=el->vd[i].h;
   x1=d2i+hi/2-(el->d2cgl);
   x2=d2i-hi/2-(el->d2cgl);
   if((x<x1)&&(x>x2))
   {
    bi=(el->vd[i].b);
    da=pas*bi;
    ar+=da;
    ms+=da*x;
   }
  }
 }
 while(ar<arie_impusa);
 (el->xu2)=(el->y2)-fabs(x-0.5*pas);
 (el->c2)=(el->y2)-fabs(ms/ar);
}



void pas12(PELEMENT el)
{
 if((el->tip)==0)
 {
  (el->qf1)=1.5*(el->mf1)/(el->h)*100.0;      /* t */
  (el->qf2)=1.5*(el->mf2)/(el->h)*100.0;
 }
 else
 {
  (el->qf1)=2.0*(el->mf1)/(el->h)*100.0;
  (el->qf2)=2.0*(el->mf2)/(el->h)*100.0;
 }
}

void pas13(PELEMENT el)
{
 (el->mu1)=(el->n)*((el->y1)-(el->c1))/100.0; /* tm */
 (el->mu2)=(el->n)*((el->y2)-(el->c2))/100.0;
}

void pas14(PELEMENT el)
{
 if((el->tip)==0)
 {
  (el->qu1)=1.5*(el->mu1)/(el->h)*100.0;      /* t */
  (el->qu2)=1.5*(el->mu2)/(el->h)*100.0;
 }
 else
 {
  (el->qu1)=2.0*(el->mu1)/(el->h)*100.0;
  (el->qu2)=2.0*(el->mu2)/(el->h)*100.0;
 }
}

void pas15(PELEMENT el)
{
 (el->qfic)=(el->tau0fc)*(el->arin)/1000.0;    /* t */
}

void pas16(PELEMENT el)
{
 (el->qui)=(el->tau0uc)*(el->arin)/1000.0;    /* t */
}

void pas17(PELEMENT el)
{
 (el->ql)=0.7*(el->n);    /* t */
}

void pas18(PELEMENT el)
{
 float qc;

     /* directia 1 */

 if((el->qu1)>(el->qfic))
  (el->qcap1)=min3((el->qu1),(el->qfic),(el->ql));
 else
  (el->qcap1)=min3((el->qu1),(el->qui),(el->ql));

    /* directia 2 */

 if((el->qu2)>(el->qfic))
  (el->qcap2)=min3((el->qu2),(el->qfic),(el->ql));
 else
  (el->qcap2)=min3((el->qu2),(el->qui),(el->ql));
}

void pas1926(PELEMENT el)
{
			  /*    psi 1 */
 if((el->qfic)>=(el->qu1))
  (el->psi1)=0.3;
 else
 {
  if((el->qfic)<=(el->qf1))
   (el->psi1)=0.8;
  else
  {
   if((((el->qfic)-(el->qf1))/((el->qu1)-(el->qf1)))<=0.2)
    (el->psi1)=0.8;
   else
    (el->psi1)=0.8-0.5*((el->qfic)-(el->qf1))/((el->qu1)-(el->qf1));
  }
 }
                          /*    psi 2 */
 if((el->qfic)>=(el->qu2))
  (el->psi2)=0.3;
 else
 {
  if((el->qfic)<=(el->qf2))
   (el->psi2)=0.8;
  else
  {
   if((((el->qfic)-(el->qf2))/((el->qu2)-(el->qf2)))<=0.2)
    (el->psi2)=0.8;
   else
    (el->psi2)=0.8-0.5*((el->qfic)-(el->qf2))/((el->qu2)-(el->qf2));
  }
 }
}

void pas27(PCLADIRE casa,int i)
{
 int j,nre;
 float pq,q;

 pq=q=0.0;
 nre=(casa->ve[i].nre);
 for(j=0;j<nre;j++)   /* iterare peste elementele etajului i */
 {
  pq+=(casa->ve[i].ve[j].psi1)*(casa->ve[i].ve[j].qcap1);
  q+=(casa->ve[i].ve[j].qcap1);
 }
 casa->ve[i].psimed1=(float)pq/q;

 pq=q=0.0;
 for(j=0;j<nre;j++)   /* iterare peste elementele etajului i */
 {
  pq+=(casa->ve[i].ve[j].psi2)*(casa->ve[i].ve[j].qcap2);
  q+=(casa->ve[i].ve[j].qcap2);
 }
 (casa->ve[i].psimed2)=pq/q;
}

void pas28(PCLADIRE casa)
{
 float qc1=0.,qc2=0.,g=0.0,gseism=0.0;
 int etaj,j,nrel;

 etaj=0; // !!!

  nrel=casa->ve[etaj].nre;
  for(j=0;j<nrel;j++)
  {
   qc1+=(casa->ve[etaj].ve[j].qcap1);
   qc2+=(casa->ve[etaj].ve[j].qcap2);
   if(casa->Gseism==0.0)
    gseism+=(casa->ve[etaj].ve[j].nseism);
   g+=(casa->ve[etaj].ve[j].n);
  }
  casa->G=g;

  if(casa->Gseism==0)
   casa->Gseism=gseism;

  casa->qc1=qc1;casa->qc2=qc2;

  casa->R1=qc1/((casa->ks)*(casa->beta)*(casa->ve[etaj].psimed1)*(casa->epsilon)*
                (casa->Gseism));
  casa->R2=qc2/((casa->ks)*(casa->beta)*(casa->ve[etaj].psimed2)*(casa->epsilon)*
                (casa->Gseism));

}


void calcule(PCLADIRE casa)
{
 int i,j;
 float msd1j,msd2j,ariej,d2icmd1j,d1icmd2j,icmd1j,icmd2j;

 pas71(casa);
 for(i=0;i<casa->nre;i++) /* iterare peste toate etajele */
  {
               /*  Etapa 3 din schema aplicata pe tot etajul i */

  msd1j=msd2j=ariej=0.0;
  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 3 element %3d.     ",j+1);
   pas3(get_element(casa,i,j));
   msd1j+=(casa->ve[i].ve[j].arie)*(casa->ve[i].ve[j].d2cgl);
   msd2j+=(casa->ve[i].ve[j].arie)*(casa->ve[i].ve[j].d1cgl);
   ariej+=(casa->ve[i].ve[j].arie);
  }
  casa->ve[i].d1cg=msd2j/ariej; /*      coord. CG etaj         */
  casa->ve[i].d2cg=msd1j/ariej;
  casa->ve[i].arie=ariej;
  if(casa->forta)
   for(j=0;j<casa->ve[i].nre;j++)
   {
    casa->ve[i].ve[j].proc_arie=(casa->ve[i].ve[j].arie)/ariej;
    casa->ve[i].ve[j].n=casa->forta*casa->ve[i].ve[j].proc_arie;
   }
  icmd1j=icmd2j=d2icmd1j=d1icmd2j=0.0;
  for(j=0;j<casa->ve[i].nre;j++)
  {
   d2icmd1j+=(casa->ve[i].ve[j].icgd1)*
                 (casa->ve[i].ve[j].d2cgl-casa->ve[i].d2cg);
   icmd1j+=casa->ve[i].ve[j].icgd1+(casa->ve[i].ve[j].arie)*
            pow((casa->ve[i].ve[j].d2cgl-casa->ve[i].d2cg),2);
   d1icmd2j+=(casa->ve[i].ve[j].icgd2)*
                 (casa->ve[i].ve[j].d1cgl-casa->ve[i].d1cg);
   icmd2j+=casa->ve[i].ve[j].icgd2+(casa->ve[i].ve[j].arie)*
            pow((casa->ve[i].ve[j].d1cgl-casa->ve[i].d1cg),2);
  }
  casa->ve[i].d1cr=d1icmd2j/icmd2j; /*      coord. CR fata de CM      */
  casa->ve[i].d2cr=d2icmd1j/icmd1j;


              /*  Etapa 4 din schema aplicata pe tot etajul i. */
              /*  Forta N pe element este data de intrare.     */

              /*  Etapa 5 din schema aplicata pe tot etajul i */
  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 5 element %3d.           ",j+1);
   pas5(get_element(casa,i,j));
   if(casa->ve[i].ve[j].sigma0>(0.99*casa->rc))
    {
     printf("\n\n Eroare :\n");
     printf("\n Sigma0[elementul %d]=%8.3f > Rc[elementul %d]=%8.3f\n\n\n",j+1,casa->ve[i].ve[j].sigma0,
                                             j+1,0.99*casa->rc);
     exit(1);
    }
  }
              /*   Etapa 6 din schema aplicata pe tot etajul i. */
              /*   Marca mortarului, respectiv caramizii este   */
              /*  data de intrare.                              */

              /*   Etapa 7.1 este comuna pentru toata casa.*/
              /*   S-a executat la inceput.                */


              /*   Etapa 7.2 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 7-2 element %3d.       ",j+1);
   pas72(casa,get_element(casa,i,j));
  }
              /*   Etapa 8 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 8 element %3d.       ",j+1);
   pas8(get_element(casa,i,j));
  }
              /*   Etapa 9 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 9 element %3d.        ",j+1);
   pas9(get_element(casa,i,j),casa);
  }
              /*   Etapele 10 si 11 din schema, aplicate pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 10-11 element %3d.        ",j+1);
   pas1011(get_element(casa,i,j));
  }

              /*   Etapa 12 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 12 element %3d.           ",j+1);
   pas12(get_element(casa,i,j));
  }

              /*   Etapa 13 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 13 element %3d.            ",j+1);
   pas13(get_element(casa,i,j));
  }

              /*   Etapa 14 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 14 element %3d.             ",j+1);
   pas14(get_element(casa,i,j));
  }

              /*   Etapa 15 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 15 element %3d.               ",j+1);
   pas15(get_element(casa,i,j));
  }


              /*   Etapa 16 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 16 element %3d.              ",j+1);
   pas16(get_element(casa,i,j));
  }

              /*   Etapa 17 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 17 element %3d.          ",j+1);
   pas17(get_element(casa,i,j));
  }

              /*   Etapa 18 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 18 element %3d.          ",j+1);
   pas18(get_element(casa,i,j));
  }


              /*   Etapele 19-26 din schema aplicata pe tot etajul i.*/

  for(j=0;j<casa->ve[i].nre;j++)
  {
   gotoxy(1,6);
   printf("\n Pas 19-26 element %3d.        ",j+1);
   pas1926(get_element(casa,i,j));
  }

              /*   Etapa 27 din schema aplicata pe tot etajul i.*/
   gotoxy(1,6);
   printf("\n Pas 27.                    ");
   pas27(casa,i);
 }
   gotoxy(1,6);
   printf("\n Pas 28.                     ");
   pas28(casa);
}










