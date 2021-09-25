from typing import List
from typing import Tuple

class Dreptunghi() :
    b  : float
    h  : float
    d1 : float
    d2 : float
    def __init__(self, _b:float, _h:float, _d1:float, _d2:float):
        self.b  = _b
        self.h  = _h
        self.d1 = _d1
        self.d2 = _d2

class Element():
    """description of class"""
    nume            : str 
    nrd             : int     #numarul de dreptunghiuri
    tip             : int     # tip 0 sau 1
    h               : float   # inaltimea
    arie            : float   # aria elementului         */
    proc_arie       : float   # aria elem / aria etaj    */
    gri             : float   # grosimea inimii          */
    d1cgl           : float   # d1-ul CG elem. in global  */
    d2cgl           : float   # d2-ul CG elem. in global  */
    y1              : float   # distantele la capetele elementului */
    y2              : float   #
    arin            : float   # aria inimii              */
    icgd1           : float   # momentul de inertie fata de cg, axa d1 */
    icgd2           : float   # momentul de inertie fata de cg, axa d2 */
    w1cg            : float   # modulele de rezistenta   */
    w2cg            : float   #
    r1              : float   # dist. CG<-->limite sambure */
    r2              : float   #
    N               : float   # forta N pe element       */
    Nseism          : float   #
    sigma0          : float   # tensiunea sigma in elem. */
    tau0fc          : float   # rezistenta zidariei elementului*/
    tau0uc          : float   #
    mf1             : float   # momentele de fisurare    */
    mf2             : float   #
    ac              : float   # ariile zonelor comprimate sunt egale */
    xu1             : float
    xu2             : float   # inaltimile zonelor comprimate        */
    c1              : float
    c2              : float   # dist. de la CG zona comp. la fibrele extreme */
    qf1             : float
    qf2             : float   # fortele taietoare asociate mom. de fisurare  */
    mu1             : float
    mu2             : float   # momentele incov. ultime                      */
    qu1             : float
    qu2             : float   # fortele taietoare asoc. mom. ultime          */
    qfic            : float   # forta taietoare asoc. ruperii dupa sect. inc.*/
    qui             : float   #                            in zona de cedare */
    ql              : float   # forta oriz. capab. la alunec in rosturi.     */
    qcap1           : float   # * forta taietoare capab. in stadiul ultim      */
    qcap2           : float   #
    psi1            : float
    psi2            : float
    psim            : float
    vecD            : List[Dreptunghi]    #vector dreptunghi

    def __init__(self):   
        self.nume = 'Numele elementului'     
        self.nrd = self.tip = 0
        self.h               = 0.0    # inaltimea
        self.arie            = 0.0    # aria elementului         */
        self.proc_arie       = 0.0    # aria elem / aria etaj    */
        self.gri             = 0.0    # grosimea inimii          */
        self.d1cgl           = 0.0    # d1-ul CG elem. in global  */
        self.d2cgl           = 0.0    # d2-ul CG elem. in global  */
        self.y1              = 0.0    # distantele la capetele elementului */
        self.y2              = 0.0    #
        self.arin            = 0.0    # aria inimii              */
        self.icgd1           = 0.0    # momentul de inertie fata de cg, axa d1 */
        self.icgd2           = 0.0    # momentul de inertie fata de cg, axa d2 */
        self.w1cg            = 0.0    # modulele de rezistenta   */
        self.w2cg            = 0.0    #
        self.r1              = 0.0    # dist. CG<-->limite sambure */
        self.r2              = 0.0    #
        self.N               = 0.0    # forta N pe element       */
        self.Nseism          = 0.0    #
        self.sigma0          = 0.0    # tensiunea sigma in elem. */
        self.tau0fc          = 0.0    # rezistenta zidariei elementului*/
        self.tau0uc          = 0.0    #
        self.mf1             = 0.0    # momentele de fisurare    */
        self.mf2             = 0.0    #
        self.ac              = 0.0    # ariile zonelor comprimate sunt egale */
        self.xu1             = 0.0 
        self.xu2             = 0.0    # inaltimile zonelor comprimate        */
        self.c1              = 0.0 
        self.c2              = 0.0    # dist. de la CG zona comp. la fibrele extreme */
        self.qf1             = 0.0 
        self.qf2             = 0.0    # fortele taietoare asociate mom. de fisurare  */
        self.mu1             = 0.0 
        self.mu2             = 0.0    # momentele incov. ultime                      */
        self.qu1             = 0.0 
        self.qu2             = 0.0    # fortele taietoare asoc. mom. ultime          */
        self.qfic            = 0.0    # forta taietoare asoc. ruperii dupa sect. inc.*/
        self.qui             = 0.0    #                            in zona de cedare */
        self.ql              = 0.0    # forta oriz. capab. la alunec in rosturi.     */
        self.qcap1           = 0.0    # * forta taietoare capab. in stadiul ultim      */
        self.qcap2           = 0.0    #
        self.psi1            = 0.0 
        self.psi2            = 0.0 
        self.psim            = 0.0 
        self.vecD            = []
        

class Etaj():
    nre : int
    d1cg    : float
    d2cg    : float
    arie    : float
    d1cr    : float
    d2cr    : float
    psimed1 : float
    psimed2 : float
    vElem   : List[Element]
    def __init__(self) -> None:
        self.nre = 0
        self.d1cg    = 0.0
        self.d2cg    = 0.0
        self.arie    = 0.0
        self.d1cr    = 0.0
        self.d2cr    = 0.0
        self.psimed1 = 0.0    # coef psi mediu
        self.psimed2 = 0.0    
        self.vElem   = []    #vector element


#class DateInitiale():
#    #Dim             : Tuple [float, float, float]
#    #Scara           : int
#    #Rotire          : int
#    #DeltaOrigine    : float
#    #G               : float
#    #Gseism          : float
#    #Rezultate       : int
#    #Ks              : float
#    #Beta            : float
#    #Eps             : float
#    #mm              : int
#    #mc              : int
#    Denumire        : str
#    vEtaje          : List[Etaj]
#    def __init__(self):
#        self.Dim         = [0 ,0 ,0]
#        self.nre         = 0
#        self.nrn         = 0
#        self.mesaj1      = "Mesaj1"
#        self.mesaj2      = "Mesaj2"
#        self.titludesen  = "TitulDesen"
#        self.vEtaje      = []


dictTipElem = {0 : "pereti plini sau spaleti in consola", 1 : "spaleti dublu incastrati la capete" }

class Cladire:
    Dim             : Tuple [float, float, float]
    Scara           : int
    Rotire          : int
    DeltaOrigine    : float
    nre : int  #numarul de etaje
    nrn : int 
    mesaj1 : str
    mesaj2 : str
    TitluDesen : str
    Denumire        : str
    vecEtaje : List[Etaj]
    mm : int #marca mortar
    mc : int #marca caramida
    ks      : float
    beta    : float
    eps     : float
    forta   : float
    G       : float
    GSeism  : float
    Rezultate : float
    rc      : float
    rt      : float
    R1      : float
    R2      : float
    qc1     : float
    qc2     : float

    def __init__(self) :   
        self.Dim         = [0 ,0 ,0]     
        self.Scara = 1
        self.Rotire = 0
        self.DeltaOrigine = 0
        self.nre = 0
        self.nrn = 0
        self.mesaj1 = "Mesaj1"
        self.mesaj2 = "Mesaj1"
        self.TitluDesen = "TitluDesen"
        self.Denumire = "Denumire"
        self.vecEtaje = []
        self.mm = 0
        self.mc = 0
        self.ks = 0
        self.beta = 0
        self.eps = 0
        self.forta = 0
        self.G = 0
        self.GSeism = 0
        self.Rezultate = 0
        self.rc = 0
        self.rt = 0
        self.R1 = 0
        self.R2 = 0
        self.qc1 = 0
        self.qc2 = 0

    def GetElement(self, etaj, nrelem) -> Element:
        return self.vecEtaje[etaj].vElem[nrelem]
