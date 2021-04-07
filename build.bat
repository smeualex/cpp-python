@echo off
SET mypath=%~dp0

call :log "============================================================================="
call :log "==== " %CD%

SET ARCH=Win32
SET CONFIG=Release
SET GENERATOR="Visual Studio 16 2019"
SET BUILD_DIR=build\%ARCH%\%CONFIG%

call :log " >> Building project - %CONFIG% with %GENERATOR%" 

call :log " >> CMake Configure..." 
cmake -S . -B %BUILD_DIR% -G %GENERATOR% -A %ARCH% -DCMAKE_BUILD_TYPE=%CONFIG%
call :ExitIfError %ERRORLEVEL% "cmake - config. error"

call :log " >> CMake Build..." 
cmake --build %BUILD_DIR% --config %CONFIG%
call :ExitIfError %ERRORLEVEL% "cmake - build error"

call :log " >> DONE" 
call :log "============================================================================="

:log
    ECHO [%DATE% %TIME%] %*
    goto :eof

:ExitIfError
    set errCode=%~1
    set exitMsg=%~2
    if "%errCode%" NEQ "0" (
        call :log %exitMsg% %errCode%
        goto :endWithErrors
    )
    goto :eof

:endWithErrors
    call :log "Exiting with error = %ERRORLEVEL%"
    cd %mypath%

:end