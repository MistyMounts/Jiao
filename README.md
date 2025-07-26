# Multi-Modal Infant Abnormal Behavior Detection

A comprehensive system for detecting abnormal behaviors in infants and caregivers using multi-modal AI approaches.

## 🎯 Project Overview

This project aims to develop an intelligent monitoring system that can detect various abnormal behaviors in infant care environments, including:

- **Infant Abnormal Behaviors**: Crying, falling, fighting, abnormal sleep positions
- **Caregiver Misconduct**: Leaving, verbal abuse, violence, neglect
- **Environmental Hazards**: Stranger detection, overcrowding, dangerous area proximity

## 🏗️ Project Structure

```
Jiao/
├── babies/
│   ├── videos/           # Downloaded video datasets
│   │   ├── 婴幼儿哭闹/
│   │   ├── 照护人员离开/
│   │   ├── 陌生人群检测/
│   │   ├── 拥挤检测/
│   │   ├── 危险区域靠近/
│   │   ├── 跌倒未爬起/
│   │   ├── 趴窝式睡眠/
│   │   ├── 照护人员辱骂/
│   │   ├── 婴幼儿打闹/
│   │   ├── 剧烈摇晃/
│   │   └── 其他异常行为/
│   ├── data/             # Data files and logs
│   │   ├── video_ids.txt
│   │   ├── video_download_info.json
│   │   └── download_log.json
│   ├── docs/             # Documentation
│   │   └── search_strategy.md
│   └── scripts/          # Python scripts
│       ├── download_videos.py
│       └── smart_download.py
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+**
2. **YouTube Data API Key**
3. **VPN/Proxy setup** (for accessing YouTube in restricted regions)
4. **yt-dlp** for video downloading

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Jiao

# Install dependencies
pip install google-api-python-client httplib2

# Install yt-dlp
pip install yt-dlp

# Set up YouTube API key
export YOUTUBE_API_KEY="your_api_key_here"
```

### Usage

#### Basic Video Download
```bash
cd babies/scripts
python download_videos.py
```

#### Smart Download with Classification
```bash
cd babies/scripts
python smart_download.py
```

## 📊 Dataset Categories

The system collects videos for 10 main categories of abnormal behaviors:

| Category | Chinese Keywords | English Keywords |
|----------|------------------|------------------|
| Infant Crying | 婴儿哭闹, 幼儿哭闹 | baby crying, toddler crying |
| Caregiver Leaving | 照护人员离开, 保姆离开 | caregiver leaving, nanny leaving |
| Stranger Detection | 陌生人接触婴儿 | stranger touching baby |
| Overcrowding | 人群拥挤, 房间拥挤 | crowded room, room overcrowding |
| Danger Proximity | 婴儿靠近危险 | baby near danger |
| Falling | 婴儿跌倒, 幼儿摔倒 | baby falling, toddler falling |
| Abnormal Sleep | 婴儿趴睡, 趴着睡觉 | baby sleeping on stomach |
| Caregiver Abuse | 照护人员骂人 | caregiver yelling |
| Infant Fighting | 婴儿打架, 幼儿打闹 | babies fighting, toddlers fighting |
| Violent Shaking | 摇晃婴儿 | shaking baby |

## 🔧 Configuration

### Proxy Settings
The scripts are configured to use a local proxy at `127.0.0.1:33210`. Modify the proxy settings in the scripts if needed:

```python
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:33210'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:33210'
```

### Download Parameters
- **Video Quality**: 720p maximum (configurable)
- **Download Timeout**: 10 minutes per video
- **Results per Keyword**: 3-5 videos
- **Total Expected**: 50-150 videos

## 📈 Data Collection Strategy

### Search Strategy
- **Bilingual Keywords**: Chinese and English for broader coverage
- **Relevance Filtering**: Title-based relevance scoring
- **Duration Filtering**: 1-30 minutes videos
- **Quality Control**: HD videos preferred

### Storage Organization
- **Categorized Storage**: Videos organized by behavior type
- **Metadata Tracking**: JSON files with video information
- **Download Logs**: Comprehensive logging of download status

## 🤖 Multi-Modal Features

The collected dataset supports multi-modal analysis:

### Visual Modality
- **Behavior Recognition**: Action detection in video frames
- **Person Detection**: Counting and tracking individuals
- **Scene Analysis**: Environmental context understanding

### Audio Modality
- **Crying Detection**: Infant crying sound recognition
- **Voice Analysis**: Caregiver voice emotion detection
- **Noise Level**: Environmental noise monitoring

### Temporal Modality
- **Behavior Duration**: How long abnormal behaviors last
- **Pattern Recognition**: Recurring behavior patterns
- **Sequence Analysis**: Behavior progression over time

## 📝 Data Format

### Video Information JSON
```json
{
  "video_id": "FDZ9fbKDtoM",
  "title": "Video Title",
  "category": "婴幼儿哭闹",
  "duration": 360,
  "url": "https://www.youtube.com/watch?v=FDZ9fbKDtoM",
  "search_query": "婴儿哭闹",
  "status": "success"
}
```

## 🔒 Privacy and Ethics

- **Educational Purpose**: Videos collected for research and development
- **Public Content**: Only publicly available YouTube videos
- **No Personal Data**: No collection of personal information
- **Respectful Use**: Intended for improving infant safety

## 📚 Documentation

- **Search Strategy**: Detailed keyword design and collection strategy
- **API Documentation**: YouTube Data API usage
- **Data Processing**: Video preprocessing and annotation guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- YouTube Data API for video search capabilities
- yt-dlp for reliable video downloading
- Open source community for multi-modal AI tools

## 📞 Contact

For questions or contributions, please open an issue on GitHub.

---

**Note**: This project is designed for research and educational purposes. Always ensure compliance with local laws and YouTube's terms of service when collecting video data.
