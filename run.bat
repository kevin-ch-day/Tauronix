@echo off
:: Improved Batch Script to Start the Python Application

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

:: Check if pip needs to be updated
echo Checking if pip is up to date...
python -m pip install --upgrade pip >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo pip is up to date or has been updated.
) ELSE (
    echo Failed to update pip. Please check for issues manually.
    pause
    exit /b
)

:: Check if required packages are installed
echo Checking required Python packages...

pip show pandas >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing pandas...
    pip install pandas
)

pip show requests >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing requests...
    pip install requests
)

pip show mysql-connector-python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing mysql-connector-python...
    pip install mysql-connector-python
)

pip show tabulate >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Installing tabulate...
    pip install tabulate
)

:: Start the application
echo Starting the application...
python main.py

:: Check if the application ran successfully
IF %ERRORLEVEL% NEQ 0 (
    echo Application failed to start. Please check for errors.
) ELSE (
    echo Application started successfully.
)

pause
