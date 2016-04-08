REM deletes any existing build of checkLeague, then creates a new windowless build, copying in 'userInfo.txt' to the directory holding 'checkLeague.exe' for proper function
rd /Q /S build,dist
del checkLeague.spec
pyinstaller -w checkLeague.py
cd dist\checkLeague
copy ..\..\userInfo.txt .
