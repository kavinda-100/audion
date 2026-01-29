@echo off
REM Audion Music Player - Windows Installation Script
REM This script will clone the repository, install dependencies, and set up the application

setlocal EnableDelayedExpansion

REM Colors (using Windows 10+ ANSI support)
set "ESC=[0m"
set "RED=[31m"
set "GREEN=[32m"
set "BLUE=[34m"
set "YELLOW=[33m"

echo %BLUE%================================================%ESC%
echo %BLUE%    🎵 Audion Music Player Installation%ESC%
echo %BLUE%================================================%ESC%

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo %YELLOW%[WARNING]%ESC% Running as administrator. This is not required for user installation.
    choice /M "Continue anyway"
    if !errorlevel! neq 1 (
        echo %BLUE%[INFO]%ESC% Installation cancelled.
        exit /b 1
    )
)

echo %BLUE%[INFO]%ESC% Starting Audion Music Player installation...
echo.

REM Check for Python
echo %BLUE%[INFO]%ESC% Checking for Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%[ERROR]%ESC% Python is not installed or not in PATH.
    echo %BLUE%[INFO]%ESC% Please install Python 3.8+ from https://python.org
    echo %BLUE%[INFO]%ESC% Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo %GREEN%[SUCCESS]%ESC% Found Python %PYTHON_VERSION%

REM Check for Git
echo %BLUE%[INFO]%ESC% Checking for Git installation...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%[WARNING]%ESC% Git is not installed.
    echo %BLUE%[INFO]%ESC% Please install Git from https://git-scm.com/download/win
    choice /M "Continue without Git (manual download required)"
    if !errorlevel! neq 1 (
        exit /b 1
    )
    set GIT_AVAILABLE=false
) else (
    set GIT_AVAILABLE=true
    echo %GREEN%[SUCCESS]%ESC% Git is available
)

REM Set installation directory
set INSTALL_DIR=%USERPROFILE%\AppData\Local\Audion
set REPO_URL=https://github.com/your-username/audion.git

REM Setup repository
echo %BLUE%[INFO]%ESC% Setting up Audion repository...
if exist "%INSTALL_DIR%" (
    echo %BLUE%[INFO]%ESC% Existing installation found.
    if "%GIT_AVAILABLE%"=="true" (
        echo %BLUE%[INFO]%ESC% Updating from repository...
        cd /d "%INSTALL_DIR%"
        git pull origin main
        if !errorLevel! neq 0 (
            echo %YELLOW%[WARNING]%ESC% Failed to update repository. Continuing with existing files.
        )
    ) else (
        echo %YELLOW%[WARNING]%ESC% Cannot update without Git. Using existing files.
    )
) else (
    if "%GIT_AVAILABLE%"=="true" (
        echo %BLUE%[INFO]%ESC% Cloning Audion repository...
        git clone "%REPO_URL%" "%INSTALL_DIR%"
        if !errorLevel! neq 0 (
            echo %RED%[ERROR]%ESC% Failed to clone repository.
            echo %BLUE%[INFO]%ESC% Please manually download the source code to: %INSTALL_DIR%
            pause
            exit /b 1
        )
    ) else (
        echo %BLUE%[INFO]%ESC% Please manually download the source code to: %INSTALL_DIR%
        echo %BLUE%[INFO]%ESC% Download from: %REPO_URL%
        pause
        if not exist "%INSTALL_DIR%\audion.py" (
            echo %RED%[ERROR]%ESC% Source code not found in installation directory.
            exit /b 1
        )
    )
)

REM Change to installation directory
cd /d "%INSTALL_DIR%"
if %errorLevel% neq 0 (
    echo %RED%[ERROR]%ESC% Could not access installation directory: %INSTALL_DIR%
    exit /b 1
)

REM Setup Python virtual environment
echo %BLUE%[INFO]%ESC% Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    if !errorLevel! neq 0 (
        echo %RED%[ERROR]%ESC% Failed to create virtual environment.
        echo %BLUE%[INFO]%ESC% Make sure Python venv module is available.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo %BLUE%[INFO]%ESC% Activating virtual environment...
call venv\Scripts\activate.bat
if %errorLevel% neq 0 (
    echo %RED%[ERROR]%ESC% Failed to activate virtual environment.
    exit /b 1
)

REM Upgrade pip
echo %BLUE%[INFO]%ESC% Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo %BLUE%[INFO]%ESC% Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if !errorLevel! neq 0 (
        echo %RED%[ERROR]%ESC% Failed to install some dependencies.
        echo %BLUE%[INFO]%ESC% Trying to continue...
    )
) else (
    echo %BLUE%[INFO]%ESC% Installing core dependencies manually...
    pip install pygame mutagen
)

REM Install PyInstaller for building executable
echo %BLUE%[INFO]%ESC% Installing PyInstaller...
pip install pyinstaller

REM Build the application
echo %BLUE%[INFO]%ESC% Building Audion application...
if exist "build_executable.py" (
    python build_executable.py
) else (
    echo %BLUE%[INFO]%ESC% Creating executable with PyInstaller...
    if exist "assets\audion.ico" (
        pyinstaller --onedir --windowed --icon=assets\audion.ico --add-data "assets;assets" audion.py
    ) else (
        pyinstaller --onedir --windowed --add-data "assets;assets" audion.py
    )
)

if not exist "dist\audion\audion.exe" (
    echo %RED%[ERROR]%ESC% Failed to build application.
    pause
    exit /b 1
)

echo %GREEN%[SUCCESS]%ESC% Application built successfully!

REM Create desktop shortcut
echo %BLUE%[INFO]%ESC% Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Audion Music Player.lnk
set TARGET_PATH=%INSTALL_DIR%\dist\audion\audion.exe
set ICON_PATH=%INSTALL_DIR%\assets\audion.ico

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%TARGET_PATH%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%\dist\audion'; if (Test-Path '%ICON_PATH%') { $Shortcut.IconLocation = '%ICON_PATH%' }; $Shortcut.Description = 'Audion Music Player - A modern music player'; $Shortcut.Save()}"

if exist "%SHORTCUT_PATH%" (
    echo %GREEN%[SUCCESS]%ESC% Desktop shortcut created.
) else (
    echo %YELLOW%[WARNING]%ESC% Could not create desktop shortcut.
)

REM Create Start Menu entry
echo %BLUE%[INFO]%ESC% Creating Start Menu entry...
set START_MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Audion
set START_MENU_SHORTCUT=%START_MENU_DIR%\Audion Music Player.lnk

mkdir "%START_MENU_DIR%" >nul 2>&1

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_SHORTCUT%'); $Shortcut.TargetPath = '%TARGET_PATH%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%\dist\audion'; if (Test-Path '%ICON_PATH%') { $Shortcut.IconLocation = '%ICON_PATH%' }; $Shortcut.Description = 'Audion Music Player - A modern music player'; $Shortcut.Save()}"

if exist "%START_MENU_SHORTCUT%" (
    echo %GREEN%[SUCCESS]%ESC% Start Menu entry created.
) else (
    echo %YELLOW%[WARNING]%ESC% Could not create Start Menu entry.
)

REM Register file associations (optional)
echo.
choice /M "Set up file associations for audio files"
if !errorlevel! equ 1 (
    echo %BLUE%[INFO]%ESC% Setting up file associations...
    
    REM Create registry entries for file associations
    reg add "HKEY_CURRENT_USER\Software\Classes\.mp3" /ve /d "Audion.AudioFile" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\.wav" /ve /d "Audion.AudioFile" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\.ogg" /ve /d "Audion.AudioFile" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\.flac" /ve /d "Audion.AudioFile" /f >nul 2>&1
    
    reg add "HKEY_CURRENT_USER\Software\Classes\Audion.AudioFile" /ve /d "Audio File" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\Audion.AudioFile\DefaultIcon" /ve /d "\"%ICON_PATH%\",0" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\Audion.AudioFile\shell\open\command" /ve /d "\"%TARGET_PATH%\" \"%%1\"" /f >nul 2>&1
    reg add "HKEY_CURRENT_USER\Software\Classes\Audion.AudioFile\shell\play\command" /ve /d "\"%TARGET_PATH%\" \"%%1\"" /f >nul 2>&1
    
    echo %GREEN%[SUCCESS]%ESC% File associations configured.
)

REM Create uninstaller
echo %BLUE%[INFO]%ESC% Creating uninstaller...
(
echo @echo off
echo echo Uninstalling Audion Music Player...
echo.
echo REM Remove desktop shortcut
echo del "%%USERPROFILE%%\Desktop\Audion Music Player.lnk" ^>nul 2^>^&1
echo.
echo REM Remove Start Menu entry
echo rmdir /s /q "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Audion" ^>nul 2^>^&1
echo.
echo REM Remove file associations
echo reg delete "HKEY_CURRENT_USER\Software\Classes\.mp3" /f ^>nul 2^>^&1
echo reg delete "HKEY_CURRENT_USER\Software\Classes\.wav" /f ^>nul 2^>^&1
echo reg delete "HKEY_CURRENT_USER\Software\Classes\.ogg" /f ^>nul 2^>^&1
echo reg delete "HKEY_CURRENT_USER\Software\Classes\.flac" /f ^>nul 2^>^&1
echo reg delete "HKEY_CURRENT_USER\Software\Classes\Audion.AudioFile" /f ^>nul 2^>^&1
echo.
echo REM Remove installation directory
echo echo Removing installation directory...
echo cd /d "%%USERPROFILE%%"
echo rmdir /s /q "%INSTALL_DIR%"
echo.
echo echo Audion Music Player has been uninstalled.
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

echo %GREEN%[SUCCESS]%ESC% Installation completed successfully!
echo.
echo %BLUE%[INFO]%ESC% You can now:
echo %BLUE%[INFO]%ESC% • Launch Audion from your desktop shortcut
echo %BLUE%[INFO]%ESC% • Find Audion in your Start Menu
echo %BLUE%[INFO]%ESC% • Double-click audio files to open with Audion (if file associations were set up)
echo.
echo %BLUE%[INFO]%ESC% Installation directory: %INSTALL_DIR%
echo %BLUE%[INFO]%ESC% To uninstall, run: %INSTALL_DIR%\uninstall.bat
echo.
echo %GREEN%[SUCCESS]%ESC% Enjoy your music! 🎵
echo.
pause