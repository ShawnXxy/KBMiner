# MyKBMiner - 知识库挖掘工具集合

这个项目包含了两个专门用于技术博客爬取的 Python 脚本，用于构建数据库技术知识库。

## 项目概述

### 1. 阿里数据库内核月报爬虫 (`ali_crawler.py`)
- **目标网站**: http://mysql.taobao.org/monthly/
- **功能特性**:
  - ✅ MySQL/InnoDB 内容智能过滤
  - ✅ 增量更新机制 (跟踪已处理月份)
  - ✅ 个人文章下载 (完整内容)
  - ✅ 自动图片下载和本地引用
  - ✅ Markdown 格式转换
  - ✅ 进度跟踪和错误处理

### 2. ActionTech 技术干货爬虫 (`actiontech_crawler.py`)
- **目标网站**: https://opensource.actionsky.com/category/技术干货
- **功能特性**:
  - ✅ 全站技术文章爬取
  - ✅ 自动分页处理
  - ✅ 分类信息提取 (技术分享、故障分析、MySQL新特性等)
  - ✅ 去重处理
  - ✅ 分类统计和目录生成

## 🎯 核心功能

### 智能内容过滤
- **阿里爬虫**: 专注 MySQL/InnoDB，自动排除 PolarDB、MariaDB 等
- **ActionTech**: 自动识别技术分类，支持 13 种内容类型

### 增量更新系统
- 跟踪已处理内容，避免重复爬取
- 支持断点续传和错误恢复

### 多媒体处理
- 自动下载文章中的图片
- 生成唯一文件名避免冲突
- 更新 Markdown 中的图片引用路径
### 格式转换
- HTML 到 Markdown 的智能转换
- 保持代码块、列表、链接等格式
- 清理多余的 HTML 标签

## 使用方法

### 阿里爬虫使用
```bash
# 更新月报摘要
python ali_crawler.py

# 下载所有文章内容 (包含图片)
python ali_crawler.py --download-articles

# 测试下载几篇文章
python ali_crawler.py --test-articles

# 测试图片下载功能
python ali_crawler.py --debug-images

# 查看帮助
python ali_crawler.py --help
```

### ActionTech 爬虫使用
```bash
# 爬取所有技术文章
python actiontech_crawler.py

# 测试单页爬取
python actiontech_crawler.py --test

# 查看帮助
python actiontech_crawler.py --help
```

## 📁 输出结构

### 阿里爬虫输出

```
ali_monthly/
├── 阿里数据库内核月报.md          # 摘要文件 (按月份组织)
├── .processed_months.txt          # 增量更新跟踪文件
└── articles/                      # 完整文章内容
    ├── .img/                      # 下载的图片文件
    │   ├── abc123_diagram1.png
    │   └── def456_chart2.jpg
    ├── 2025-05_MySQL无锁哈希表LF_HASH.md
    └── 2024-12_MySQL优化器代码速览.md
```

### ActionTech 爬虫输出
```
actiontech/
├── ActionTech技术干货.md          # 所有文章 (按分类组织)
└── ActionTech技术干货_测试.md      # 测试输出文件
```

## 📊 爬取统计

### 阿里数据库内核月报
- **总月份数**: 453 个月报
- **已测试**: 4 篇文章 + 10 张图片
- **覆盖内容**: MySQL、InnoDB 相关技术文章
- **过滤效率**: 自动排除 PolarDB、MariaDB、行业动态等非核心内容

### ActionTech 技术干货
- **总文章数**: 614 篇
- **分类数量**: 13 个技术分类
- **页面总数**: 123 页
- **主要分类**:
  - 技术分享: 346 篇
  - 故障分析: 129 篇
  - MySQL 新特性: 98 篇
  - 技术文章: 25 篇
  - 其他分类: 16 篇

## 🔧 技术特点

### 共同特性
- **Python 标准库**: 仅使用 urllib、re、os 等标准库
- **编码处理**: 支持中文 URL 和内容
- **错误处理**: 完善的异常处理和日志记录
- **命令行界面**: 多种运行模式和选项

### 高级功能
- **智能过滤**: 基于关键词的内容筛选
- **增量更新**: 避免重复处理已爬取内容
- **多媒体处理**: 图片下载和本地化引用
- **格式转换**: HTML 到 Markdown 的自动转换
- **分类管理**: 自动提取和组织内容分类

## 🚀 扩展建议

### 可以添加的数据源
- 美团技术团队博客
- 字节跳动技术博客
- 腾讯云数据库团队博客
- PingCAP 技术博客
- 其他公司技术博客

### 功能增强建议
- 全文搜索功能
- 标签和关键词提取
- 自动摘要生成
- 内容相似度分析
- 定期自动更新
- Web 界面展示
- **Local References**: Updates markdown to use relative paths (`![description](.img/filename.png)`)
- **Format Support**: Handles PNG, JPG, GIF, and other web image formats
- **Size Optimization**: Preserves original image quality and dimensions
- **Deduplication**: Skips re-downloading existing images

## 🚀 Usage

### Basic Commands

```bash
# Update summary with new monthly reports
python ali_crawler.py

# Download a few sample articles for testing
python ali_crawler.py --test-articles

# Download ALL individual articles (may take time)
python ali_crawler.py --download-articles

# Run filtering logic tests
python ali_crawler.py --test

# Show help information
python ali_crawler.py --help
```

### First Run
On the first run, the crawler will:
1. Fetch all 131 monthly reports (2014-2025)
2. Filter 453 MySQL/InnoDB focused articles
3. Create a summary markdown file
4. Optionally download individual article contents

### Subsequent Runs
The crawler automatically detects new content and only processes updates, making it perfect for:
- Daily/weekly scheduled runs
- Automated knowledge base maintenance
- Keeping your MySQL documentation current

## 🔍 Content Filtering

The crawler intelligently filters content based on:

**Include**: Articles containing "MySQL" or "InnoDB" keywords
**Exclude**: Articles about PolarDB, MariaDB, MyRocks, RocksDB, TokuDB, HybridDB, X-Engine, or industry news

This ensures your knowledge base stays focused on core MySQL technologies.

## 📊 Statistics

- **Total Monthly Reports**: 131 (from 2014/08 to 2025/06)
- **MySQL Articles Found**: 453
- **Coverage Period**: Over 10 years of MySQL innovations
- **Content Quality**: High-technical depth from Alibaba's MySQL team

## 🛠 Technical Details

- **Language**: Python 3 with standard library only
- **Architecture**: Modular function-based design
- **Error Handling**: Robust with graceful degradation
- **Encoding**: Full UTF-8 support for Chinese content
- **Network**: Efficient with incremental updates

## 📝 Article Format

Each downloaded article includes:
- **Title**: Original article title
- **Metadata**: Publication date and source URL
- **Image Count**: Number of images downloaded for the article
- **Content**: Full article text converted to markdown
- **Local Images**: All images downloaded and referenced with local paths
- **Formatting**: Clean, readable markdown structure with preserved diagrams

## 🔄 Automation Ready

Perfect for automated knowledge base updates:
- Stateless operation (safe for cron jobs)
- Incremental processing (minimal resource usage)
- Error recovery (continues from interruption point)
- No configuration required

## 📚 Use Cases

- **Learning**: Comprehensive MySQL/InnoDB knowledge base
- **Research**: Historical trends in MySQL development
- **Documentation**: Offline access to technical articles
- **Analysis**: Content mining and knowledge extraction

## 🎉 Getting Started

1. Clone this repository
2. Run `python ali_crawler.py` to build your knowledge base
3. Explore the generated markdown files
4. Set up automated runs for continuous updates

Happy knowledge mining! 🚀
