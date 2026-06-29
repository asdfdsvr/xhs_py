#!/bin/bash
# Render 构建脚本 — 下载 Node.js + 安装 Python 和 npm 依赖
set -e

echo "📦 下载 Node.js..."
mkdir -p node_bin
curl -sL https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz | tar xJ -C node_bin --strip-components=1

echo "✅ Node.js: $(node_bin/bin/node -v)"
echo "✅ npm: $(node_bin/bin/npm -v)"

# 安装 npm 依赖（crypto-js）
echo "📦 安装 npm 依赖..."
node_bin/bin/npm install

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

echo "✅ 构建完成"