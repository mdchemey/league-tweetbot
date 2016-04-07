rd /Q /S build,dist
del checkLeague.spec
pyinstaller checkLeague.py
cd dist\checkLeague
copy ..\..\userInfo.txt .