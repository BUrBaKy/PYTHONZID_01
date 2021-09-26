import numpy as np
import math
from .structura import *
from .cladire import *

class MotorCalcul(object):
    """Clasa se va ocupa cu efectuarea calculelor"""
    def __init__(self) -> None:
        super().__init__()

    def lat(self, elem : Element, i : int):
        return elem.vecD[i].b, elem.vecD[i].h, elem.vecD[i].d2, elem.d2cgl, elem.vecD[i].d1, elem.d1cgl

    def pas3(self, elem : Element):
        nrd = elem.nrd
        elem.arie = sd1 = sd2 = 0.0
        arie = []
        d2cg = []
        d1cg = []
        for i in range(nrd):
            bi, hi, d2i, d2cgli, d1i, d1cgli = self.lat(elem, i)
            arie.append(bi * hi)
            sd1 += arie[i] * elem.vecD[i].d2
            sd2 += arie[i] * elem.vecD[i].d1
            elem.arie += arie[i]
        elem.d1cgl = sd2 / elem.arie
        elem.d2cgl = sd1 / elem.arie
        elem.ecgd1 = elem.icgd2 = 0.0
        for i in range(nrd):
            bi, hi, d2i, d2cgli, d1i, d1cgli = self.lat(elem, i)
            d2cg.append(d2i - d2cgli)
            d1cg.append(d1i - d1cgli)
            elem.icgd1 += bi * pow(hi, 3) / 12 + arie[i] *pow(d2cg[i], 2)
            elem.icgd2 += hi * pow(bi, 3) / 12 + arie[i] *pow(d1cg[i], 2)
        max = -1.0E35
        min = 1.0E35
        for i in range(nrd):
            bi, hi, d2i, d2cgli, d1i, d1cgli = self.lat(elem, i)
            disti = d2cg[i] - hi / 2
            if(disti < min):
                min = disti
            if(disti > max):
                max = disti
        elem.y2 = -min
        elem.y1 = +max
        elem.arin = (-min + max) * elem.gri
        elem.w1cg = math.fabs(elem.icgd1 / elem.y1)
        elem.w2cg = math.fabs(elem.icgd1 / elem.y1)
        elem.r1 = elem.w2cg / elem.arie
        elem.r2 = elem.w1cg / elem.arie

    def pas5(self, elem : Element):
        elem.sigma0 = elem.N * 1e3 / elem.arie # 1t*1000/cm2. kg/cm2 */

    def pas71(self, casa : Cladire):
        tabel2 = np.array([[44.0,36.0,34.0,30.0,26.0,20.0],
                           [36.0,30.0,28.0,26.0,22.0,18.0],
                           [32.0,26.0,24.0,20.0,18.0,14.0],
                           [28.0,24.0,22.0,18.0,14.0,12.0]])
        tabel3 = np.array([2.7,1.8,0.9,0.45])
        casa.rc = tabel2[casa.mm][casa.mc]
        casa.rt = tabel3[casa.mm]

    def pas72(self, casa : Cladire, el : Element):
        tabel40 = np.array([0.5,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0])
        tabel41 = np.array([[1.9,2.1,2.3,2.6,2.8,3.0,3.2,3.4,3.5,3.7,3.9,4.0,4.2],
                           [1.3,1.5,1.7,1.9,2.1,2.3,2.5,2.6,2.8,2.9,3.0,3.2,3.3],
                           [0.7,0.8,1.0,1.2,1.3,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2],
                           [0.4,0.5,0.7,0.8,0.9,1.0,1.1,1.2,1.2,1.3,1.4,1.5,1.5]])
        tabel42 = np.array([[      #/*       c200     */
                            [0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7],
                            [0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2],
                            [0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6],
                            [0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9]],
                           [#      /*       c150     */
                            [0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7],
                            [0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2],
                            [0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6],
                            [0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9]],
                           [#      /*       c125     */
                            [0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7],
                            [0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2],
                            [0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6],
                            [0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9]],
                           [#      /*       c100     */
                            [0.1,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5,2.8,3.1,3.4,3.7],
                            [0.1,0.3,0.5,0.8,1.1,1.3,1.6,1.9,2.2,2.4,2.7,3.0,3.2],
                            [0.1,0.2,0.4,0.6,0.9,1.1,1.3,1.5,1.7,2.0,2.2,2.4,2.6],
                            [0.1,0.1,0.3,0.5,0.6,0.8,0.9,1.1,1.3,1.4,1.6,1.7,1.9]],
                           [#     /*        c75      */
                            [0.1,0.3,0.6,1.0,1.3,1.6,2.0,2.3,2.6,3.0,3.3,3.6,4.0],
                            [0.1,0.3,0.6,0.9,1.2,1.5,1.7,2.0,2.3,2.6,2.9,3.2,3.5],
                            [0.1,0.2,0.4,0.7,0.9,1.1,1.3,1.6,1.8,2.1,2.3,2.5,2.7],
                            [0.1,0.2,0.3,0.5,0.7,0.9,1.0,1.2,1.4,1.6,1.8,2.0,2.1]],
                           [#    /*         c50      */
                            [0.2,0.4,0.7,1.1,1.5,1.9,2.3,2.7,3.1,3.5,3.9,4.3,4.6],
                            [0.2,0.3,0.7,1.0,1.3,1.6,2.0,2.3,2.6,3.0,3.3,3.6,4.0],
                            [0.1,0.2,0.5,0.8,1.0,1.3,1.5,1.8,2.1,2.3,2.6,3.8,3.1],
                            [0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4]]])

        sig0 = el.sigma0
        linie = casa.mm
        mc = casa.mc
        col = -1
        for i in range(12):
            if sig0 >= tabel40[i] and sig0 < tabel40[i+1]:
                col = i
        if col == -1:
            it = 0
            if sig0 <= tabel40[0]:
                col = 0
            else:
                col = 12
        else:
            it = 1
        
        # Interpolare liniara in tabel pentru calculul Tau0fcap.in daN/cm2
        if it:
            el.tau0fc = tabel41[linie][col] + (sig0 - tabel40[col]) * (tabel41[linie][col+1] - tabel40[col]) / (tabel40[col+1] - tabel40[col])
            el.tau0uc = tabel42[mc][linie][col] + (sig0 - tabel40[col])*(tabel42[mc][linie][col+1] - tabel42[mc][linie][col]) / (tabel40[col+1] - tabel40[col])
        else:
            el.tau0fc = tabel41[linie][col]
            el.tau0uc = tabel42[mc][linie][col]
    
    def pas8(self, el : Element):
        el.mf1 = el.N * el.r1 / 100. # T*m
        el.mf2 = el.N * el.r2 / 100.
    
    def pas9(self, el : Element, casa : Cladire):
        el.ac = el.sigma0 / casa.rc * el.arie
    
    def pas1011(self, el : Element):
        pas = 0.01 # 1 mm
        nrd = el.nrd
        arie_impusa = el.ac
        x = el.y1
        ar = 0.0
        ms = 0.0
        while True: # pentru capatul de sus 'coord d2 maxima'
            x -= pas
            for i in range(nrd):
                d2i = el.vecD[i].d2
                hi = el.vecD[i].h
                x1=d2i + hi/2 * el.d2cgl
                x2=d2i - hi/2 * el.d2cgl
                if (x < x1) and (x > x2):
                    bi = el.vecD[i].b
                    da = pas * bi
                    ar += da
                    ms += da*x
            if not(ar<arie_impusa):
                break
        el.xu1 = el.y1 - (x + 0.5 * pas)
        el.c1 = el.y1 - ms/ar
        x = 0.0
        ar = 0.0
        ms = 0.0
        x = -el.y2
        while True: # pentru capatul de jos 'coord d2 minima'
            x+=pas
            for i in range(nrd):
                d2i = el.vecD[i].d2
                hi = el.vecD[i].h
                x1 = d2i + hi / 2 - el.d2cgl
                x2 = d2i - hi / 2 - el.d2cgl
                if (x < x1) and (x > x2):
                    bi = el.vecD[i].b
                    da = pas * bi
                    ar += da
                    ms += da * x
            if not(ar < arie_impusa):
                break
        el.xu2 = el.y2 - math.fabs(x - 0.5*pas)
        el.c2 = el.y2 - math.fabs(ms/ar)

    def pas12(self, el : Element) -> None:
        if el.tip == 0 :
            el.qf1 = 1.5 * el.mf1 / el.h * 100.0
            el.qf2 = 1.5 * el.mf2 / el.h * 100.0
        else :
            el.qf1 = 2.0 * el.mf1 / el.h * 100.0
            el.qf2 = 2.0 * el.mf2 / el.h * 100.0

    def pas13(self, el : Element) -> None:
        el.mu1 = el.N * (el.y1 - el.c1) / 100.0
        el.mu2 = el.N * (el.y2 - el.c2) / 100.0

    def pas14(self, el : Element) -> None:
        if el.tip == 0 :
            el.qu1 = 1.5 * el.mu1 / el.h * 100.0
            el.qu2 = 1.5 * el.mu2 / el.h * 100.0
        else:
            el.qu1 = 2.0 * el.mu1 / el.h * 100.0
            el.qu2 = 2.0 * el.mu2 / el.h * 100.0
    
    def pas15(self, el : Element) -> None:
        el.qfic = el.tau0fc * el.arin / 1000.0

    def pas16(self, el : Element) -> None:
        el.qui = el.tau0uc * el.arin / 1000.0

    def pas17(self, el : Element) -> None:
        el.ql = 0.7 * el.N

    def pas18(self, el : Element) -> None:
        # directia 1
        if el.qu1 > el.qfic :
            el.qcap1 = min(el.qu1, el.qfic, el.ql)
        else:
            el.qcap1 = min(el.qu1, el.qui, el.ql)
        # directia 2
        if el.qu2 > el.qfic :
            el.qcap2 = min(el.qu2, el.qfic, el.ql)
        else:
            el.qcap2 = min(el.qu2, el.qui, el.ql)
            
    def pas1926(self, el : Element) -> None:
        #psi 1
        if (el.qfic >= el.qu1):
            el.psi1 = 0.8
        else:
            if ((el.qfic - el.qf1) / (el.qu1 - el.qf1) <= 0.2):
                el.psi1 = 0.8
            else:
                el.psi1 = 0.8 - 0.5 * ((el.qfic - el.qf1) / (el.qu1 - el.qf1))
        #psi 2
        if ( el.qfic >= el.qu2 ):
            el.psi2 = 0.3
        else:
            if (el.qfic <= el.qf2):
                el.psi2 = 0.8
            else:
                if(((el.qfic - el.qf2)/(el.qu2 - el.qf2))<=0.2) :
                    el.psi2 = 0.8
                else:
                    el.psi2 = 0.8 - 0.5*(el.qfic - el.qf2)/(el.qu2 - el.qf2)
  
    def pas27(self, casa : Cladire ,i : int) -> None:
        pq=q=0.0;
        etajCrt = casa.vecEtaje[i]
        
        for elemCrt in etajCrt.vElem:  #iterare peste elementele etajului i
            pq += elemCrt.psi1 * elemCrt.qcap1
            q += elemCrt.qcap1  
        
        if  (q != 0):
            etajCrt.psimed1 = pq / q

        pq=q=0.0
        for elemCrt in etajCrt.vElem:  #iterare peste elementele etajului i
            pq += elemCrt.psi2 * elemCrt.qcap2
            q += elemCrt.qcap2  
        
        if  (q != 0):
            etajCrt.psimed2 = pq / q
        
    def pas28(self, casa : Cladire) -> None:
        qc1=0.0 
        qc2=0 
        g=0.0
        GSeism=0.0                
        etaj0 = casa.vecEtaje[0]
        for elemCrt in etaj0.vElem:
            qc1 += elemCrt.qcap1
            qc2 += elemCrt.qcap2
            if ( casa.GSeism == 0.0 ):
                GSeism += elemCrt.Nseism
            g += elemCrt.N
        
        casa.G = g

        if ( casa.GSeism == 0 ):
            casa.GSeism = GSeism

        casa.qc1 = qc1
        casa.qc2 = qc2
        if (casa.ks * casa.beta * etaj0.psimed2 * casa.eps * casa.GSeism !=0 ):
            casa.R2 = qc2 / (casa.ks * casa.beta * etaj0.psimed2 * casa.eps * casa.GSeism) #cod modificat de la casa.R2 = qc2 / (casa.ks * casa.beta * casa.vecEtaje[etaj0].psimed2 * casa.epsilon * casa.GSeism)
        else:
            casa.R2 = -1
        if (casa.ks * casa.beta * etaj0.psimed1 * casa.eps * casa.GSeism != 0):
            casa.R1 = qc1 / (casa.ks * casa.beta * etaj0.psimed1 * casa.eps * casa.GSeism) #cod modificat de la casa.R1 = qc1 / (casa.ks * casa.beta * casa.vecEtaje[etaj0].psimed1 * casa.epsilon * casa.GSeism)
        else:
            casa.R1 = -1

    def Calculeaza(self, casa : Cladire) -> None:
        self.pas71(casa)
        for iEtaj, etajCrt in enumerate(casa.vecEtaje): #iterare peste toate etajele 
            #Etapa 3 din schema aplicata pe tot etajul i 
            msd1j = msd2j = ariej = 0.0
            for j, eleCrt in enumerate(etajCrt.vElem):
                #gotoxy(1,6)
                print("Pas 3 element ", j+1)
                self.pas3(eleCrt)
                msd1j += eleCrt.arie * eleCrt.d2cgl
                msd2j += eleCrt.arie * eleCrt.d1cgl
                ariej += eleCrt.arie
            
            etajCrt.d1cg = msd2j / ariej #      coord. CG etaj         
            etajCrt.d2cg = msd1j / ariej
            etajCrt.arie = ariej  
                
            if (casa.forta != 0):
                for eleCrt in etajCrt.vElem:
                    eleCrt.proc_arie = eleCrt.arie / ariej
                    eleCrt.N = casa.forta * eleCrt.proc_arie
                
            icmd1j = icmd2j = d2icmd1j = d1icmd2j = 0.0
            for elemCrt in etajCrt.vElem:
                d2icmd1j += elemCrt.icgd1 * (elemCrt.d2cgl - etajCrt.d2cg)
                icmd1j   += elemCrt.icgd1 + elemCrt.arie * math.pow((elemCrt.d2cgl - etajCrt.d2cg),2)
                d1icmd2j += elemCrt.icgd2 * (elemCrt.d1cgl - etajCrt.d1cg)
                icmd2j   += elemCrt.icgd2 + elemCrt.arie * math.pow((elemCrt.d1cgl - etajCrt.d1cg),2)

            etajCrt.d1cr = d1icmd2j / icmd2j    # coord. CR fata de CM
            etajCrt.d2cr = d2icmd1j / icmd1j

            #Etapa 4 din schema aplicata pe tot etajul i
            #Forta N pe element este data de intrare
            #Etapa 5 din schema aplicata pe tot etajul i

            for idx, elemCrt in enumerate(etajCrt.vElem):
                #gotoxy(1,6)
                print('Pas 5 element {}'.format(idx))
                self.pas5(elemCrt)
                if elemCrt.sigma0 > 0.99 * casa.rc:
                    print('Eroare: Sigma0[elementul {}]={} > Rc[elementul {}]={}'.format(idx+1, elemCrt.sigma0, idx+1, 0.99*casa.rc))
                    return

            #/*   Etapa 6 din schema aplicata pe tot etajul i. */
            #/*   Marca mortarului, respectiv caramizii este   */
            #/*  data de intrare.                              */
            #
            #/*   Etapa 7.1 este comuna pentru toata casa.*/
            #/*   S-a executat la inceput.                */
            #
            #/*   Etapa 7.2 din schema aplicata pe tot etajul i.*/

            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 7-2 element {}.'.format(idx+1))
                self.pas72(casa, elemCrt)
            
            #/*   Etapa 8 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 8 element {}.'.format(idx+1))
                self.pas8(elemCrt)

            #/*   Etapa 9 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 9 element {}.'.format(idx+1))
                self.pas9(elemCrt, casa)

            #/*   Etapele 10 si 11 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 10-11 element {}.'.format(idx+1))
                self.pas1011(elemCrt)
            
            #/*   Etapa 12 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 12 element {}.'.format(idx+1))
                self.pas12(elemCrt)

            #/*   Etapa 13 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 13 element {}.'.format(idx+1))
                self.pas13(elemCrt)

             #/*   Etapa 14 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 14 element {}.'.format(idx+1))
                self.pas14(elemCrt)

             #/*   Etapa 15 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 15 element {}.'.format(idx+1))
                self.pas15(elemCrt)

             #/*   Etapa 16 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 16 element {}.'.format(idx+1))
                self.pas16(elemCrt)

             #/*   Etapa 17 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 17 element {}.'.format(idx+1))
                self.pas17(elemCrt)

             #/*   Etapa 18 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 18 element {}.'.format(idx+1))
                self.pas18(elemCrt)

             #/*   Etapele 19-26 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 19-26 element {}.'.format(idx+1))
                self.pas1926(elemCrt)

             #/*   Etapa 27 din schema aplicata pe tot etajul i.*/
            for idx, elemCrt in enumerate(etajCrt.vElem):
                print('Pas 27')
                self.pas27(casa, iEtaj)
        
        print('Pas 28 {}.'.format(idx+1))
        self.pas28(casa)