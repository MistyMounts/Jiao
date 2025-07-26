from googleapiclient.discovery import build
import subprocess
import os
import time
import httplib2
import signal
import sys

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33210'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33210'

# 从环境变量获取API Key，如果没有则使用默认值
api_key = os.getenv('YOUTUBE_API_KEY', 'AIzaSyD360lA1BOCoGg3KDrWgZhbyjC0jUdH1PU')

# 创建带超时的HTTP客户端
http = httplib2.Http(timeout=30)  # 30秒超时
youtube = build('youtube', 'v3', developerKey=api_key, http=http)

# 全局变量用于跟踪下载进程
current_process = None

def signal_handler(signum, frame):
    """处理Ctrl+C信号"""
    print("\n收到中断信号，正在停止程序...")
    if current_process:
        try:
            current_process.terminate()
            print("已终止当前下载进程")
        except:
            pass
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

def search_videos(query, max_results=20):
    try:
        print(f"正在搜索: {query}")
        request = youtube.search().list(
            q=query,
            part='id,snippet',
            type='video',
            maxResults=max_results
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        print(f"找到 {len(video_ids)} 个视频")
        return video_ids
    except Exception as e:
        print(f"搜索失败 '{query}': {e}")
        return []

if __name__ == "__main__":
    try:
        # 1. 搜索关键词 - 多模态异常行为识别项目素材收集
        keywords = [
            # 婴幼儿哭闹相关
            "婴儿哭闹", "baby crying",
            "幼儿哭闹", "toddler crying", 
            "婴儿大哭", "baby screaming",
            "幼儿情绪失控", "toddler tantrum",
            
            # 照护人员离开/疏忽
            "照护人员离开", "caregiver leaving",
            "保姆离开房间", "nanny leaving room",
            "照护人员疏忽", "caregiver neglect",
            "无人看护婴儿", "unattended baby",
            
            # 陌生人群检测
            "陌生人接触婴儿", "stranger touching baby",
            "陌生人抱婴儿", "stranger holding baby",
            "陌生人进入房间", "stranger entering room",
            "可疑人员", "suspicious person",
            
            # 拥挤检测
            "人群拥挤", "crowded room",
            "多人聚集", "people gathering",
            "房间拥挤", "room overcrowding",
            "人员密集", "dense crowd",
            
            # 危险区域靠近
            "婴儿靠近危险", "baby near danger",
            "幼儿爬向危险", "toddler crawling to danger",
            "靠近楼梯", "near stairs",
            "靠近窗户", "near window",
            "靠近电器", "near electrical appliances",
            
            # 跌倒未爬起
            "婴儿跌倒", "baby falling",
            "幼儿摔倒", "toddler falling",
            "跌倒不起", "falling not getting up",
            "婴儿摔倒", "baby tumble",
            
            # 趴窝式睡眠
            "婴儿趴睡", "baby sleeping on stomach",
            "趴着睡觉", "sleeping face down",
            "婴儿睡眠姿势", "baby sleep position",
            "趴窝睡眠", "prone sleeping",
            
            # 照护人员辱骂
            "照护人员骂人", "caregiver yelling",
            "保姆发脾气", "nanny angry",
            "照护人员情绪失控", "caregiver emotional outburst",
            "照护人员暴力", "caregiver violence",
            
            # 婴幼儿互相打闹
            "婴儿打架", "babies fighting",
            "幼儿打闹", "toddlers fighting",
            "儿童冲突", "children conflict",
            "婴儿推搡", "baby pushing",
            
            # 照护人员剧烈摇晃
            "摇晃婴儿", "shaking baby",
            "剧烈摇晃", "violent shaking",
            "摇晃综合征", "shaken baby syndrome",
            "不当摇晃", "improper shaking",
            
            # 其他异常行为
            "照护人员打骂", "caregiver hitting",
            "婴儿被虐待", "baby abuse",
            "照护不当", "improper care",
            "婴儿安全", "baby safety"
        ]
        all_video_ids = set()
        
        for kw in keywords:
            print(f"处理关键词: {kw}")
            ids = search_videos(kw, 3)  # 每个关键词取前3个结果
            all_video_ids.update(ids)
            time.sleep(1)  # 添加延迟，避免请求过快
        
        if not all_video_ids:
            print("没有找到任何视频，请检查网络连接或API Key")
            exit(1)
        
        # 2. 保存视频ID到文件
        with open("video_ids.txt", "w", encoding="utf-8") as f:
            for vid in all_video_ids:
                f.write(vid + "\n")
        print(f"共获取{len(all_video_ids)}个视频ID，已保存到video_ids.txt")

        # 3. 批量下载视频
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")
        os.makedirs(save_dir, exist_ok=True)
        print(f"视频将保存到: {save_dir}")
        
        # 创建分类目录
        categories = {
            "婴幼儿哭闹": ["婴儿哭闹", "baby crying", "幼儿哭闹", "toddler crying", "婴儿大哭", "baby screaming", "幼儿情绪失控", "toddler tantrum"],
            "照护人员离开": ["照护人员离开", "caregiver leaving", "保姆离开房间", "nanny leaving room", "照护人员疏忽", "caregiver neglect", "无人看护婴儿", "unattended baby"],
            "陌生人群检测": ["陌生人接触婴儿", "stranger touching baby", "陌生人抱婴儿", "stranger holding baby", "陌生人进入房间", "stranger entering room", "可疑人员", "suspicious person"],
            "拥挤检测": ["人群拥挤", "crowded room", "多人聚集", "people gathering", "房间拥挤", "room overcrowding", "人员密集", "dense crowd"],
            "危险区域靠近": ["婴儿靠近危险", "baby near danger", "幼儿爬向危险", "toddler crawling to danger", "靠近楼梯", "near stairs", "靠近窗户", "near window", "靠近电器", "near electrical appliances"],
            "跌倒未爬起": ["婴儿跌倒", "baby falling", "幼儿摔倒", "toddler falling", "跌倒不起", "falling not getting up", "婴儿摔倒", "baby tumble"],
            "趴窝式睡眠": ["婴儿趴睡", "baby sleeping on stomach", "趴着睡觉", "sleeping face down", "婴儿睡眠姿势", "baby sleep position", "趴窝睡眠", "prone sleeping"],
            "照护人员辱骂": ["照护人员骂人", "caregiver yelling", "保姆发脾气", "nanny angry", "照护人员情绪失控", "caregiver emotional outburst", "照护人员暴力", "caregiver violence"],
            "婴幼儿打闹": ["婴儿打架", "babies fighting", "幼儿打闹", "toddlers fighting", "儿童冲突", "children conflict", "婴儿推搡", "baby pushing"],
            "剧烈摇晃": ["摇晃婴儿", "shaking baby", "剧烈摇晃", "violent shaking", "摇晃综合征", "shaken baby syndrome", "不当摇晃", "improper shaking"],
            "其他异常行为": ["照护人员打骂", "caregiver hitting", "婴儿被虐待", "baby abuse", "照护不当", "improper care", "婴儿安全", "baby safety"]
        }
        
        # 为每个类别创建目录
        for category in categories.keys():
            category_dir = os.path.join(save_dir, category)
            os.makedirs(category_dir, exist_ok=True)
        
        # 记录视频信息
        video_info_list = []
        
        with open("video_ids.txt", "r", encoding="utf-8") as f:
            for line in f:
                video_id = line.strip()
                if video_id:
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"正在下载: {url}")
                    
                    # 确定视频类别（这里简化处理，实际应该根据搜索关键词确定）
                    category = "其他异常行为"  # 默认类别
                    
                    try:
                        # 使用yt-dlp下载到对应类别文件夹
                        category_dir = os.path.join(save_dir, category)
                        current_process = subprocess.Popen([
                            "yt-dlp", 
                            "-P", category_dir, 
                            "--proxy", "http://127.0.0.1:33210",
                            "--write-info-json",  # 保存视频信息
                            url
                        ])
                        current_process.wait(timeout=300)  # 5分钟超时
                        print(f"下载成功: {video_id} -> {category}")
                        
                        # 记录视频信息
                        video_info_list.append({
                            "video_id": video_id,
                            "url": url,
                            "category": category,
                            "status": "success"
                        })
                        
                        current_process = None
                    except subprocess.TimeoutExpired:
                        print(f"下载超时: {url}")
                        if current_process:
                            current_process.terminate()
                            current_process = None
                        video_info_list.append({
                            "video_id": video_id,
                            "url": url,
                            "category": category,
                            "status": "timeout"
                        })
                    except Exception as e:
                        print(f"下载失败: {url}, 错误: {e}")
                        if current_process:
                            current_process.terminate()
                            current_process = None
                        video_info_list.append({
                            "video_id": video_id,
                            "url": url,
                            "category": category,
                            "status": "failed",
                            "error": str(e)
                        })
        
        # 保存视频信息到JSON文件
        import json
        with open("video_download_info.json", "w", encoding="utf-8") as f:
            json.dump(video_info_list, f, ensure_ascii=False, indent=2)
        print("视频下载信息已保存到 video_download_info.json")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        if current_process:
            current_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"程序出错: {e}")
        if current_process:
            current_process.terminate()
        sys.exit(1)