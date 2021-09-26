#include <graphics.h>
#include <stdlib.h>
#include <string.h>
#include "casa.h"
#include "utile.h"

int xmin=1.0e30,xmax=-1.0e30,ymin=1.0e30,ymax=-1.0e30,
    borderx=50,bordery=50;

extern int maxx,maxy;
        // limitele ecranului in modul grafic selectat
double ax,bx,ay,by;


int px(float x)
{
 return (ax*x+bx);
}

int py(float y)
{
 return (maxy-ay*y-by);
}


void punct(int x,int y,char nume[60])
{
 setcolor(WHITE);
 circle(px(x),py(y),2);
 settextstyle(SMALL_FONT,HORIZ_DIR,1);
 outtextxy(px(x)+5,py(y)-5,nume);
 setcolor(WHITE);
}


void border()
{
 setlinestyle(SOLID_LINE,0,THICK_WIDTH);
 line(0,0,0,maxy);
 line(maxx,0,maxx,maxy);
 line(0,0,maxx,0);
 line(0,maxy,maxx,maxy);
 setlinestyle(SOLID_LINE,0,NORM_WIDTH);
 punct(0,0,"");
 outtextxy(px(0)+5,py(0)+15,"Origine etaj.");
}


void limite(PCLADIRE pc)
{
 int etaj,nretaje,i,j,nre,nrd;
 float bmix,bmax,bmiy,bmay,d1,d2,b,h,lx,ly,l;

 nretaje=pc->nre;
 for(etaj=0;etaj<nretaje;etaj++)
 {
  nre=pc->ve[etaj].nre;
  for(i=0;i<nre;i++)
  {
   nrd=pc->ve[etaj].ve[i].nrd;// numarul de dreptunghiuri.
   for(j=0;j<nrd;j++)
   {
    d1=pc->ve[etaj].ve[i].vd[j].d1;
    d2=pc->ve[etaj].ve[i].vd[j].d2;
    b=pc->ve[etaj].ve[i].vd[j].b;
    h=pc->ve[etaj].ve[i].vd[j].h;
    bmix=d1-0.5*b;
    bmax=d1+0.5*b;
    bmiy=d2-0.5*h;
    bmay=d2+0.5*h;
    if(bmix<xmin)
     xmin=bmix;
    if(bmax>xmax)
     xmax=bmax;
    if(bmiy<ymin)
     ymin=bmiy;
    if(bmay>ymax)
     ymax=bmay;
   }
  }
 }
 lx=xmax-xmin;ly=ymax-ymin;
 if(lx>ly)
  l=lx;
 else
  l=ly;

 ax=(maxx-2.0*borderx)/l;
  bx=borderx-ax*xmin;
 ay=(maxy-2.0*bordery)/l;
  by=bordery-ay*ymin;
}


void desdrept(float x1,float y1,float x2,float y2)
{
 setlinestyle(SOLID_LINE,0,THICK_WIDTH);
 line(px(x1),py(y1),px(x2),py(y2));
 setlinestyle(SOLID_LINE,0,NORM_WIDTH);
}


void desenaredreptunghi(float x,float y,float b,float h)
{
 setfillstyle(INTERLEAVE_FILL,WHITE);
 bar(px(x-0.5*b),py(y+0.5*h),px(x+0.5*b),py(y-0.5*h));
}


void desenareetaj(int args,int etaj,PCLADIRE pc)
{
 int i,j,nre,nrd;
 float x,y,b,h;

 nre=pc->ve[etaj].nre;
 for(i=0;i<nre;i++)
 {
  nrd=pc->ve[etaj].ve[i].nrd;// numarul de dreptunghiuri.
  for(j=0;j<nrd;j++)
  {
   x=pc->ve[etaj].ve[i].vd[j].d1;
   y=pc->ve[etaj].ve[i].vd[j].d2;
   b=pc->ve[etaj].ve[i].vd[j].b;
   h=pc->ve[etaj].ve[i].vd[j].h;
   desenaredreptunghi(x,y,b,h);
  }
   if(args!=2)punct(pc->ve[etaj].ve[i].d1cgl,pc->ve[etaj].ve[i].d2cgl,
		    pc->ve[etaj].ve[i].nume);
 }
 settextjustify(CENTER_TEXT,CENTER_TEXT);
 outtextxy(maxx/2,maxy-30,pc->mesaj1);
 outtextxy(maxx/2,maxy-20,pc->mesaj2);
 settextjustify(RIGHT_TEXT,CENTER_TEXT);
 outtextxy(maxx-borderx/2,maxy-10,pc->titludesen);
 settextjustify(CENTER_TEXT,CENTER_TEXT);
}


void axe()
{
 setcolor(WHITE);
 settextjustify(LEFT_TEXT,CENTER_TEXT);
 moveto(px(0),py(0));
 linerel(30,0);
 outtext("d1");

 moveto(px(0),py(0));
 linerel(0,-30);
 outtext("d2");
 setcolor(WHITE);
}


