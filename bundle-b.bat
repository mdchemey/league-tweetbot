rd /Q /S build,dist
del checkLeague.spec
pyinstaller -w checkLeague.py
cd dist\checkLeague
copy ..\..\userInfo.txt .