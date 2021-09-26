.AUTODEPEND

#		*Translator Definitions*
CC = bcc +ZIDARIE.CFG
TASM = TASM
TLIB = tlib
TLINK = tlink
LIBPATH = F:\BORLANDC\LIB
INCLUDEPATH = F:\BORLANDC\INCLUDE


#		*Implicit Rules*
.c.obj:
  $(CC) -c {$< }

.cpp.obj:
  $(CC) -c {$< }

#		*List Macros*


EXE_dependencies =  \
 {$(LIBPATH)}grafice.lib \
 main.obj \
 utile.obj \
 casa.obj \
 calcule.obj \
 desenare.obj \
 inout.obj

#		*Explicit Rules*
zidarie.exe: zidarie.cfg $(EXE_dependencies)
  $(TLINK) /x/c/d/P-/L$(LIBPATH) @&&|
c0h.obj+
main.obj+
utile.obj+
casa.obj+
calcule.obj+
desenare.obj+
inout.obj
zidarie
		# no map file
grafice.lib+
graphics.lib+
emu.lib+
mathh.lib+
ch.lib
|


#		*Individual File Dependencies*
main.obj: zidarie.cfg main.c 

utile.obj: zidarie.cfg utile.c 

casa.obj: zidarie.cfg casa.c 

calcule.obj: zidarie.cfg calcule.c 

desenare.obj: zidarie.cfg desenare.c 

inout.obj: zidarie.cfg inout.c 

#		*Compiler Configuration File*
zidarie.cfg: zidarie.mak
  copy &&|
-mh
-w+
-j30
-g50
-i20
-G
-O
-Og
-Oe
-Om
-Ov
-Ol
-Ob
-Op
-Oi
-Z
-k-
-vi-
-I$(INCLUDEPATH)
-L$(LIBPATH)
| zidarie.cfg


