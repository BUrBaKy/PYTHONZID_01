import pdb
import os
from tkinter import messagebox

from .structura import *

class Inout():
    CaleFisierIn : str
    CaleFisierOut : str
    def __init__(self, CaleIn, CaleOut):
        if CaleIn == '':
            CaleIn = 'D:\\-=Lucru=-\\Programare\\ZIDSURSA\\CIULL.txt'
        if CaleOut == '':
            CaleOut = 'D:\\-=Lucru=-\\Programare\\ZIDSURSA\\CIULL.OUT'

        self.CaleFisierIn = CaleIn
        self.CaleFisierOut = CaleOut   
        
    def DeschideSiCiteste(self, oCladire):
        messagebox.showinfo("CaleFisierIn", self.CaleFisierIn)
        fisier = open(self.CaleFisierIn, "r")
        messagebox.showinfo("DeschideSiCiteste()", "DeschideSiCiteste()")
        count = 0
        while True:
            count += 1
            if (count > 4):
                break
            linie = fisier.readline()
            messagebox.showinfo("LinieCuLinie", linie)
            self.ParseLine(linie)
        fisier.close()
    
    def CitesteElement(self, fisier, linie, oCladire : Cladire, elemCrt:Element):
        if not linie:
            return
        #Nume
        elemCrt.nume = linie
        #Tipul
        for _ in range(0,4):
            linie = fisier.readline()
        #tipul = int(linie)
        #elemCrt.tip = (tipul, dictTipElem[tipul])
        elemCrt.tip = int(linie)
        #Inaltime
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(':')
        elemCrt.h = float(lista[0]) #cm
        #Forta N pe element si forta pentru seism.
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(' ')
        elemCrt.N = float(lista[0]) # tone
        elemCrt.Nseism = float(lista[1]) # tone
        #Nr de dreptunghiuri pe element
        linie = fisier.readline()
        linie = fisier.readline()
        elemCrt.nrd = int(linie)
        for _ in range(0,4):
            linie = fisier.readline()
        for _ in range(0, elemCrt.nrd):
            linie = fisier.readline()
            lista = linie.split(' ')
            b = float(lista[0]) * oCladire.Scara
            h = float(lista[1]) * oCladire.Scara
            d1 = float(lista[2]) * oCladire.Scara
            d2 = float(lista[3]) * oCladire.Scara
            if (oCladire.Rotire == -1):
                new_d1  =  d2 + 0.5 * h
                new_d2  = -d1 + oCladire.DeltaOrigine -0.5 * b
                new_b   = h
                new_h   = b
            elif (oCladire.Rotire == 0):
                new_d1  = d1 + 0.5 * b
                new_d2  = d2 + 0.5 * h
                new_b   = b
                new_h   = h
            elif (oCladire.Rotire == 1):
                new_d1  = -d2 + oCladire.DeltaOrigine -0.5 * h
                new_d2  =  d1 + 0.5 * b
                new_b   =  h
                new_h   =  b
            noudreptunghi = Dreptunghi(new_b, new_h, new_d1, new_d2)
            elemCrt.vecD.append(noudreptunghi)
        #Grosime inima element
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(' ')
        if (oCladire.Rotire != 0):
            elemCrt.Grosime = float(lista[1])
        else :
            elemCrt.Grosime = float(lista[0])
            
    def CiteseFisier(self, oCladire : Cladire):
        fisier = open(self.CaleFisierIn, "r")        
        linie = fisier.readline()
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(':')
        oCladire.Dim = lista[0].split(' ')
        
        linie = fisier.readline()
        lista = linie.split(':')
        lista = lista[0].split(' ')
        oCladire.Scara = float(lista[0])

        linie = fisier.readline()
        lista = linie.split(':')
        lista = lista[0].split(' ')
        oCladire.Rotire = float(lista[0])

        linie = fisier.readline()
        lista = linie.split(':')
        lista = lista[0].split(' ')
        oCladire.G = float(lista[0])

        linie = fisier.readline()
        linie = fisier.readline()
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(':')
        lista = lista[0].split(' ')
        oCladire.Gseism = float(lista[0])

        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(':')
        lista = lista[0].split(' ')
        oCladire.Rezultate = int(lista[0])

        linie = fisier.readline()
        linie = fisier.readline()
        linie = fisier.readline()
        lista = linie.split(' ')
        while('' in lista) :
            lista.remove('')
        oCladire.ks = float(lista[0])
        oCladire.beta = float(lista[1])
        oCladire.eps = float(lista[2])
        #Marca mortarului
        while True :
            linie = fisier.readline()
            if "Mortarul" in linie :
                linie = fisier.readline()
                oCladire.mm = int(linie)
                break
        #Marca caramizii
        linie = fisier.readline()
        linie = fisier.readline()
        oCladire.mc = int(linie)
        mesaj = "O Cladire \n Marca mortar: " + str(oCladire.mm) + "\n Marca caramida: " + str(oCladire.mc) + "\n"
        #messagebox.showinfo("Detalii cladire",mesaj)
        #Denumire
        while True :
            linie = fisier.readline()
            if "Denumire" in linie :
                lista = linie.split('=')
                oCladire.Denumire = lista[1]
                break
        #Sarim peste longitudinal / transversal
        while True :
            linie = fisier.readline()
            if "Numarul de elemente" in linie :
                lista = linie.split(':')
                etajNou = Etaj()
                etajNou.nre = int(lista[0])
                break
        elemCurent = 0
        #while pe elemente
        while elemCurent < etajNou.nre and linie :
            while linie :
                linie = fisier.readline()
                if ':' in linie:
                    break
            linie = fisier.readline()
            #New element
            elemCrt = Element()
            self.CitesteElement(fisier, linie, oCladire, elemCrt)
            etajNou.vElem.append(elemCrt)
            elemCurent+=1
        oCladire.vecEtaje.append(etajNou)
        oCladire.nre = oCladire.vecEtaje.__len__()
        fisier.close()
    
    def ParseLine(self, linestring):
        ListOut = linestring.split(':')
        messagebox.showinfo("Linie impartita dupa :", ListOut)
    
    def Convert(i:int, j:int) -> str:        
        i1_switch = {
            0: 'C200',
            1: 'C150',
            2: 'C125',
            3: 'C100',
            4: 'C75',
            5: 'C50' }
        i2_switch = {
            0: 'M50',
            1: 'M25',
            2: 'M10',
            3: 'M4'}
        if i==1:
            return i1_switch(j)
        else:
            return i2_switch(j)

    def SalvareDate(self, casa : Cladire):
        try:
            if os.path.exists(self.CaleFisierOut):
                os.remove(self.CaleFisierOut)
            fisier = open(self.CaleFisierOut,"w")
        
            fisier.write('\n')
            fisier.write('Program  :   ZIDARIE\n\n')
            fisier.write('Autori   :   prof. dr. ing. Radu Agent\n')
            fisier.write('             ing. Nicolae Mihaila\n')
            fisier.write('             ing. Stefan Epure\n\n')

            fisier.write('Denumire : {}\n'.format(casa.mesaj1))
            fisier.write('         : {}\n'.format(casa.mesaj2))

            fisier.write('\n Unitatile de masura sunt:\n')
            fisier.write('\n Lungimi  :  <cm>:')
            fisier.write('\n Arii     :  <cm2>:')
            fisier.write('\n Forte    :  <tone>:')
            fisier.write('\n Eforturi :  <daN/cm2>:')
            fisier.write('\n Momente  :  <t*m>:')

            fisier.write('\n\n\n\t\t  D A T E L E  D E  I N T R A R E: \n\n')
            fisier.write('\n\n Materiale : ')
            fisier.write('\n\nMarca de caramida folosita este {}'.format(self.Convert(1,casa.mc)))
            fisier.write('\nMarca de mortar folosit este {}'.format(self.Convert(2,casa.mm)))
            fisier.write('\n\n Coeficientii seismici : ks={:.1f}  beta={:.1f}  epsilon={:.1f}'.format(casa.ks, casa.beta, casa.eps))
            fisier.write('\n\n\n Geometria:        < Fata de sistemul de referinta al nivelului. >\n')

            for i, etajCrt in enumerate(casa.vecEtaje):
                for j, elemCrt in enumerate(etajCrt.vElem):
                    fisier.write('\n\n\n      Elementul {} are {} dreptunghiuri. '.format(elemCrt.nume, elemCrt.vecD.__len__))
                    fisier.write('\n\n\tb\th\td1\td2\n')
                    for k, dCrt in enumerate(elemCrt.vecD):
                        fisier.write('\n{:d}:\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}'.format(k+1, dCrt.b, dCrt.h, dCrt.d1, dCrt.d2))
                    fisier.write('\n\n   Grosime inima                 : {:.2f}'.format(elemCrt.gri))
                    fisier.write('\n   Forta in element              : {:.2f}'.format(elemCrt.N))
                    fisier.write('\n   Forta in element pentru seism : {:.2f}'.format(elemCrt.Nseism))
            if casa.Rezultate:
                fisier.write('\n\n\t\t    R  E  Z  U  L  T  A  T  E  L  E     C  O  M  P  L  E  T  E')
            else:
                fisier.write('\n\n\t\t    R  E  Z  U  L  T  A  T  E  L  E ')

            for i, etajCrt in enumerate(casa.vecEtaje):
                if casa.Rezultate:
                    fisier.write('\n\n     Centrul de greutate     :        d1 ={:.2f}          d2 ={:.2f}'.format(etajCrt.d1cg, etajCrt.d2cg))
                    fisier.write('\n\n     Centrul de rigiditate   : d1cr-d1cm ={:.2f}   d1cr-d1cm ={:.2f}'.format(etajCrt.d1cr, etajCrt.d2cr))
                else:
                    fisier.write('\n\n     Incarcarea pe nivel     :              N = {:.3f}'.format(casa.G))
                    fisier.write('\n     Incarcarea pentru seism :         Nseism = {:.3f}'.format(casa.GSeism))
                    fisier.write('\n          Aria zidurilor     :              A = {:.3f}'.format(etajCrt.arie))
            
                for j, elemCrt in enumerate(etajCrt.vElem):
                    fisier.write('\n\n\n                 Elementul  {}'.format(elemCrt.nume))
                    if casa.Rezultate:
                        fisier.write('\n\nArie\ty1\ty2\tArin\tIcgd1\tIcgd2\tW1cg\tW2cg\n')
                        fisier.write('\n{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.4f}\t{:.4}'.format(
                            elemCrt.arie, elemCrt.y1, elemCrt.y2, elemCrt.arin, elemCrt.icgd1, elemCrt.icgd2, elemCrt.w1cg, elemCrt.w2cg))
                        fisier.write('\n\nSigma0\ttau0fc\ttau0uc\tMf1\tMf2\tAc1,2\txu1\txu2\n')
                        fisier.write('\n{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.4f}\t{:.4f}\t{:.4}'.format(
                            elemCrt.sigma0, elemCrt.tau0fc, elemCrt.tau0uc, elemCrt.mf1, elemCrt.mf2, elemCrt.ac, elemCrt.xu1, elemCrt.xu2))
                        fisier.write('\n\nc1\tc2\tQf1\tQf2\tMu1\tMu2\tQu1\tQu2\n')
                        fisier.write('\n{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.4f}\t{:.4f}\t{:.4}'.format(
                            elemCrt.c1, elemCrt.c2, elemCrt.qf1, elemCrt.qf2, elemCrt.mu1, elemCrt.mu2, elemCrt.qu1, elemCrt.qu2))
                        fisier.write('\n\nQficap\tQui\tQl\tQcap1\tQcap2\tpsi1\tpsi2\tArie\n')
                        fisier.write('\n{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.4f}\t{:.4}'.format(
                            elemCrt.qfic, elemCrt.qui, elemCrt.ql, elemCrt.qcap1, elemCrt.qcap2, elemCrt.psi1, elemCrt.psi2, elemCrt.proc_arie))
                    else:
                        fisier.write('\n\nArie\tArie inima')
                        fisier.write('\n{:.2f}\t{:.2f}'.format(elemCrt.arie, elemCrt.arin))
                        fisier.write('\n\nSigma0\ttau0fc\ttau0uc\n')
                        fisier.write('\n{:.2f}\t{:.2f}\t{:.2f}'.format(
                            elemCrt.sigma0, elemCrt.tau0fc, elemCrt.tau0uc))
                        fisier.write('\n\nQf1\tQf2\tQficap\n')
                        fisier.write('\n{:.3f}\t{:.3f}\t{:.3f}'.format(
                            elemCrt.qf1, elemCrt.qf2, elemCrt.qfic))
                        fisier.write('\n\nQu1\tQu2\tQui\tQl\n')
                        fisier.write('{:.3f}{:.3f}{:.3f}{:.3f}'.format(elemCrt.qu1, elemCrt.qu2, elemCrt.qui, elemCrt.ql))
                        fisier.write('\n\nQcap1\tQcap2\n')
                        fisier.write('{:.3f}{:.3f}'.format(elemCrt.qcap1, elemCrt.qcap2))
                        fisier.write('\n\nPsi1\tPsi2\n')
                        fisier.write('{:.3f}{:.3f}'.format(elemCrt.psi1, elemCrt.psi2))
                fisier.write('\n\n\n\n\n\t      C O N C L U Z I I   C A L C U L\n')
                fisier.write('\n\nQcap.1 = {:.3f}\tQcap.2 = {:.3f}\n'.format(casa.qc1, casa.qc2))
                fisier.write('\n\Psi mediu 1 = {:.3f}\tPsi mediu 2 = {:.3f}\n'.format(etajCrt.psimed1, etajCrt.psimed2))
                fisier.write('\n\n    Gradul de acoperire al structurii:\n\n\t\tR1 = {:.2f}\n\t\tR2 = {:.2f}'.format(casa.R1, casa.R2))

            fisier.write('-=  S F A R S I T  =-')
            fisier.close()
        except Exception as e:
            messagebox.showinfo('Eroare la salvare!', 'Eroare la salvare!\n{}'.format(e))


                


