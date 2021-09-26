#include <stdlib.h>
#include <alloc.h>
#include "casa.h"
#include "utile.h"

extern int NRDE,NREE,NRE;

void far AlocareCladire(PCLADIRE p)
{
 int i,j;

 p=(cladire*)farcalloc(1,sizeof(struct cladire));
 if(p==NULL)
  error("Nu este memorie suf.");

 p->nre=NRE;
 test_heap();
                        /* etaje */
 (p->ve)=(etaj*)farcalloc(NRE,sizeof(struct etaj));
 if((p->ve)==NULL)
  error("Nu este memorie suf.");
 for(i=0;i<NRE;i++)
 {
  p->ve[i].nre=NREE;
  if(((p->ve[i]).ve=(PELEMENT) farcalloc(NREE,sizeof(struct element)))==NULL)
   error("Nu este memorie suficienta.");  /* elem etaj i */
  for(j=0;j<NREE;j++)
  {
   p->ve[i].ve[j].nrd=NRDE;
   if((p->ve[i].ve[j].vd=(PDREPTUNGHI) farcalloc(NRDE,sizeof(struct dreptunghi)))==NULL)
    error("Nu este memorie suficienta.");
  }
 }
}


PELEMENT get_element(PCLADIRE casa,int etaj,int nrelem)
{
 return ((casa->ve[etaj].ve)+nrelem);
}

