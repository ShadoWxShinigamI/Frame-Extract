@echo off

set ENV_NAME=Frame-Extract
set REQUIREMENTS=requirements.txt
set PYTHON_FILE=Frames.py

call conda activate %ENV_NAME%
if %errorlevel% neq 0 (
    echo Creating Conda environment: %ENV_NAME%
    call conda create --name %ENV_NAME% python==3.10.10 --yes
    call conda activate %ENV_NAME%
    echo Installing requirements from: %REQUIREMENTS%
    call conda install --file %REQUIREMENTS% --yes
) else (
    echo Conda environment %ENV_NAME% already exists.
)

echo Running Python file: %PYTHON_FILE%
python %PYTHON_FILE%
