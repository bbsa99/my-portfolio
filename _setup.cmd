@echo off
set PATH=C:\Users\amanu\flutter\bin;%PATH%
cd /d "C:\Users\amanu\.cline\data\workspaces\chat\yonas project\TaxiMeter_Flutter"
echo === flutter --version ===
flutter.bat --version
echo === config enable-web ===
flutter.bat config --enable-web --no-analytics
echo === pub get ===
flutter.bat pub get
echo === SETUP_DONE ===
