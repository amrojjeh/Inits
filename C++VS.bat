REM Uses VS Compiler

@echo off

REM -------- BUILD.BAT --------
echo @echo off > build.bat
echo pushd Code\ >> build.bat
echo if not defined DevEnvDir (call vcvarsall x64) >> build.bat
echo cl main.cpp /Zi >> build.bat
echo move main.exe ..\ >> build.bat
echo popd >> build.bat

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