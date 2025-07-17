# MyKBMiner - 知识库挖掘工具集合

> 专门用于技术博客爬取的 Python 工具集，帮助构建高质量的数据库技术知识库

## 📚 项目概述

MyKBMiner 包含两个专业的技术博客爬虫，专注于数据库技术内容的自动化收集、过滤和组织：

### 🎯 核心工具

| 工具 | 目标网站 | 主要功能 | 状态 |
|------|----------|----------|------|
| **阿里数据库内核月报爬虫** | [mysql.taobao.org](http://mysql.taobao.org/monthly/) | MySQL/InnoDB 深度技术文章 | ✅ 生产就绪 |
| **ActionTech 技术干货爬虫** | [opensource.actionsky.com](https://opensource.actionsky.com/category/技术干货) | 数据库技术文章集合 | ✅ 生产就绪 |

---

## 🚀 阿里数据库内核月报爬虫

### 核心特性
- **智能过滤**: 自动筛选 MySQL/InnoDB 核心内容，排除 PolarDB、MariaDB 等
- **增量更新**: 跟踪已处理月份，避免重复爬取
- **完整下载**: 下载文章全文、图片，转换为离线 Markdown
- **自动化处理**: 图片本地化、路径更新、格式优化

### 📊 数据统计
- **总月份**: 131 个月报 (2014/08 - 2025/06)
- **筛选结果**: 453 篇 MySQL/InnoDB 技术文章
- **时间跨度**: 10+ 年的 MySQL 技术演进
- **内容质量**: 阿里巴巴 MySQL 团队深度技术分享

### 使用方法
```bash
# 更新月报摘要（推荐首次运行）
python ali_crawler.py

# 下载所有个人文章内容
python ali_crawler.py --download-articles

# 测试下载功能（下载几篇文章）
python ali_crawler.py --test-articles

# 调试图片下载
python ali_crawler.py --debug-images

# 查看帮助
python ali_crawler.py --help
```

### 输出结构
```
ali_monthly/
├── 阿里数据库内核月报.md          # 摘要文件（按月份组织）
├── .processed_months.txt          # 增量更新跟踪
└── articles/                      # 完整文章内容
    ├── .img/                      # 下载的图片
    │   ├── abc123_diagram1.png
    │   └── def456_chart2.jpg
    ├── 2025-05_MySQL无锁哈希表LF_HASH.md
    └── 2024-12_MySQL优化器代码速览.md
```

---

## 🏢 ActionTech 技术干货爬虫

### 核心特性
- **全站爬取**: 自动处理分页，覆盖所有技术文章
- **智能分类**: 自动识别和组织 13+ 种技术分类
- **高级过滤**: 多层过滤机制，确保内容质量
- **内容下载**: 提取完整文章内容，支持图片下载
- **增量更新**: 状态跟踪，支持定期更新

### 📊 数据统计
- **总文章**: 650+ 篇技术文章
- **分类数量**: 13+ 个专业分类
- **主要分类**:
  - 技术分享: 346 篇
  - 故障分析: 129 篇  
  - MySQL 新特性: 98 篇
  - MySQL 核心模块揭秘: 46+ 篇
  - 图解 MySQL: 10+ 篇

### 🔍 智能过滤系统

#### 标题过滤（排除关键词）
```
MariaDB, ScaleFlux, TiDB, OB运维, ClickHouse, 
行业趋势, obclient, OceanBase, Kubernetes, 
MongoDB, Orchestrator, Redis
```

#### 分类过滤（排除类别）
```
ActionDB, ChatDBA, ClickHouse, DTLE, OceanBase,
Kubernetes, MongoDB, Orchestrator, Redis
```

#### 硬性包含（特殊类别）
- **MySQL核心模块揭秘**: 深度技术剖析
- **图解 MySQL**: 可视化技术解释

### 使用方法
```bash
# 基础爬取（仅文章列表）
python actiontech_crawler.py

# 增量爬取（推荐定期使用）
python actiontech_crawler.py --incremental
python actiontech_crawler.py -i

# 完整爬取含内容下载
python actiontech_crawler.py --download
python actiontech_crawler.py -d

# 增量爬取 + 内容下载（推荐生产使用）
python actiontech_crawler.py -i -d

# 仅下载现有文章内容
python actiontech_crawler.py --download-only

# 测试功能
python actiontech_crawler.py --test
python actiontech_crawler.py --test-filter

# 强制全量爬取
python actiontech_crawler.py --full -d
```

### 推荐使用模式

#### 首次部署
```bash
python actiontech_crawler.py -d
```

#### 定期更新（生产环境）
```bash
python actiontech_crawler.py -i -d
```

### 输出结构
```
actiontech/
├── ActionTech技术干货.md          # 所有文章（按分类组织）
├── crawl_state.json              # 增量更新状态
└── articles/                     # 下载的文章内容
    ├── .img/                     # 本地图片存储
    └── *.md                      # 个人文章文件
```

---

## 🛠️ 技术特点

### 核心技术栈
- **Python 3**: 纯标准库实现，无外部依赖
- **网络处理**: urllib.request 高效 HTTP 客户端
- **内容解析**: 正则表达式精确提取
- **状态管理**: JSON 持久化增量跟踪
- **格式转换**: HTML → Markdown 智能转换

### 高级功能
- **✅ 智能过滤**: 多层次关键词和分类筛选
- **✅ 增量更新**: 状态跟踪，避免重复处理
- **✅ 多媒体处理**: 图片下载、本地化、路径更新
- **✅ 格式优化**: HTML 清理、Markdown 格式化
- **✅ 错误处理**: 完善异常处理和恢复机制
- **✅ 编码支持**: 完整 Unicode/UTF-8 支持
- **✅ 跨平台**: Windows、Linux、macOS 兼容

### 质量保证
- **内容验证**: 最小长度检查，避免空文件
- **去重处理**: URL 基础去重，确保唯一性
- **进度跟踪**: 详细进度报告和统计信息
- **错误恢复**: 个别失败不影响整体处理
- **资源管理**: 内存和网络高效使用

---

## 📈 性能表现

### 阿里爬虫
- **摘要生成**: 快速，几秒完成
- **文章下载**: 453 篇文章，适中时间
- **图片处理**: 并行下载，高效处理
- **增量更新**: 极快，仅处理新内容

### ActionTech 爬虫
- **全量爬取**: 650+ 文章，中等时间
- **增量更新**: 极快，仅处理新文章
- **内容下载**: 并行图片下载
- **内存效率**: 逐篇处理，内存友好

---

## 🎯 应用场景

### 知识库构建
- 建立专业数据库技术文档库
- 维护最新 MySQL 技术资料
- 按分类组织，便于检索

### 技术研究
- 跟踪数据库技术发展趋势
- 分析技术文章内容演变
- 历史技术决策参考

### 离线阅读
- 下载文章供离线访问
- 保持格式和图片本地化
- 创建便携式文章集合

### 自动化监控
- 定时任务自动更新
- 监控特定技术分类
- 集成通知系统

---

## 🚀 快速开始

### 环境要求
- Python 3.6+
- 网络连接
- 磁盘空间（建议 1GB+）

### 安装使用
```bash
# 克隆项目
git clone https://github.com/ShawnXxy/MyKBMiner.git
cd MyKBMiner

# 运行阿里爬虫（构建知识库）
python ali_crawler.py

# 运行 ActionTech 爬虫
python actiontech_crawler.py -i -d

# 查看输出结果
ls ali_monthly/
ls actiontech/
```

### 定时任务设置

#### Linux/macOS (crontab)
```bash
# 每天早上 8 点更新
0 8 * * * cd /path/to/MyKBMiner && python ali_crawler.py
0 8 * * * cd /path/to/MyKBMiner && python actiontech_crawler.py -i -d
```

#### Windows (任务计划程序)
- 创建基本任务
- 设置触发器：每日
- 操作：启动程序 `python`，参数 `ali_crawler.py`

---

## 📊 最新统计

| 指标 | 阿里爬虫 | ActionTech 爬虫 | 总计 |
|------|----------|-----------------|------|
| **文章数量** | 453 篇 | 650+ 篇 | 1100+ 篇 |
| **时间跨度** | 2014-2025 | 近期活跃 | 10+ 年 |
| **分类数** | MySQL/InnoDB | 13+ 分类 | 15+ 分类 |
| **内容质量** | 极高深度 | 高实用性 | 综合优秀 |

---

## 🔮 未来规划

### 功能增强
- [ ] 多线程下载提升性能
- [ ] 高级内容分析和分类
- [ ] 外部数据库集成
- [ ] Web 管理界面
- [ ] 高级过滤配置
- [ ] 内容质量评分

### 数据源扩展
- [ ] 美团技术团队博客
- [ ] 字节跳动技术博客  
- [ ] 腾讯云数据库博客
- [ ] PingCAP 技术博客
- [ ] 其他优质技术博客

---

## 📝 版本信息

- **当前版本**: v2.0.0
- **状态**: 生产就绪 ✅
- **最后更新**: 2025-07-17
- **总功能**: 20+ 综合特性
- **维护状态**: 积极维护

---

## 🏁 总结

MyKBMiner 提供了完整的技术内容挖掘解决方案，从阿里数据库月报的深度技术到 ActionTech 的实用干货，涵盖了数据库技术学习和研究的各个层面。

**核心优势**:
- 🎯 **专业聚焦**: 专门针对数据库技术
- 🚀 **高度自动化**: 增量更新，定时任务
- 📚 **内容丰富**: 1100+ 篇高质量技术文章
- 🔧 **生产就绪**: 稳定可靠，错误处理完善

立即开始构建你的数据库技术知识库！🚀
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
