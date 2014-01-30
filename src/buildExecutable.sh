echo "If these fail, check your installation of pyinstaller"
pyinstaller -w -F gui.py
cp add.gif dist/add.gif
cp delete.gif dist/delete.gif
cp edit.gif dist/edit.gif
cp logo.gif dist/logo.gif