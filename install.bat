@echo off
chcp 65001 > nul

REM Активация виртуального окружения
call .\venv\Scripts\activate.bat

REM Проверка наличия файла requirements.txt
if not exist requirements.txt (
    echo Файл requirements.txt не найден.
    pause
    exit /b
)

REM Установка зависимостей
pip install -r requirements.txt

REM Запуск python файла в новом окне командной строки
start "Заголовок окна" python имя_файла.py

pause