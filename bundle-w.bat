REM deletes any existing build of checkLeague, then creates a new windowed build, copying in 'userInfo.txt' to the directory holding 'checkLeague.exe' for proper function
rd /Q /S build,dist
del checkLeague.spec
pyinstaller checkLeague.py
cd dist\checkLeague
copy ..\..\userInfo.txt .
