
struct dreptunghi{
 float b,h,d1,d2;
};

typedef struct dreptunghi  * PDREPTUNGHI;

struct element{
 char
  nume[11];        /* numele elementului       */
 int
  nrd,            /* numarul de dreptunghiuri */
  tip;            /* 0 sau 1                  */
 float
  h,              /* inaltimea spaletului     */
  arie,           /* aria elementului         */
  proc_arie,      /* aria elem / aria etaj    */
  gri,            /* grosimea inimii          */
  d1cgl,          /* d1-ul CG elem. in global  */
  d2cgl,          /* d2-ul CG elem. in global  */
  y1,             /* distantele la capetele elementului */
  y2,
  arin,           /* aria inimii              */
  icgd1,          /* momentul de inertie fata de cg, axa d1 */
  icgd2,          /* momentul de inertie fata de cg, axa d2 */
  w1cg,           /* modulele de rezistenta   */
  w2cg,
  r1,             /* dist. CG<-->limite sambure */
  r2,
  n,              /* forta N pe element       */
  nseism,
  sigma0,         /* tensiunea sigma in elem. */
  tau0fc,         /* rezistenta zidariei elementului*/
  tau0uc,
  mf1,            /* momentele de fisurare    */
  mf2,
  ac,             /* ariile zonelor comprimate sunt egale */
  xu1,xu2,        /* inaltimile zonelor comprimate        */
  c1,c2,          /* dist. de la CG zona comp. la fibrele extreme */
  qf1,qf2,        /* fortele taietoare asociate mom. de fisurare  */
  mu1,mu2,        /* momentele incov. ultime                      */
  qu1,qu2,        /* fortele taietoare asoc. mom. ultime          */
  qfic,           /* forta taietoare asoc. ruperii dupa sect. inc.*/
  qui,            /*                            in zona de cedare */
  ql,             /* forta oriz. capab. la alunec in rosturi.     */
  qcap1,           /* forta taietoare capab. in stadiul ultim      */
  qcap2,
  psi1,psi2,psim;

 PDREPTUNGHI vd;
};

typedef struct element  *    PELEMENT;


struct etaj{
 int nre;
 float
  d1cg,d2cg,arie,d1cr,d2cr,
  psimed1,psimed2;          /* coef psi mediu */
 PELEMENT ve;
};

typedef struct etaj  *       PETAJ;

struct cladire{
 int nre;         /* numarul de etaje         */
 int nrn;
 char
  mesaj1[81],mesaj2[81],titludesen[81];
 PETAJ ve;
 int
  mm,             /* marca mortarului         */
  mc;             /* marca caramizii          */
 float
  ks,beta,epsilon,forta;
 float
  G,Gseism;
 float
  rc,             /* Rc Rt                    */
  rt;
 float
  R1,R2,qc1,qc2;
};

typedef struct cladire *    PCLADIRE;

void far AlocareCladire(PCLADIRE);

PELEMENT get_element(PCLADIRE,int,int);
