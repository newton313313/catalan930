@echo off
REM ---------------------------------------------------------------------------
REM render_all.bat
REM One-click rendering of the videos into codes\renders\ (wraps render_all.py).
REM
REM   Double-click it            -> a small menu (everything / demos / scenes / 480p)
REM   render_all.bat <args>      -> passes the args to render_all.py, no menu,
REM                                 e.g.  render_all.bat --fulton5 -l
REM
REM Run install_windows.bat first. If manimgl is not on PATH (double-click from
REM Explorer), this script tries to activate Anaconda / Miniconda by itself.
REM Keep this file ASCII-only (cmd reads .bat files as cp950).
REM ---------------------------------------------------------------------------
setlocal
cd /d "%~dp0"

where manimgl >nul 2>nul || call :activate_conda
where manimgl >nul 2>nul || goto :nomanim

if not "%~1"=="" (
    python render_all.py %*
    goto :done
)

echo.
echo ============================================================
echo   One-click render  (output: codes\renders\)
echo ============================================================
echo   1. Everything: all 123 scenes + all 15 demos, 1080p
echo   2. Demos only: the 15 continuous-play videos, 1080p
echo   3. Scenes only: the 123 single-scene videos, 1080p
echo   4. Quick check: everything at 480p (fast, low quality)
echo   Q. Quit
echo.
echo   1080p takes several hours; 480p is much faster.
echo   Existing videos with the same name are overwritten.
echo.
set "CHOICE=none"
set /p "CHOICE=Choose 1-4 or Q: "
set "CHOICE=%CHOICE: =%"

set DEMOS=--intro-demo --full --complete --mit-demo --mit-complete --fulton-demo --fulton2-demo --fulton3-demo --fulton4-demo --fulton5-demo --fulton6-demo --fulton7-demo --raney-demo --raney-paper-demo --raney-ladder-demo

if /i "%CHOICE%"=="Q" goto :eof
if "%CHOICE%"=="1" python render_all.py --hd %DEMOS% & goto :done
if "%CHOICE%"=="2" python render_all.py --hd %DEMOS% --demos-only & goto :done
if "%CHOICE%"=="3" python render_all.py --hd & goto :done
if "%CHOICE%"=="4" python render_all.py -l %DEMOS% & goto :done
echo Unknown choice "%CHOICE%". Nothing was rendered.
pause
exit /b 1

:activate_conda
for %%D in ("%USERPROFILE%\anaconda3" "%USERPROFILE%\miniconda3" "%ProgramData%\anaconda3" "%ProgramData%\miniconda3" "%LOCALAPPDATA%\anaconda3" "%LOCALAPPDATA%\miniconda3") do (
    if exist "%%~D\Scripts\activate.bat" (
        call "%%~D\Scripts\activate.bat" "%%~D"
        goto :eof
    )
)
goto :eof

:nomanim
echo.
echo manimgl was not found.
echo Run install_windows.bat first, or start this file from an "Anaconda Prompt".
pause
exit /b 1

:done
echo.
echo Finished. Videos are in %~dp0renders
pause
