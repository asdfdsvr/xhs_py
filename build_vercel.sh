#!/bin/bash
# Render 构建脚本 — 安装 Python 和 npm 依赖
set -e

echo "📦 检查系统 Node.js..."
which node && echo "✅ 系统 Node.js: $(node -v)" || echo "⚠️ 无系统 Node.js"
which npm && echo "✅ 系统 npm: $(npm -v)" || echo "⚠️ 无系统 npm"

# 安装 npm 依赖（crypto-js 等）
echo "📦 安装 npm 依赖..."
npm install --production 2>&1 || echo "⚠️ npm install 失败"

# 验证
if [ -f "node_modules/crypto-js/index.js" ]; then
    echo "✅ crypto-js 就绪"
else
    echo "⚠️ crypto-js 未安装，手动安装..."
    npm install crypto-js 2>&1 || true
fi

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

echo "✅ 构建完成"