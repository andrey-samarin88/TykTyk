установка библиотек:
pip install pgzero
pip install pyinstaller

сборка:
pyinstaller --onefile --windowed --collect-data pgzero --name "TykTyk" tyk_tyk.py

прочее:
сброс кэша:
git rm -r -f --cached .idea