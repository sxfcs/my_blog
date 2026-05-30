@echo off
echo ========================================
echo 博客部署脚本
echo ========================================
echo.

echo [1/4] 打包项目代码...
powershell -Command "Compress-Archive -Path '.' -DestinationPath 'deploy.zip' -Force -Exclude 'venv','.git','db.sqlite3','deploy.zip','.github'"
echo 打包完成！

echo.
echo [2/4] 请上传 deploy.zip 到 PythonAnywhere
echo.
echo 操作步骤：
echo 1. 登录 https://www.pythonanywhere.com
echo 2. 点击 Files 选项卡
echo 3. 上传 deploy.zip 到 /home/lzysxfcs/
echo 4. 按任意键继续...
pause > nul

echo.
echo [3/4] 连接到 PythonAnywhere Bash...
echo 请在打开的 Bash 控制台中执行以下命令：
echo.
echo cd ~/my_blog
echo unzip -o ../deploy.zip
echo rm ../deploy.zip
echo python3.13 manage.py migrate --noinput
echo python3.13 manage.py collectstatic --noinput
echo touch /var/www/lzysxfcs_pythonanywhere_com_wsgi.py
echo.
echo 按任意键打开 PythonAnywhere 网站...
pause > nul

start https://www.pythonanywhere.com/user/lzysxfcs/consoles/

echo.
echo [4/4] 部署完成后，请点击 Web 选项卡的 Reload 按钮
echo.
echo 按任意键退出...
pause > nul