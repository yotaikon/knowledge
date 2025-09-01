# 🧠 智能向量知识库系统

一个基于 ChromaDB 和 Sentence Transformers 的本地向量知识库系统，支持多种文档格式的智能搜索和语义检索。

## ✨ 主要特性

- 🔍 **智能语义搜索** - 基于向量相似度的语义检索，支持自然语言查询
- 📄 **多格式支持** - 支持 PDF、DOCX、TXT、图片等多种文档格式
- 🏠 **本地部署** - 完全本地化，数据安全可控
- 🎯 **高精度检索** - 使用先进的 Sentence Transformers 模型
- 📊 **结果导出** - 支持搜索结果导出为 JSON 格式
- 🖥️ **交互式界面** - 友好的命令行交互界面
- 🔧 **编程接口** - 提供完整的 Python API

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 至少 2GB 可用内存
- 支持的操作系统：Windows、macOS、Linux

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yotaikon/knowledge.git
cd knowledge
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行系统**
```bash
# 交互式查询系统（推荐）
python use_knowledge_base.py

# 或直接使用高级接口
python advanced_vector_kb.py
```

## 📖 使用指南

### 交互式查询系统

运行 `python use_knowledge_base.py` 后，您将看到以下菜单：

```
============================================================
           🧠 向量知识库查询系统 🧠
============================================================
支持功能：
1. 搜索知识库内容
2. 查看知识库统计信息
3. 导出搜索结果
4. 退出系统
============================================================
```

### 基本操作

1. **搜索知识库**
   - 选择选项 1
   - 输入搜索关键词
   - 指定返回结果数量
   - 查看搜索结果和相似度分数

2. **查看统计信息**
   - 选择选项 2
   - 查看知识库中的文档总数和基本信息

3. **导出搜索结果**
   - 选择选项 3 或在搜索后选择导出
   - 指定输出文件名
   - 结果将保存为 JSON 格式

## 📁 支持的文件格式

| 格式 | 扩展名 | 说明 | 依赖 |
|------|--------|------|------|
| PDF | .pdf | 文档和报告 | PyPDF2 或 pdftotext |
| Word | .docx | 文档文件 | python-docx |
| 文本 | .txt | 纯文本文件 | 内置支持 |
| 图片 | .jpg, .png, .bmp, .tiff | 图片文件 | pytesseract + Pillow |

## 🔧 编程接口

### 基本用法

```python
from advanced_vector_kb import AdvancedVectorKnowledgeBase

# 初始化知识库
kb = AdvancedVectorKnowledgeBase()

# 搜索文档
results = kb.search("汽车零部件", n_results=5)

# 获取统计信息
info = kb.get_collection_info()

# 导出搜索结果
kb.export_search_results("关键词", 10, "results.json")
```

### 高级用法

```python
# 处理指定目录中的所有文档
kb.process_directory("./documents")

# 处理单个文件
documents = kb.process_file("example.pdf")
kb.add_documents(documents)

# 自定义搜索参数
results = kb.search(
    query="搜索关键词",
    n_results=10,
    where={"file_type": ".pdf"}  # 只搜索PDF文件
)
```

## 📊 使用示例

### 示例 1：搜索汽车零部件相关内容

```
请输入搜索关键词: 汽车零部件
显示结果数量 (默认5): 3

正在搜索: '汽车零部件'...

✅ 找到 3 个相关结果:
--------------------------------------------------

📄 结果 1:
   文件: 汽车零部件研究.txt
   类型: .txt
   相似度: 0.892
   内容: 汽车零部件线圈生产线停机时间研究 本研究主要关注汽车零部件生产过程中线圈生产线的停机时间问题...
```

### 示例 2：导出搜索结果

```
是否导出搜索结果到文件? (y/n): y
请输入文件名 (默认: search_results.json): 汽车零部件搜索结果.json
✅ 搜索结果已导出到: 汽车零部件搜索结果.json
```

## 🏗️ 项目结构

```
knowledge/
├── 📁 local_db/                    # 向量数据库存储目录
│   ├── chroma.sqlite3             # ChromaDB 数据库文件
│   └── e2d57f6e-.../              # 向量数据目录
├── 🐍 advanced_vector_kb.py        # 高级向量知识库核心类
├── 🐍 use_knowledge_base.py        # 交互式查询系统
├── 📋 requirements.txt             # Python 依赖包列表
├── 📖 README.md                    # 项目说明文档
├── 📖 使用说明.md                  # 详细使用指南
└── 📄 各种文档文件...              # 您的知识库文档
```

## 🛠️ 技术架构

- **向量数据库**: ChromaDB
- **文本嵌入**: Sentence Transformers (all-MiniLM-L6-v2)
- **文档处理**: 
  - PDF: PyPDF2 / pdftotext
  - DOCX: python-docx
  - 图片: pytesseract + Pillow
- **编码支持**: UTF-8, GBK

## ❓ 常见问题

### Q: 为什么搜索不到结果？
A: 请检查：
1. 知识库中是否已添加文档
2. 搜索关键词是否与文档内容相关
3. 文档格式是否被正确支持

### Q: 如何处理中文文档？
A: 系统完全支持中文：
- ✅ 中文文本提取
- ✅ 中文语义搜索
- ✅ 中文文件名和路径
- ✅ 中文OCR识别

### Q: 如何提高搜索准确性？
A: 建议：
1. 使用更具体的关键词
2. 增加返回结果数量
3. 查看相似度分数，选择相关性高的结果
4. 确保文档质量良好

### Q: 系统性能如何？
A: 性能特点：
- 首次索引较慢，后续搜索快速
- 内存占用约 500MB-1GB
- 支持数万文档的索引和搜索

## 🔄 更新日志

### v1.0.0 (当前版本)
- ✅ 基础向量知识库功能
- ✅ 多格式文档支持
- ✅ 交互式查询界面
- ✅ 搜索结果导出
- ✅ 中文文档支持

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目主页: https://github.com/yotaikon/knowledge
- 问题反馈: [Issues](https://github.com/yotaikon/knowledge/issues)

---

**⭐ 如果这个项目对您有帮助，请给它一个星标！**

**祝您使用愉快！** 🎉
