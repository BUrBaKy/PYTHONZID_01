cls
@echo off
if %1. == . goto ERROR

zidarie %1 %1.out %2
goto END

:ERROR
@echo.
@echo Sintaxa este :  rulare 'nume_problema' [ SVGA, GIF ] .
@echo.
goto END

:END




