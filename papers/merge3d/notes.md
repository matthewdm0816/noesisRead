# Merge3D: Efficient 3D Multimodal LLMs via Joint 2D-3D Token Merging

## 元信息
- **Authors**: Tianbo Pan, Xingyi Yang, Xinchao Wang
- **Venue**: CVPR 2026
- **arXiv**: 暂无（项目页面标注 Coming Soon）
- **DOI**: 暂无
- **Project Page**: [https://tianbo-pan.github.io/merge3d/](https://tianbo-pan.github.io/merge3d/)
- **开源**: 暂无（Code / arXiv 均标注 Coming Soon）

---

## 费曼讲解

大家好，我来聊聊 Merge3D 这篇工作的核心思路。

**一句话版本：** 如果你有 1000 块拼图碎片但只需要 100 块就能看懂画面，你会怎么挑？Merge3D 的答案是——既要挑"好看"的（语义重要），也要挑"位置对"的（几何一致）。

**展开来说：**

最近有一批工作（比如 VG LLM、Spatial-MLLM）用两个视觉编码器来理解 3D 场景：一个 2D 编码器负责提取外观和语义特征（比如"这是椅子"），一个 3D 几何编码器负责理解空间关系（比如"这把椅子在桌子前方 1 米"）。两个编码器的特征融合后一起喂给 LLM 来回答问题。

问题是，双编码器意味着每帧图像产出两套 token，视频有几十帧，token 数量爆炸——LLM 的自注意力是 $O(n^2)$ 的，1600 个 visual token 一次推理就要 10 秒。

之前有人做过 2D token 压缩（比如 VisionZip），但只用 2D 注意力来选重要 token、合并相似 token。我们在实验中发现，这对 3D 任务来说是不够的：

- 2D 注意力擅长挑"语义重要"的 token（适合回答"房间里有什么"）
- 3D 特征擅长保持"空间位置正确"的 token（适合回答"桌子在哪里"）
- 如果只用 2D 信息做合并，外观相似但位置不同的 token 可能被错误地混在一起，导致 3D grounding 崩盘

**Merge3D 的解法很直觉：**

1. **挑赢家（Dominant Token Selection）：** 用 2D 编码器的注意力分数来挑选最重要的 token——这些是"语义 C 位"，它们大概率跟用户的问题相关。

2. **分组搬家（Contextual Token Merging）：** 对于剩下的 token，不是简单按外观相似度合并，而是计算一个**混合相似度** = 2D 语义相似度 × 3D 几何相似度。这确保只有"长得像"**且**"位置近"的 token 才会被合并到同一个 dominant token 上。

用类比来说：想象你在整理图书馆。只按语义分类（2D），你可能会把图书馆 A 的"科幻小说"和图书馆 B 的"科幻小说"归到一起——虽然内容相似但位置完全不同。Merge3D 的做法是：先确认"这是同一栋楼的书"（3D 几何约束），再按内容分类（2D 语义），这样整理出来的结果既有意义又不会丢失空间信息。

**效果：** 删掉 70% 的 token 后，3D grounding 指标只掉 6% 左右，推理速度快 2.5 倍。极端压缩到只留 5% token 时，仍然比所有 baseline 强。

## 摘要翻译

> 融合了 3D 几何信息的多模态大语言模型（MLLM）在 3D 场景理解方面展现出强大能力。然而，其主要瓶颈在于处理多视角、冗长的视觉 token 序列所带来的巨大计算负担。为克服这一挑战，我们提出了 Merge3D，一种融合 3D 几何与 2D 语义信息的几何感知 token 合并框架。传统的 2D 压缩方法仅依赖语义信号，对于 3D 任务而言并不充分，因为它们倾向于丢弃空间上关键的 token 并损害 grounding 性能。Merge3D 通过语义-几何 token 合并器（SemGeo Merger）桥接两种模态：2D 注意力用于选取语义上显著的主导 token，而混合 2D+3D 相似度则从空间连贯的 3D 邻域中分配和聚合上下文 token。这种设计在激进压缩下保留了 3D 结构先验和帧间对应关系。Merge3D 实现了高达 70% 的视觉 token 减少和约 3 倍的推理加速，同时在 Scan2Cap、CV-Bench 和 BLINK 等 3D grounding、描述和空间推理基准上保持强劲性能。

## 引言翻译

> 融合了 3D 几何信息的多模态大语言模型（MLLMs）在 2D 图像和视频理解方面取得了显著成功，推动了其向 3D 领域的扩展，包括场景理解、视觉-语言-动作框架和具身导航。尽管取得了这些进展，最近的研究揭示了空间推理方面持续存在的局限性：MLLMs 往往将视频帧视为孤立的 token，未能捕捉帧间对应关系等关键 3D 线索。此前增强 MLLMs 3D 感知的努力依赖于视频序列，但需要显式的 3D 输入——例如注入的坐标或重建的鸟瞰图（BEV）地图——这在现实场景中很稀缺，且从图像估计时容易出错。
>
> 为了消除这种依赖，预训练的前馈 3D 重建模型（如 VGGT）可以为多视图图像提供强大的几何先验。在此基础上，VG LLM 和 Spatial-MLLM 开创了一种纯视觉的双编码器架构，将 2D 语义特征与从视频序列中提取的 3D 几何先验融合。这种设计无需显式 3D 数据即可实现稳健的 3D 视觉 grounding 和空间推理，取得了令人期待的结果。然而，双编码器架构为多帧视频产生了较长的视觉 token 序列，在训练和推理过程中带来了巨大的计算开销。
>
> 我们观察到大量的视觉 token 冗余，这与 2D 视觉-语言 token 压缩领域的发现一致。然而，2D 和 3D 编码器的双注意力图的引入为 token 选择和合并带来了独特的挑战。从经验上看，我们发现了一个明显的任务依赖模式：2D 注意力引导的合并在空间推理基准上表现优异（如 CV-Bench、BLINK），而 3D 注意力引导的合并在 3D grounding 和检测上表现更好（如 Scan2Cap）。特征分布分析进一步确认了它们互补的表征优势：3D 几何 token 表现出强聚类性，编码空间邻近性和跨帧一致性，而 2D 语义 token 更分散，捕捉细粒度的外观细节。因此，一种融合语义显著性和几何一致性的混合合并策略仍然严重欠缺探索。
>
> 在本文中，我们介绍了 Merge3D，一种面向双编码器 3D 视频 MLLM 的几何感知 token 合并框架。Merge3D 在 VG LLM 基础上增加了语义-几何 token 合并器（SemGeo Merger），以 2D 特征相似度为锚点选取语义上显著的目标 token，并利用 3D 特征相似度从空间连贯的 3D 邻域中分组和聚合源 token。这种双相似度融合平衡了两种模态的贡献，通过在保留 2D 语义的同时维护 3D 结构先验来增强空间保真度。在几何上有意义的簇内进行合并，维持了帧间对应关系和视角不变性，这对于自我中心-他人中心推理至关重要。Merge3D 在所有指标和 token 保留比率上均达到最优或极具竞争力的表现，在极端压缩（5% token）时优势尤其明显。

## 论文总结

Merge3D 提出了一种面向双编码器 3D 视频多模态大语言模型的几何感知 token 合并框架。核心是 SemGeo Merger 模块：利用 2D 编码器的注意力分数选取语义显著的主导 token，再通过 2D 语义相似度和 3D 几何相似度的乘积融合来分配和聚合剩余的上下文 token。该方法在 VG LLM 基础上实现了最高 70% 的视觉 token 压缩和约 3 倍推理加速，在 Scan2Cap 3D grounding、CV-Bench 和 BLINK 空间推理基准上均优于仅用 2D 或 3D 信息的压缩方法。

## 核心问题

**问题：** 双编码器 3D 视频 MLLM 产生的视觉 token 序列过长，导致训练和推理的计算代价极高。现有的 token 压缩方法（如 VisionZip）仅基于 2D 语义信息，无法同时保持 3D 空间结构——它们会把外观相似但空间位置不同的 token 错误合并，导致 3D grounding 性能大幅下降。

**为什么重要：** 3D 场景理解是机器人、AR/VR、自动驾驶等领域的核心能力。双编码器架构（2D 语义 + 3D 几何）已成为主流范式，但 token 冗余使其实用部署困难。简单压缩会破坏空间信息，不压缩则计算代价不可接受。这是一个效率-质量的核心权衡问题。

**现有方法不足：**
- VisionZip 等 2D 压缩方法只关注语义显著性，忽视 3D 几何结构，压缩后 grounding 性能退化严重
- Visionzip-3D（仅用 3D 信息）在语义任务上表现差，会产生类别混淆
- 随机裁剪（Randomzip）在所有指标上都表现最差
- 没有现成方法能同时利用 2D 和 3D 信息进行 token 压缩

## 方法详解

### 整体框架

Merge3D 构建在 VG LLM（Video-3D Geometry LLM）之上，保持 2D 视觉编码器、3D 几何编码器和视频 LLM 解码器冻结，仅在融合阶段和解码器之间插入 SemGeo Merger 模块进行训练。

**流程：**
1. 输入多帧 RGB 视频 $\{I_k\}_{k=1}^{m}$ 和语言 prompt $P$
2. 2D 编码器提取每帧特征 $F_k^{2D} \in \mathbb{R}^{h \times w \times d}$（经 $2 \times 2$ 空间下采样）
3. 3D 几何编码器（VGGT）提取几何特征 $F_k^{3D} \in \mathbb{R}^{h \times w \times d}$（同样下采样）
4. 逐元素相加融合：$F_k^{fus} = F_k^{2D'} + F_k^{3D'}$
5. 展平得到 token 序列 $T^{fus} \in \mathbb{R}^{n \times d}$，其中 $n = m \cdot h \cdot w$
6. **SemGeo Merger 压缩 token**
7. 压缩后的视觉 token 与文本 token 拼接，送入 LLM 解码器生成回答

### SemGeo Merger 核心模块

#### 1. Dominant Token Selection（主导 token 选取）

用 2D 编码器某一层的注意力张量 $A \in \mathbb{R}^{B \times H_a \times n \times n}$ 来计算每个 token 的重要性分数：

- 对每个 token，沿 query 维度求和收到的注意力，再跨注意力头取平均
- 按重要性分数选 top-K token 构成主导集 $D = \{d_1, \ldots, d_K\}$
- 其余 token 构成上下文集 $C = T^{fus} \setminus D$

**为什么用 2D 注意力选主导 token：** 实验表明 2D 注意力图在 query-relevant 区域有集中激活模式，更适合挑出语义上最重要的 token。

#### 2. Contextual Token Merging（上下文 token 合并）

这是本文的核心创新。对 2D 和 3D 特征分别展平得到：
- $V = [v_1, \ldots, v_n]^\top \in \mathbb{R}^{n \times d}$（2D 特征）
- $G = [g_1, \ldots, g_n]^\top \in \mathbb{R}^{n \times d}$（3D 特征）

对主导 token $d_k \in D$ 和上下文 token $c \in C$，计算：

**语义相似度：**
$$s_{sem}(k, c) = \exp\left(\frac{v_k^\top v_c}{\tau_{sem}}\right)$$

**几何相似度：**
$$s_{geo}(k, c) = \exp\left(\frac{g_k^\top g_c}{\tau_{geo}}\right)$$

**混合相似度（乘积融合）：**
$$s_{fuse}(k, c) = s_{sem}(k, c) \cdot s_{geo}(k, c)$$

每个上下文 token 被分配到混合相似度最高的主导 token：
$$a(c) = \arg\max_{k \in D} s_{fuse}(k, c)$$

设 $C_k = \{c \in C \mid a(c) = k\}$ 为分配给 $d_k$ 的上下文 token 集合，合并更新为：
$$\hat{d}_k = d_k + \frac{1}{|C_k|} \sum_{c \in C_k} c$$

若 $C_k$ 为空则 $\hat{d}_k = d_k$。

**乘积融合的关键意义：** 只有同时"语义相似"**且**"几何邻近"的 token 才会获得高权重。这防止了远距离但外观相似的区域被错误合并，保持了准确的 3D grounding。

### 训练细节

- **冻结参数：** 2D 编码器、3D 几何编码器（VGGT）、LLM 骨干（Qwen2.5-VL）全部冻结
- **仅训练：** SemGeo Merger 模块
- **损失函数：** 统一的 next-token prediction（标准自回归语言建模目标）
- **训练数据：** ScanRefer（36,665 条物体描述，562 个扫描）、Scan2Cap（带 Mask3D proposals）、SPAR-7M 子集（234K 条，33 种任务）、LLaVA-Video-178K（63K 条）
- **优化器：** Adam，batch size 64，warmup ratio 0.03，峰值学习率 $1 \times 10^{-5}$ 后线性衰减
- **训练资源与时间：** 8 × H100 80G GPU，仅需 1/4 epoch（约 2-3 小时）即可收敛，非常高效

## 实验与可视化

### 实验设置

**数据集/基准：**
- **Scan2Cap：** 3D dense captioning + visual grounding，指标包括 CIDEr (C@0.5)、BLEU-4 (B-4@0.5)、METEOR (M@0.5)、ROUGE-L (R@0.5)，IoU 阈值 0.5
- **CV-Bench：** 空间推理，分 2D 子集（平面关系如左右/前后）和 3D 子集（深度排序和几何关系）
- **BLINK：** 挑战性空间推理，分 Depth（度量/序数距离理解）、Spatial（单视角关系推理）、Multi-View（视角变化下的自我-他人中心一致性）

**基线：**
- Visionzip-2D：仅用 2D 语义相似度做 token 选择和合并
- Visionzip-3D：仅用 3D 几何相似度
- Randomzip：随机选择和合并（结构无关的裁剪基线）
- VG LLM-4B：原始无压缩基线

### 主要结果

#### Scan2Cap（3D Grounding + Dense Captioning）

| 方法 | Token 保留率 | C@0.5 | B-4@0.5 | M@0.5 | R@0.5 |
|------|-------------|-------|---------|-------|-------|
| Baseline (VG LLM-4B) | 100% | 78.6 | 40.9 | 28.6 | 62.4 |
| Merge3D* | 30% | 73.4 | 39.3 | 28.2 | 61.6 |
| Merge3D* | 10% | 66.1 | 37.9 | 27.5 | 61.1 |
| Merge3D* | 5% | 57.9 | 36.1 | 26.8 | 60.5 |

- 30% 保留率下保留 93.4% 的 CIDEr 性能，加速 2.5 倍
- 5% 保留率下 CIDEr=57.9，仍优于 Visionzip-3D (52.4)、Visionzip-2D (49.5)、Randomzip (51.2)

#### CV-Bench（空间推理）

| 方法 | Token 保留率 | 2D (%) | 3D (%) | Avg. (%) |
|------|-------------|--------|--------|----------|
| Baseline | 100% | 72.9 | 91.3 | 82.1 |
| Merge3D* | 30% | 71.0 | 88.1 | 79.6 |
| Merge3D* | 10% | 68.6 | 86.3 | 77.5 |
| Merge3D* | 5% | 67.5 | 82.0 | 74.8 |

- 30% 保留率下保留 97.0% 的平均准确率
- 5% 保留率下 Avg. 74.8%，远超 Visionzip-2D (68.9%)、Visionzip-3D (63.6%)

#### BLINK（空间推理）

| 方法 | Token 保留率 | Depth | Spatial | Multi-View | Avg. |
|------|-------------|-------|---------|------------|------|
| Baseline | 100% | 79.8% | 67.8% | 57.1% | 68.4% |
| Merge3D* | 30% | 78.2% | 68.5% | 55.6% | 67.5% |
| Merge3D* | 5% | 62.9% | 62.9% | 55.6% | 60.5% |

- Multi-View 子集对所有方法都很困难（55-57%），token 合并本身不足以应对大视角变化

#### 推理效率

| 方法 | Token 数 | 总推理时间 | 加速比 |
|------|---------|-----------|--------|
| Baseline | 1623 | 10.58s | - |
| Merge3D (30%) | 564 | 4.14s | 2.5× |
| Merge3D (5%) | 186 | 3.40s | 3.1× |

### 消融实验

#### 2D vs 3D 相似度消融（CV-Bench, 5% 保留率）

| 2D 相似度 | 3D 相似度 | 2D (%) | 3D (%) | Avg. (%) |
|-----------|-----------|--------|--------|----------|
| ✓ | ✗ | 64.8 | 80.7 | 72.8 |
| ✗ | ✓ | 63.7 | 80.8 | 72.3 |
| ✓ | ✓ | 67.5 | 82.0 | 74.8 |

关键发现：
- 2D 相似度主要抑制类别混淆和误检（语义保真）
- 3D 相似度主要稳定 3D 位置和朝向（空间保真）
- 两者联合使用在 2D 和 3D 子集上均取得最佳效果，证明互补而非冗余
- 乘积融合 $s_{fuse} = s_{sem} \cdot s_{geo}$ 的设计得到经验验证

#### 定性分析

- Merge3D 在激进压缩下仍能产出与 ground truth 对齐的紧致 3D 框
- Visionzip-3D 容易产生过大的框（跨越物体边界，仅按几何相似度合并会把不同物体混在一起）
- Visionzip-2D 产生更多错位和不完整的框（仅按语义合并会丢失 3D 连贯性）
- 去掉 2D 相似度：产生杂乱和语义混淆的预测，重叠框和伪检测增多
- 去掉 3D 相似度：类别保留较好但框明显错位，位置和范围不匹配真实 3D 布局

## 相关工作

### 多模态大语言模型（MLLMs）
从视频理解（Video-ChatGPT、VideoLLaMA）到 3D QA 的演进，将多视图图像视为序列利用 2D 数据。LLaVA-NeXT-Interleave 统一了多图像、视频和 3D 输入。Merge3D 在此基础上聚焦于通过几何感知 token 压缩提升效率和空间推理。

### 3D 大多模态模型
从点云方法（3D-LLM、PointLLM、GPT4Point）到混合 2D-3D 方法（Chat-3D、Chat-Scene、LEO、Scene-LLM）。近期趋势是从 3D 专用训练转向 2D 迁移：LLaVA-3D、3D-LLaVA 等将 3D 先验注入图像/视频模型。VG LLM 和 Spatial-MLLM 引入 VGGT 隐式融合 3D 知识。Merge3D 在 VG LLM 基础上进一步解决效率问题。

### Token 压缩
包括 view sampling、pooling、pruning、merging、memory 等技术。VisionZip 展示了 2D CLIP token 的稀疏性。2024-2025 年出现 Dynamic-VLM、Balanced Token Pruning、PVC 等动态压缩方法。这些方法主要针对全局视频 QA 效率，将视觉 token 视为纯语义的，很少考虑 3D 几何或双编码器 2D-3D 表示。

**本文与它们的区别：** Merge3D 是第一个专门为双编码器 3D 视频 MLLM 设计的几何感知 token 合并框架，同时利用 2D 语义显著性和 3D 几何邻近性进行 token 压缩。

## 潜在未来工作

1. **自适应保留策略：** 当前使用固定的 token 保留比率，未来可探索任务自适应或视角自适应的保留策略——例如对简单场景保留更少 token，对复杂场景保留更多。

2. **扩展到更多骨干和任务：** 将 SemGeo Merger 应用于不同的 LLM 骨干（如更大的 Qwen、LLaMA 变体）和更多 3D 下游任务（如具身导航、机器人操作）。

3. **长时程具身场景：** 论文提到 Multi-View 子集仍是挑战（所有方法 55-57%），处理大视角变化可能需要超越 token 合并的额外机制。

4. **动态 token 分配：** 不同帧的信息密度不同，可以根据帧内容动态调整每帧保留的 token 数量。

5. **与训练时压缩结合：** 当前方法在推理时进行 token 合并（训练仅更新 merger 模块），探索训练时即感知压缩的方法可能进一步减少性能损失。

6. **端到端 3D 重建与理解的联合优化：** 将 VGGT 的 3D 重建质量与下游理解任务的梯度信号结合，可能进一步提升几何先验的有效性。
