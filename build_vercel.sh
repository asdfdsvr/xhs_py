#!/bin/bash
# Vercel 构建脚本 —— 下载 Node.js 供 Python execjs 使用
set -e

echo "🚀 Vercel build: 安装 Node.js..."

mkdir -p node_bin

NODE_VERSION="20.18.0"
NODE_URL="https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz"

echo "下载 Node.js ${NODE_VERSION}..."
curl -sL "$NODE_URL" | tar xJ -C node_bin --strip-components=1 2>/dev/null || {
  NODE_URL="https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz"
  curl -sL "$NODE_URL" | tar xz -C node_bin --strip-components=1
}

if [ -f node_bin/bin/node ]; then
  echo "✅ Node.js 安装成功: $(node_bin/bin/node -v)"
  chmod +x node_bin/bin/node node_bin/bin/npm 2>/dev/null || true
else
  echo "⚠️  下载失败，尝试用系统 node..."
  which node && cp "$(which node)" node_bin/ 2>/dev/null || echo "⚠️  无系统 node"
fi

echo "✅ Vercel build 完成"
