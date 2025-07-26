# 多模态婴幼儿异常行为识别 - 素材收集策略

## 项目目标
利用多模态模型进行婴幼儿和照护人员的异常行为识别，包括：
- 婴幼儿异常行为检测
- 照护人员不当行为识别
- 环境安全隐患监测

## 关键词设计原则

### 1. 场景覆盖全面
- **婴幼儿行为**：哭闹、跌倒、打闹、睡眠异常
- **照护人员行为**：离开、辱骂、暴力、疏忽
- **环境因素**：陌生人、拥挤、危险区域

### 2. 中英文双语搜索
- 提高素材获取的广度和多样性
- 覆盖不同语言区域的视频内容
- 增加数据集的代表性

### 3. 关键词层次化
- **主要关键词**：核心行为描述
- **同义词**：不同表达方式
- **相关词**：扩展搜索范围

## 详细关键词分类

### 婴幼儿哭闹相关
- 中文：婴儿哭闹、幼儿哭闹、婴儿大哭、幼儿情绪失控
- 英文：baby crying、toddler crying、baby screaming、toddler tantrum

### 照护人员离开/疏忽
- 中文：照护人员离开、保姆离开房间、照护人员疏忽、无人看护婴儿
- 英文：caregiver leaving、nanny leaving room、caregiver neglect、unattended baby

### 陌生人群检测
- 中文：陌生人接触婴儿、陌生人抱婴儿、陌生人进入房间、可疑人员
- 英文：stranger touching baby、stranger holding baby、stranger entering room、suspicious person

### 拥挤检测
- 中文：人群拥挤、多人聚集、房间拥挤、人员密集
- 英文：crowded room、people gathering、room overcrowding、dense crowd

### 危险区域靠近
- 中文：婴儿靠近危险、幼儿爬向危险、靠近楼梯、靠近窗户、靠近电器
- 英文：baby near danger、toddler crawling to danger、near stairs、near window、near electrical appliances

### 跌倒未爬起
- 中文：婴儿跌倒、幼儿摔倒、跌倒不起、婴儿摔倒
- 英文：baby falling、toddler falling、falling not getting up、baby tumble

### 趴窝式睡眠
- 中文：婴儿趴睡、趴着睡觉、婴儿睡眠姿势、趴窝睡眠
- 英文：baby sleeping on stomach、sleeping face down、baby sleep position、prone sleeping

### 照护人员辱骂
- 中文：照护人员骂人、保姆发脾气、照护人员情绪失控、照护人员暴力
- 英文：caregiver yelling、nanny angry、caregiver emotional outburst、caregiver violence

### 婴幼儿互相打闹
- 中文：婴儿打架、幼儿打闹、儿童冲突、婴儿推搡
- 英文：babies fighting、toddlers fighting、children conflict、baby pushing

### 照护人员剧烈摇晃
- 中文：摇晃婴儿、剧烈摇晃、摇晃综合征、不当摇晃
- 英文：shaking baby、violent shaking、shaken baby syndrome、improper shaking

### 其他异常行为
- 中文：照护人员打骂、婴儿被虐待、照护不当、婴儿安全
- 英文：caregiver hitting、baby abuse、improper care、baby safety

## 搜索策略优化建议

### 1. 分批搜索
- 按类别分批执行，避免API限制
- 每个类别间隔适当时间

### 2. 结果筛选
- 设置视频时长过滤（建议5-30分钟）
- 排除明显不相关的视频
- 优先选择高清视频

### 3. 数据标注
- 为下载的视频添加标签
- 记录视频来源和关键词
- 建立视频分类目录

## 预期数据量
- 关键词数量：50个
- 每个关键词结果：3个
- 预期总视频数：约150个（去重后约100-120个）
- 数据大小：约10-50GB（取决于视频质量）

## 后续处理建议
1. 视频预处理（分辨率统一、时长截取）
2. 关键帧提取
3. 音频特征提取
4. 行为标注和分类
5. 数据集划分（训练/验证/测试） 