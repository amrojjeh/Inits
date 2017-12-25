REM Uses the Visual Studio Compiler

@echo off

REM -------- BUILD.BAT --------
echo @echo off > built.bat
echo pushd Code\ >> built.bat
echo if not defined DevEnvDir (call vcvarsall x64) >> built.bat
echo cl main.cpp /Zi >> built.bat
echo move main.exe ..\ >> built.bat
echo popd >> built.bat

REM -------- CLEAN.BAT --------
echo @echo off > clean.bat
echo rd .vs\ /S /Q >> clean.bat
echo pushd Code\ >> clean.bat
echo del *.ilk >> clean.bat
echo del *.obj >> clean.bat
echo del *.pdb >> clean.bat
echo del *.exe >> clean.bat

REM -------- DIRECTORIES & EXTRA FILES --------
mkdir Code\
echo > Code\main.cpp
