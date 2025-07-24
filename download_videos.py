from googleapiclient.discovery import build
import subprocess
import os
# 你的API Key
api_key = 'AIzaSyD360lA1BOCoGg3KDrWgZhbyjC0jUdH1PU'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos(query, max_results=20):
    request = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    return [item['id']['videoId'] for item in response['items']]

if __name__ == "__main__":
    # 1. 搜索关键词
    keywords = [ "婴儿哭闹" ]
    all_video_ids = set()
    for kw in keywords:
        ids = search_videos(kw, 3)
        all_video_ids.update(ids)
    # 2. 保存视频ID到文件
    with open("video_ids.txt", "w", encoding="utf-8") as f:
        for vid in all_video_ids:
            f.write(vid + "\n")
    print(f"共获取{len(all_video_ids)}个视频ID，已保存到video_ids.txt")

    # 3. 批量下载视频
    # 新增：自动创建目标文件夹
    save_dir = os.path.expanduser("~/babies/babies_video")
    os.makedirs(save_dir, exist_ok=True)
    with open("video_ids.txt", "r", encoding="utf-8") as f:
        for line in f:
            video_id = line.strip()
            if video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"正在下载: {url}")
                try:
                    # 使用yt-dlp下载到指定文件夹
                    subprocess.run([
                        "yt-dlp", "-P", save_dir, url
                    ], check=True)
                except Exception as e:
                    print(f"下载失败: {url}, 错误: {e}")