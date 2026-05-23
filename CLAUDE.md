# ReadPapers

论文阅读与分析工作流项目。

## 目录结构

```
papers/<paper-slug>/
├── paper.pdf        # 下载的论文 PDF
├── notes.md         # 完整分析笔记
└── metadata.json    # 结构化元数据
```

## 论文阅读工作流

Owner 给出论文（标题、URL、PDF 路径，或一个列表文件），按以下流程处理每篇论文：

### Step 1: 查找论文 & 获取元数据

Spawn 一个 Agent 子任务（subagent_type: `general-purpose`），prompt 如下：

> 搜索这篇论文的信息："{论文标题或URL}"
>
> **重要：不要使用 Semantic Scholar API，它严重 rate limited。**
>
> 搜索策略（按优先级依次尝试，直到找到足够信息）：
> 1. 用 WebSearch 搜索 `"{论文标题}" site:arxiv.org` 或直接 WebFetch `https://arxiv.org/search/?query={论文标题}&searchtype=all` 找到 arXiv 页面
> 2. 用 WebSearch 搜索 `"{论文标题}" site:dblp.org` 找到 DBLP 记录（获取 venue、DOI、正式发表信息）
> 3. 用 WebSearch 搜索 `"{论文标题}"` 作为兜底，找 conference / journal 页面
> 4. 如果有 arXiv 页面，用 WebFetch 获取元数据（标题、作者、摘要、年份）
> 5. 获取 PDF 下载链接（优先 arXiv PDF）
> 6. 下载 PDF 到 `{项目绝对路径}/papers/<slug>/paper.pdf`（用 Bash 的 curl）
>
> 将结果以 JSON 格式返回，包含以下字段：
> ```json
> {
>   "title": "...",
>   "authors": ["..."],
>   "abstract": "...",
>   "year": 2024,
>   "venue": "NeurIPS 2024 / arXiv preprint / ...",
>   "arxiv_id": "...",
>   "arxiv_url": "...",
>   "pdf_url": "...",
>   "doi": "...",
>   "published": true/false,
>   "note": "..."
> }
> ```
>
> 如果找不到正式发表版本，在 published 字段标记 false，在 note 中说明。
>
> **搜索纪律：每种搜索策略最多尝试 2 次，没找到就换下一种，全部试完还没找到就停。** 用已有的信息填写，缺失字段标记 "unknown"，在 note 中说明搜索未果。不要为了凑齐字段而无休止地搜索。
> slug 格式：论文标题的 kebab-case 简短版本（不超过 60 字符）。

拿到结果后，将 JSON 写入 `papers/<slug>/metadata.json`。

### Step 2: 阅读论文

用 Read 工具读取 PDF（大文件用 pages 参数分页读取）。

**如果 Read 报 "password-protected" 错误**，用 pypdf 去除权限限制后重试：
```python
from pypdf import PdfReader, PdfWriter
reader = PdfReader("papers/<slug>/paper.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.write("papers/<slug>/paper_decrypted.pdf")
```
然后读取 `paper_decrypted.pdf`。如果 pypdf 也失败，尝试用 `pymupdf` (`fitz`) 另存一份。

### Step 3: 检查开源状况

Spawn 一个 Agent 子任务（subagent_type: `general-purpose`），prompt 如下：

> 检查这篇论文的开源状况："{论文标题}"
>
> 论文信息：{从 metadata.json 摘要关键信息}
>
> 请按以下步骤检查：
> 1. 用 WebSearch 搜索 "{论文标题} github" 和 "{论文标题} code"
> 2. 用 WebSearch 搜索 "{论文标题} huggingface" 和 "{论文标题} model"
> 3. 用 WebSearch 搜索 "{论文标题} dataset"
> 4. 用 WebFetch 检查论文的 project page（如果有）
> 5. 在论文正文中查找是否提到了代码仓库、数据集链接、模型链接
> 6. 对找到的每个 GitHub repo，用 WebFetch 验证它确实存在且有实质内容（不是空 repo）
>
> 返回 JSON：
> ```json
> {
>   "code": [{"url": "...", "description": "...", "verified": true/false}],
>   "data": [{"url": "...", "description": "...", "verified": true/false}],
>   "model": [{"url": "...", "description": "...", "verified": true/false}],
>   "project_page": "...",
>   "summary": "一句话总结开源状况"
> }
> ```
>
> 如果什么都没找到，返回空数组并在 summary 中说明。

拿到结果后，合并到 `metadata.json` 的 `opensource` 字段。

### Step 4: 撰写分析笔记

按以下模板生成 `papers/<slug>/notes.md`，同时在对话中输出摘要版。

**公式与数学符号**：所有公式、数学符号必须用 Markdown 支持的 LaTeX 语法书写。行内公式用 `$...$`，独立公式用 `$$...$$`。不要用纯文本近似（如 `x^2`、`α`），必须写成 `$x^2$`、`$\alpha$`。

#### notes.md 模板

```markdown
# <论文标题>

## 元信息
- **Authors**: ...
- **Venue**: ... (Year)
- **arXiv**: [link](url)
- **DOI**: ...
- **开源**: [code](url) / [data](url) / [model](url) / 暂无

---

## 费曼讲解

以作者口吻，面向平均 ML/AI PhD 学生（对大多数领域仅有泛泛了解）解释这篇论文。
使用类比和简单的语言，从最核心的 idea 出发，逐步展开。
不要使用行话轰炸，先建立直觉再给细节。

## 摘要翻译

> （中文翻译原文 Abstract）

## 引言翻译

> （中文翻译原文 Introduction，保留原文段落结构）

## 论文总结

一段话概括这篇论文做了什么。

## 核心问题

这篇文章试图解决什么问题？为什么这个问题重要？现有方法的不足是什么？

## 方法详解

详细、明白地解释方法细节，要求读者不看论文就能理解：
- 整体框架/流程是什么
- 每个关键组件做什么、如何工作
- 关键的技术创新点在哪里
- 训练/推理流程是怎样的（如适用）
- 损失函数/优化目标是什么（如适用）

## 实验与可视化

- 实验设置（数据集、基线、评估指标）
- 主要结果（关键数字和对比）
- 消融实验的关键发现
- 可视化分析（如果有）

## 相关工作

关键的 related work，以及本文与它们的区别。

## 潜在未来工作

可能的未来研究方向和着手点。
```

#### 对话摘要版

在对话中输出以下精简版：
- 一句话总结
- 核心问题
- 方法亮点（3-5 个要点）
- 关键实验结果
- 开源状况

### Step 5: 批量模式（分阶段并行）

如果 Owner 给的是列表文件或多个论文，分两阶段并行处理：

#### Phase 1: 批量获取元数据

1. 解析论文列表（从文件或对话中提取）
2. **并行** spawn 多个 Agent 子任务，每个负责一篇论文的元数据获取
   - 一次最多 spawn 5 个 agent 并行
   - 超过 5 篇则分批，每批完成后启动下一批
   - 每个 agent 的 prompt 包含：论文标识、项目绝对路径、期望输出的 slug 格式
   - 每个 agent 完成：metadata.json 写入 + PDF 下载
3. 汇总检查：确认所有 PDF 和 metadata.json 就位，缺失的标记出来，Phase 2 自动跳过这些论文

#### Phase 2: 并行阅读 & 分析

确认 Phase 1 完成后：

1. **并行** spawn 多个 Agent 子任务，每篇论文一个独立 agent
   - 同样最多 5 个并行
   - 每个 agent 的 prompt 包含以下完整上下文（agent 没有父对话记忆）：
     - 论文 PDF 路径
     - metadata.json 内容（标题、摘要、年份等关键信息）
     - notes.md 输出路径
     - notes.md 模板（完整 section 要求）
     - 分析要求：费曼法、面向平均 ML PhD、中文翻译摘要和引言
     - 开源检查要求：搜索 GitHub/HuggingFace、检查论文正文、验证 repo
   - 每个 agent 完成：读 PDF → 分析 → 检查开源 → 写 notes.md → 更新 metadata.json opensource 字段
2. 每个 agent 完成后在对话中输出该论文的摘要版

#### Phase 2 Agent Prompt 模板

给每个阅读 agent 的 prompt 应包含以下完整信息（agent 没有父对话记忆，必须自包含）：

```
你是一个论文阅读助手。请完成以下任务：

## 论文信息
- PDF 路径：{absolute_path}/papers/{slug}/paper.pdf
- metadata.json 路径：{absolute_path}/papers/{slug}/metadata.json
- 论文标题：{title}
- 已知摘要：{abstract}

## 任务

### 1. 读取论文
用 Read 工具读取 PDF（大文件用 pages 参数分页读取）。

### 2. 撰写分析笔记
用 Read 工具先读取 metadata.json 获取元数据，然后将以下完整分析写入 notes.md：

（插入 notes.md 模板的完整内容，见上方 Step 4）

### 3. 检查开源状况
- WebSearch 搜索 "{title} github"、"{title} code"、"{title} huggingface"、"{title} dataset"
- WebFetch 检查论文 project page（如果有）
- 在论文正文中查找代码/数据/模型链接
- 对找到的 GitHub repo 用 WebFetch 验证存在性
- 将结果写入 metadata.json 的 opensource 字段：
  {"code": [...], "data": [...], "model": [...], "project_page": "...", "summary": "..."}

### 4. 输出摘要
最后在你的回复中输出一段对话摘要版（一句话总结 + 核心问题 + 方法亮点 + 关键实验 + 开源状况）。
```

#### Phase 3: 汇总

全部完成后：
- 在对话中输出汇总表格（标题 | venue | 一句话总结 | 开源状况）
- 生成 `papers/index.md` 汇总索引

## 工具脚本

放在 `scripts/` 目录。按需创建，不提前写。常见场景：
- PDF 批量下载
- notes.md 渲染为 docx
- 汇总索引生成
