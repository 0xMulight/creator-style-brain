@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PYCMD=py -3") else (set "PYCMD=python")
:menu
cls
echo Creator Style Brain - 创作风格脑
echo.
echo 1. 分析 examples\samples 下的作品
echo 2. 检查 examples\draft.txt 草稿
echo 3. 输出可复制的Bot提示词
echo 4. 运行测试
echo 0. 退出
set /p op=选择：
if "%op%"=="1" %PYCMD% -m creator_style_brain analyze --input examples/samples --output reports
if "%op%"=="2" %PYCMD% -m creator_style_brain check --profile reports/style-profile.json --draft examples/draft.txt
if "%op%"=="3" %PYCMD% -m creator_style_brain prompt --profile reports/style-profile.json
if "%op%"=="4" %PYCMD% -m unittest discover -s tests -v
if "%op%"=="0" exit /b 0
echo.
pause
goto menu
