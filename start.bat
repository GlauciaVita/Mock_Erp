@echo off
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Verificando dependencias...
pip list | findstr fastapi

echo.
echo Iniciando aplicacao Mock ERP com FastAPI...
echo.
echo Acesse: http://localhost:8000
echo Dashboard: http://localhost:8000/dashboard  
echo API Docs: http://localhost:8000/docs
echo Para parar: Ctrl+C
echo.

python main.py
