:: 切换到bat当前目录
cd %~dp0
set base_dir=%~dp0
%base_dir:~0,2%
pushd %base_dir%

:: 激活conda环境并保持路径
:: call activate
python ./auto_login_ipgw.py
pause