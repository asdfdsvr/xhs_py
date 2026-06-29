@echo off
REM 生产模式启动脚本 (Windows)
echo 🚀 启动小红书笔记抓取工具（生产模式）
echo.
echo 服务地址: http://0.0.0.0:5000
echo 按 Ctrl+C 停止服务
echo.

waitress-serve --host=0.0.0.0 --port=5000 app:app
