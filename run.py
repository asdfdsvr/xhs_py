from spider.spider import Data_Spider
from xhs_utils.common_util import init

cookies_str, base_path = init()
spider = Data_Spider()

# ⚠️ 注意：笔记链接有时效性，请替换为你自己浏览器中有效的链接
# 获取方式：打开小红书网页版 → 点开一篇笔记 → 复制浏览器地址栏完整URL
note_url = 'https://www.xiaohongshu.com/explore/6a4100ad000000000602263f?xsec_token=ABtKb8yD_0JLcsNt5LxrixtI1NZNjYH4I6J2wjjYaKRas=&xsec_source=pc_user'

success, msg, note_info = spider.spider_note(note_url, cookies_str)
if success:
    print(f"✅ 标题: {note_info['title']}")
    print(f"   内容: {note_info['desc'][:100]}...")
    print(f"   点赞: {note_info['liked_count']}")
    print(f"   评论: {note_info['comment_count']}")
    print(f"   收藏: {note_info['collected_count']}")
    print(f"   类型: {note_info['note_type']}")
    print(f"   标签: {note_info['tags']}")
    print(f"   上传时间: {note_info['upload_time']}")
    print(f"   图片数: {len(note_info['image_list'])}")
else:
    print(f"❌ 失败: {msg}")
    print("💡 提示：笔记链接可能已过期，请重新从浏览器复制一条有效链接")
