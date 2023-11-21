@echo off


chcp 65001 > nul

REM Активация виртуального окружения
call .\venv\Scripts\activate

REM Проверка наличия файла requirements.txt
if not exist requirements.txt (
    echo Файл requirements.txt не найден.
    pause
    exit /b
)

REM Проверка установки зависимостей
pip freeze | findstr /x /c:"-r requirements.txt" > nul
if %errorlevel% neq 0 (
    echo Зависимости не установлены. Установите зависимости с помощью команды "pip install -r requirements.txt".
    pause
    exit /b
)



REM Запуск python файла в новом окне командной строки
start "Заголовок окна" python main.py

pause
