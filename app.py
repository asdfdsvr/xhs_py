import json
import io
import os
import secrets
import tempfile
from flask import Flask, render_template, request, jsonify, send_file, session
from spider.spider import Data_Spider
from xhs_utils.data_util import save_to_xlsx
from xhs_utils.common_util import init

# ── 云平台环境适配（Vercel / Render 等） ──────────────
_IS_VERCEL = os.environ.get('VERCEL', '') == '1'
_IS_RENDER = os.environ.get('RENDER', '') == '1'

if _IS_VERCEL or _IS_RENDER:
    # 1) 把 node_bin 加入 PATH，确保 execjs 能找到 Node.js
    _node_bin = os.path.join(os.path.dirname(__file__), 'node_bin', 'bin')
    if os.path.isdir(_node_bin):
        os.environ['PATH'] = _node_bin + os.pathsep + os.environ.get('PATH', '')
    elif os.path.isdir(os.path.join(os.path.dirname(__file__), 'node_bin')):
        os.environ['PATH'] = os.path.join(os.path.dirname(__file__), 'node_bin') + os.pathsep + os.environ.get('PATH', '')

    # 2) tempfile 使用 /tmp（Vercel 只允许写 /tmp）
    tempfile.tempdir = '/tmp'

app = Flask(__name__)
# 生产环境用固定 SECRET_KEY（通过 Vercel 环境变量设置），开发环境自动生成
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# 内存存储：session_id -> { notes: [...], cookies: str }
_scrape_store = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    cookies_str = request.form.get('cookies', '').strip()
    note_urls_raw = request.form.get('note_urls', '').strip()

    if not cookies_str or not note_urls_raw:
        return jsonify({'success': False, 'error': 'Cookie 和笔记链接都不能为空'})

    cookies_str = cookies_str.strip("'\"")
    note_urls = [u.strip() for u in note_urls_raw.split('\n') if u.strip()]

    spider = Data_Spider()
    results = []
    total = len(note_urls)

    for idx, url in enumerate(note_urls):
        success, msg, note_info = spider.spider_note(url, cookies_str)
        if success and note_info:
            results.append({
                'success': True,
                'index': idx + 1,
                'total': total,
                'data': {
                    'title': note_info['title'],
                    'desc': note_info['desc'],
                    'note_type': note_info['note_type'],
                    'liked_count': note_info['liked_count'],
                    'collected_count': note_info['collected_count'],
                    'comment_count': note_info['comment_count'],
                    'share_count': note_info['share_count'],
                    'nickname': note_info['nickname'],
                    'tags': note_info['tags'],
                    'upload_time': note_info['upload_time'],
                    'ip_location': note_info['ip_location'],
                    'image_list': note_info['image_list'],
                    'note_url': note_info['note_url'],
                    'note_id': note_info['note_id'],
                    'user_id': note_info['user_id'],
                    'home_url': note_info['home_url'],
                    'avatar': note_info['avatar'],
                }
            })
        else:
            results.append({
                'success': False,
                'index': idx + 1,
                'total': total,
                'url': url,
                'error': str(msg),
            })

    # 存入内存，供下载 Excel 使用
    if '_session_id' not in session:
        session['_session_id'] = secrets.token_hex(16)
    session_id = session['_session_id']
    if session_id not in _scrape_store:
        _scrape_store[session_id] = []
    _scrape_store[session_id].extend([r['data'] for r in results if r.get('success')])
    _scrape_store[session_id] = _scrape_store[session_id][-500:]  # 最多保留500条

    return jsonify({'success': True, 'results': results, 'total_count': len(results)})


@app.route('/download_excel')
def download_excel():
    if '_session_id' not in session:
        return jsonify({'success': False, 'error': '没有可下载的数据，请先抓取笔记'})
    session_id = session['_session_id']
    notes = _scrape_store.get(session_id, [])

    if not notes:
        return jsonify({'success': False, 'error': '没有可下载的数据，请先抓取笔记'})

    # 保存到内存字节流
    buf = io.BytesIO()
    file_path = 'notes.xlsx'
    # save_to_xlsx 需要文件路径，我们使用临时文件
    import tempfile
    import os
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    try:
        save_to_xlsx(notes, tmp.name)
        tmp.close()
        with open(tmp.name, 'rb') as f:
            buf.write(f.read())
    finally:
        os.unlink(tmp.name)

    buf.seek(0)
    return send_file(
        buf,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='小红书笔记数据.xlsx'
    )


@app.route('/clear_data', methods=['POST'])
def clear_data():
    if '_session_id' in session:
        session_id = session['_session_id']
        _scrape_store.pop(session_id, None)
    return jsonify({'success': True})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    print(f"🚀 启动服务: http://0.0.0.0:{port}")
    print(f"   局域网访问: http://{__import__('socket').gethostbyname(__import__('socket').gethostname())}:{port}")
    print(f"   生产模式请使用: waitress-serve --port={port} app:app")
    app.run(debug=debug, host='0.0.0.0', port=port)
