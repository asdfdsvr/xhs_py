# 生产环境部署指南

## 方式一：Linux 服务器（推荐）

### 1. 上传项目到服务器

```bash
# 用 scp 或 git clone 将项目传到服务器
scp -r Spider_XHS-master user@your-server:/home/www/spider_xhs
```

### 2. 安装依赖

```bash
cd /home/www/spider_xhs

# Python 依赖
pip install -r requirements.txt

# Node.js 依赖
npm install
```

### 3. 使用 systemd 管理服务（推荐）

创建服务文件：

```bash
sudo vim /etc/systemd/system/spider-xhs.service
```

写入以下内容：

```ini
[Unit]
Description=小红书笔记抓取工具
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/www/spider_xhs
ExecStart=/usr/local/bin/waitress-serve --host=0.0.0.0 --port=5000 app:app
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable spider-xhs
sudo systemctl start spider-xhs
sudo systemctl status spider-xhs
```

### 4. 配置 Nginx 反向代理 + 你的域名

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    client_max_body_size 10m;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 检查配置并重载
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 配置 SSL（HTTPS）

```bash
# 使用 certbot 自动申请证书
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 方式二：Docker 部署

### 1. 构建镜像

```bash
docker build -t spider-xhs -f Dockerfile.prod .
```

### 2. 运行容器

```bash
docker run -d \
  --name spider-xhs \
  --restart always \
  -p 5000:5000 \
  spider-xhs
```

### 3. 配合 Nginx 反向代理 + 域名

同上 Nginx 配置。

---

## 方式三：Windows 服务器

```bash
# 安装依赖
pip install -r requirements.txt
npm install

# 使用 waitress 启动（生产模式，不带 debug）
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

然后用 IIS 或 Nginx 做反向代理绑定域名。

---

## 安全建议

1. **限制使用频率**：可在 `app.py` 添加速率限制
2. **添加访问密码**：可在前端加一个简单的密码验证层
3. **使用 HTTPS**：保护 Cookie 传输过程
4. **日志监控**：定期检查 `journalctl -u spider-xhs` 日志

## 验证部署

浏览器访问 `https://你的域名`，页面正常显示即可使用。
