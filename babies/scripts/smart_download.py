from googleapiclient.discovery import build
import subprocess
import os
import time
import httplib2
import signal
import sys
import json
from datetime import datetime

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33210'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33210'

# 从环境变量获取API Key
api_key = os.getenv('YOUTUBE_API_KEY', 'AIzaSyD360lA1BOCoGg3KDrWgZhbyjC0jUdH1PU')

# 创建带超时的HTTP客户端
http = httplib2.Http(timeout=30)
youtube = build('youtube', 'v3', developerKey=api_key, http=http)

# 全局变量
current_process = None
download_log = []

def signal_handler(signum, frame):
    """处理Ctrl+C信号"""
    print("\n收到中断信号，正在停止程序...")
    if current_process:
        try:
            current_process.terminate()
            print("已终止当前下载进程")
        except:
            pass
    save_download_log()
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

def search_videos(query, max_results=5, category=""):
    """搜索视频并返回详细信息"""
    try:
        print(f"正在搜索: {query} (类别: {category})")
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            type='video',
            maxResults=max_results,
            order='relevance'  # 按相关性排序
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video_info = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'channel_title': item['snippet']['channelTitle'],
                'search_query': query,
                'category': category,
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video_info)
        
        print(f"找到 {len(videos)} 个视频")
        return videos
    except Exception as e:
        print(f"搜索失败 '{query}': {e}")
        return []

def get_video_duration(video_id):
    """获取视频时长"""
    try:
        request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        response = request.execute()
        if response['items']:
            duration = response['items'][0]['contentDetails']['duration']
            # 解析ISO 8601格式的时长
            import re
            match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
            hours = int(match.group(1)[:-1]) if match.group(1) else 0
            minutes = int(match.group(2)[:-1]) if match.group(2) else 0
            seconds = int(match.group(3)[:-1]) if match.group(3) else 0
            return hours * 3600 + minutes * 60 + seconds
    except:
        pass
    return 0

def filter_videos(videos, min_duration=60, max_duration=1800):
    """过滤视频（时长、标题相关性等）"""
    filtered = []
    for video in videos:
        duration = get_video_duration(video['video_id'])
        video['duration'] = duration
        
        # 时长过滤
        if min_duration <= duration <= max_duration:
            # 标题相关性检查（简单关键词匹配）
            title_lower = video['title'].lower()
            query_lower = video['search_query'].lower()
            
            # 检查标题是否包含搜索关键词的相关词汇
            relevant_keywords = query_lower.split()
            relevance_score = sum(1 for kw in relevant_keywords if kw in title_lower)
            
            if relevance_score > 0:  # 至少包含一个相关词汇
                video['relevance_score'] = relevance_score
                filtered.append(video)
    
    return filtered

def download_video(video_info, save_dir):
    """下载单个视频"""
    global current_process
    
    video_id = video_info['video_id']
    url = video_info['url']
    category = video_info['category']
    
    # 创建分类目录
    category_dir = os.path.join(save_dir, category)
    os.makedirs(category_dir, exist_ok=True)
    
    print(f"正在下载: {video_info['title']}")
    print(f"类别: {category}, 时长: {video_info['duration']}秒")
    
    try:
        # 使用yt-dlp下载，添加更多参数
        current_process = subprocess.Popen([
            "yt-dlp",
            "-P", category_dir,
            "--proxy", "http://127.0.0.1:33210",
            "--format", "best[height<=720]",  # 限制分辨率
            "--write-info-json",  # 保存视频信息
            "--write-description",  # 保存描述
            url
        ])
        
        current_process.wait(timeout=600)  # 10分钟超时
        
        # 记录下载成功
        download_log.append({
            'video_id': video_id,
            'title': video_info['title'],
            'category': category,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'search_query': video_info['search_query']
        })
        
        print(f"下载成功: {video_id}")
        current_process = None
        return True
        
    except subprocess.TimeoutExpired:
        print(f"下载超时: {url}")
        if current_process:
            current_process.terminate()
            current_process = None
    except Exception as e:
        print(f"下载失败: {url}, 错误: {e}")
        if current_process:
            current_process.terminate()
            current_process = None
    
    # 记录下载失败
    download_log.append({
        'video_id': video_id,
        'title': video_info['title'],
        'category': category,
        'status': 'failed',
        'timestamp': datetime.now().isoformat(),
        'search_query': video_info['search_query']
    })
    
    return False

def save_download_log():
    """保存下载日志"""
    with open("download_log.json", "w", encoding="utf-8") as f:
        json.dump(download_log, f, ensure_ascii=False, indent=2)
    print(f"下载日志已保存到 download_log.json")

def main():
    # 定义关键词分类
    keyword_categories = {
        "婴幼儿哭闹": [
            "婴儿哭闹", "baby crying",
            "幼儿哭闹", "toddler crying", 
            "婴儿大哭", "baby screaming",
            "幼儿情绪失控", "toddler tantrum"
        ],
        "照护人员离开": [
            "照护人员离开", "caregiver leaving",
            "保姆离开房间", "nanny leaving room",
            "照护人员疏忽", "caregiver neglect",
            "无人看护婴儿", "unattended baby"
        ],
        "陌生人群检测": [
            "陌生人接触婴儿", "stranger touching baby",
            "陌生人抱婴儿", "stranger holding baby",
            "陌生人进入房间", "stranger entering room",
            "可疑人员", "suspicious person"
        ],
        "拥挤检测": [
            "人群拥挤", "crowded room",
            "多人聚集", "people gathering",
            "房间拥挤", "room overcrowding",
            "人员密集", "dense crowd"
        ],
        "危险区域靠近": [
            "婴儿靠近危险", "baby near danger",
            "幼儿爬向危险", "toddler crawling to danger",
            "靠近楼梯", "near stairs",
            "靠近窗户", "near window"
        ],
        "跌倒未爬起": [
            "婴儿跌倒", "baby falling",
            "幼儿摔倒", "toddler falling",
            "跌倒不起", "falling not getting up",
            "婴儿摔倒", "baby tumble"
        ],
        "趴窝式睡眠": [
            "婴儿趴睡", "baby sleeping on stomach",
            "趴着睡觉", "sleeping face down",
            "婴儿睡眠姿势", "baby sleep position",
            "趴窝睡眠", "prone sleeping"
        ],
        "照护人员辱骂": [
            "照护人员骂人", "caregiver yelling",
            "保姆发脾气", "nanny angry",
            "照护人员情绪失控", "caregiver emotional outburst",
            "照护人员暴力", "caregiver violence"
        ],
        "婴幼儿打闹": [
            "婴儿打架", "babies fighting",
            "幼儿打闹", "toddlers fighting",
            "儿童冲突", "children conflict",
            "婴儿推搡", "baby pushing"
        ],
        "剧烈摇晃": [
            "摇晃婴儿", "shaking baby",
            "剧烈摇晃", "violent shaking",
            "摇晃综合征", "shaken baby syndrome",
            "不当摇晃", "improper shaking"
        ]
    }
    
    # 创建保存目录
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")
    os.makedirs(base_dir, exist_ok=True)
    
    all_videos = []
    
    # 按类别搜索
    for category, keywords in keyword_categories.items():
        print(f"\n=== 开始搜索类别: {category} ===")
        category_videos = []
        
        for keyword in keywords:
            videos = search_videos(keyword, max_results=3, category=category)
            category_videos.extend(videos)
            time.sleep(2)  # 避免API限制
        
        # 过滤视频
        filtered_videos = filter_videos(category_videos)
        print(f"类别 {category} 过滤后剩余 {len(filtered_videos)} 个视频")
        
        # 按相关性排序
        filtered_videos.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # 选择前5个最相关的视频
        selected_videos = filtered_videos[:5]
        all_videos.extend(selected_videos)
        
        print(f"类别 {category} 最终选择 {len(selected_videos)} 个视频")
    
    # 保存视频信息
    with open("selected_videos.json", "w", encoding="utf-8") as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=2)
    
    print(f"\n总共选择了 {len(all_videos)} 个视频")
    print("开始下载...")
    
    # 下载视频
    success_count = 0
    for i, video in enumerate(all_videos, 1):
        print(f"\n进度: {i}/{len(all_videos)}")
        if download_video(video, base_dir):
            success_count += 1
        time.sleep(1)
    
    print(f"\n下载完成！成功下载 {success_count}/{len(all_videos)} 个视频")
    save_download_log()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        if current_process:
            current_process.terminate()
        save_download_log()
        sys.exit(0)
    except Exception as e:
        print(f"程序出错: {e}")
        if current_process:
            current_process.terminate()
        save_download_log()
        sys.exit(1) 