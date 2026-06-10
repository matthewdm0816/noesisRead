# Sparse3DPR: Training-Free 3D Hierarchical Scene Parsing and Task-Adaptive Subgraph Reasoning from Sparse RGB Views

## 元信息
- **Authors**: Haida Feng, Hao Wei, Zewen Xu, Haolin Wang, Chade Li, Yihong Wu
- **Venue**: AAAI 2026
- **arXiv**: [2511.07813](https://arxiv.org/abs/2511.07813)
- **DOI**: [10.48550/arXiv.2511.07813](https://doi.org/10.48550/arXiv.2511.07813)
- **开源**: 暂无

---

## 费曼讲解

想象你是一个机器人管家，需要理解一个房间的布局来回答主人的问题，比如"离门最近的椅子在哪里？"。

最直觉的方法是把房间里所有物体以及它们之间的关系都描述成文字，然后丢给一个大语言模型去推理。ConceptGraphs 就是这么做的——它把所有物体和两两关系平铺成一个"扁平"的场景图。问题是，这就像把一本百科全书一页纸全印出来给 LLM 看，信息太多太杂，LLM 很难高效推理。

Sparse3DPR 的核心 insight 来自人类认知：我们理解房间时，首先会识别出大平面结构——地板、墙壁、天花板，然后把物体"挂"在这些平面结构下面。这就像整理衣柜：不是把所有衣服堆成一堆，而是按"衣架-层板-抽屉"的层级来组织。

具体来说，Sparse3DPR 做了三件事：

**第一，建一个有层级的场景图 (HPSG)。** 最顶层是场景类型（如"办公室"），中间层是结构平面（墙、地板、天花板），底层是具体物体。物体通过最小生成树连接到最近的结构平面，就像衣服挂在最近的衣架上。

**第二，只给 LLM 看跟问题相关的部分 (Task-Adaptive Subgraph)。** 如果问题是"门旁边的椅子"，就不需要把天花板上的灯的信息也塞给 LLM。方法是用句子嵌入计算问题和每个节点的语义相似度，取出最相关的种子节点，再扩展它们的一阶和二阶邻居，形成一个精简的子图。

**第三，只需要稀疏的 RGB 图片。** 不需要深度相机或稠密点云，用 DUSt3R 从几张普通照片就能重建 3D 几何。

整个流程不需要任何 3D 任务特定的训练，完全利用预训练好的模型（SAM2、GroundingDINO、DUSt3R、Qwen-VL）的能力。

## 摘要翻译

> 近年来，大语言模型（LLM）在 3D 场景理解中得到了广泛探索。其中，免训练方法因其灵活性和泛化能力而受到越来越多的关注。然而，这些方法在实际部署中通常面临准确性和效率的挑战。为解决这些问题，我们提出了 Sparse3DPR，一种利用预训练 LLM 推理能力的新型免训练开放场景理解框架，仅需稀疏视角 RGB 输入。具体而言，我们引入了层次化平面增强场景图（HPSG），它支持开放词汇并采用主导平面结构作为空间锚点，从而实现更清晰的推理链和更可靠的高层推理。此外，我们设计了任务自适应子图提取方法，动态过滤与查询无关的信息，减少上下文噪声，提升 3D 场景推理效率和准确性。实验结果表明 Sparse3DPR 的优越性：在 Space3D-Bench 上相比 ConceptGraphs 实现了 28.7% 的 EM@1 提升和 78.2% 的加速。此外，Sparse3DPR 在 ScanQA 上取得了与训练方法相当的性能，真实世界实验进一步证实了其鲁棒性和泛化能力。

## 引言翻译

> 三维（3D）场景理解对具身人工智能至关重要，因为它使机器人能够在复杂物理环境中理解、推理和执行自然语言指令。随着大语言模型（LLM）的快速发展，特别是其在沟通、常识推理和开放世界知识整合方面的强大能力，激发了基于 LLM 的 3D 场景理解解决方案。
>
> 现有方法大致可分为训练方法和免训练方法。训练方法通过专门训练将 3D 几何或视觉特征与文本特征对齐，需要复杂架构并产生高昂计算成本。免训练方法则构建显式的结构化表示（如场景图），编码物体和空间关系，然后将场景图转化为文本上下文输入 LLM，从而利用其强大的零样本推理能力，同时消除训练成本。
>
> 尽管免除了 3D 特定训练，免训练方法在实际部署中仍面临推理准确性和计算效率的挑战。第一个瓶颈是 3D 场景表示的质量和结构组织，它是 LLM 的主要上下文输入，显著影响推理可靠性。当前用于 LLM 推理的场景图分为两类：扁平场景图（如 ConceptGraphs）将所有物体和成对关系编码在单一层中，缺乏层次结构来组织大量节点，导致冗余且低效的 token 输入。层次场景图（如 TB-HSU）按功能对物体分组，虽然提供更多结构，但其层次破坏了场景的自然空间邻近性，破坏物理连贯性并引入推理歧义。另一个关键问题是推理的上下文化方法。先前工作（如 SceneGPT）采用静态、非自适应的方法，将整个未过滤的场景表示转化为每个查询的单一上下文，增加了计算成本并降低了推理准确性。
>
> 为解决这些挑战，我们提出 Sparse3DPR，一种从稀疏视角 RGB 输入进行 3D 场景理解的新型免训练框架。受人类组织场景认知机制的启发，Sparse3DPR 构建了以主导平面（如墙壁、地板、天花板）为锚点的层次化平面增强场景图（HPSG），实现结构效率和空间连贯性。在语义方面，利用预训练视觉语言模型（VLM）丰富细粒度物体的丰富概念，从而实现开放词汇能力。此外，我们引入任务自适应子图提取方法，通过动态检索 HPSG 中仅与查询相关的部分来模拟人类选择性注意力，减少上下文噪声，实现更准确和高效的特定任务推理。

## 论文总结

Sparse3DPR 提出了一种无需训练的 3D 场景理解框架，仅需稀疏 RGB 视角输入。框架核心是两个创新：(1) 层次化平面增强场景图（HPSG），以墙壁/地板/天花板等主导平面作为空间锚点组织物体，形成三级层次结构（场景类型-结构平面-物体实例）；(2) 任务自适应子图提取，基于语义相似度从 HPSG 中动态检索与查询相关的子图，为 LLM 提供精简聚焦的上下文。在 Space3D-Bench 上相比 ConceptGraphs 实现 28.7% EM@1 提升和 78.2% 加速，在 ScanQA 上达到与训练方法相当的性能。

## 核心问题

**解决什么问题：** 免训练 3D 场景理解方法在实际部署中的准确性和效率不足。

**为什么重要：** 3D 场景理解是具身 AI（机器人导航、操作）的基础能力。免训练方法因无需 3D 专用数据和训练而更具实用性，但现有方法存在两个瓶颈：
1. **场景表示质量差**：扁平场景图（ConceptGraphs）缺乏层次，节点过多导致 token 冗余；功能导向的层次场景图（TB-HSU）破坏空间连贯性。
2. **推理上下文不精准**：现有方法将整个场景图不加过滤地输入 LLM，任务无关信息淹没关键细节，既浪费计算又降低准确率。

**现有方法不足：**
- ConceptGraphs：扁平结构，token 低效，无层次组织
- TB-HSU：功能导向层次破坏空间邻近性，局限于预定义语义类别
- SceneGPT：静态上下文化，将整个场景图一次性输入 LLM

## 方法详解

### 整体框架

Sparse3DPR 分为两大阶段：(1) 层次化场景解析，从稀疏 RGB 图像构建 HPSG；(2) 任务自适应子图提取与 LLM 推理。

### 组件一：几何提取（Geometry Extraction from Sparse RGB Inputs）

- 输入：均匀采样的 $n$ 张稀疏视角 RGB 图像 $I = \{I_i\}_{i=1}^n$
- 使用 DUSt3R 进行多视图重建，推断每视角的 3D 点图 $X_i \in \mathbb{R}^{W \times H \times 3}$ 和置信度图 $C_i \in \mathbb{R}^{W \times H}$
- 通过逐元素乘积 $P_i = X_i \odot C_i$ 抑制低置信度点，生成过滤后的点云

### 组件二：结构元素提取（Structural Element Extraction）

三阶段流程提取场景的骨架结构（墙、地板、天花板）：

**Stage 1 - Mask-guided plane detection:**
- 用 SAM2 生成类别无关的分割 mask $M_i^j$
- 将 2D mask 提升到 3D：$P_i^j = X_i \odot (M_i^j \odot C_i)$
- 对每个候选点云用 RANSAC 拟合平面，得到法向量 $n_i^j$、偏移 $d_i^j$ 和内点集 $O_i^j$
- 仅保留内点比例超过 $\rho_{\text{min\_inlier}}$ 的有效平面

**Stage 2 - Multi-stage plane grouping:**
- 视内细化：在平面参数空间 (PPS) 中用 DBSCAN 聚类几何共面表面，然后通过几何感知区域增长（角度阈值 $\theta_{\text{ang}}$，距离阈值 $\delta_{\text{dist}}$）扩展碎片化区域，再次 DBSCAN 合并相邻共面片段
- 跨视图对齐：对所有视图的细化平面在 PPS 中进行全局 DBSCAN，合并同一平面的多视图观测
- 输出：全局一致的平面集合 $\Pi_{\text{global}}$

**Stage 3 - Plane semantic labeling:**
- 基于几何的语义标注：检测与重力方向对齐的平面作为地板，建立重力对齐坐标系
- 天花板：法向量与重力方向夹角小于 20 度，正偏移
- 墙壁：法向量近似垂直于地板，通过多标准过滤（面积、边界长度、至少两个不同视角的观测）

### 组件三：物体实例提取（Object Instance Extraction）

**Stage 1 - Open-vocabulary instance segmentation:**
- RAM++ 预测开放词汇类别标签
- GroundingDINO 定位候选物体区域
- SAM2 生成实例 mask
- 传播模块 $F_P$ 实现跨视图一致的实例 ID 分配

**Stage 2 - Unified semantic-geometric fusion:**
- 结合 2D mask 和 DUSt3R 的 3D 几何，DBSCAN 去噪
- 渐进式合并全局物体集：基于实例 ID 匹配或 3D IoU $\phi_{\text{geo}} > \kappa$ 的统一关联规则
- 公式：若 ID 匹配或 IoU 超阈值，合并到已有物体；否则注册为新实例

**Stage 3 - Vision-language caption generation:**
- 选择分割置信度最高的 top-5 视角，裁剪物体图像
- VLM (Qwen-VL) 生成初步描述
- LLM 精炼合并为最终 caption $c_v$、规范标签 $t^*$ 和候选标签集 $T$

### 组件四：HPSG 构建

场景图 $G = (V, E)$，节点集合 $V = \bigcup_{l=0}^{2} V_l$ 分三层：
- $V_0$：全局场景类型（如"办公室"）
- $V_1$：结构平面元素（墙、地板、天花板）
- $V_2$：物体实例

边集合 $E = \bigcup_{m=0}^{2} E_m$：
- $E_0$：场景类型到结构的默认链接
- $E_1$：结构到物体的拓扑连接（通过 3D bbox IoU 计算相似矩阵，构建最小生成树）
- $E_2$：物体间的空间关系（"on", "in", "next to"，由 LLM 根据 caption 和 3D 位置推断）

### 组件五：任务自适应子图提取（Task-Adaptive Subgraph Extraction）

1. 用 SentenceTransformer 编码所有节点 caption $\{e_i\}$ 和用户查询 $q$ 为嵌入
2. 计算查询感知评分：$S(q, e_i; \tau) = \exp\left(\frac{\mathcal{N}(F_q) \cdot \mathcal{N}(F_{e_i})}{\tau}\right)$，$\tau = 0.07$
3. 用 FAISS 检索 top-K 种子节点 $I^*$
4. 扩展一阶邻居 $\mathcal{N}(I^*)$ 和二阶邻居 $\mathcal{N}^2(I^*)$，保留对应边
5. 生成局部化子图 $G_q^* = G[I^* \cup \mathcal{N}(I^*) \cup \mathcal{N}^2(I^*)]$

### 推理流程

将提取的子图转化为文本上下文，配合 few-shot prompt 模板输入 LLM 进行问答推理。整个流程完全无需训练。

## 实验与可视化

### 实验设置

- **数据集**：
  - Replica：8 个高保真室内场景（5 办公室 + 3 房间），评估语义理解
  - ScanQA：大规模 3D VQA 基准，评估推理能力
  - Space3D-Bench：7 个场景的空间 QA 基准，评估空间推理
- **基线**：ConceptGraphs, ConceptFusion, HOV-SG, MaskCLIP 等免训练方法；3D-LLM, Scene-LLM, LL3DA, Chat-Scene 等训练方法
- **指标**：EM@1, BLEU-1~4, METEOR, ROUGE-L, CIDEr, F-mIoU, mAcc
- **关键模型**：DUSt3R-512-DPT（几何）, SAM2（分割）, RAM++ + GroundingDINO（检测）, Qwen2.5-VL-7B-Instruct（caption 和推理）, SentenceTransformer all-mpnet-base-v2（嵌入）
- **硬件**：单张 RTX 4090
- **采样**：Replica/Space3D-Bench 每场景 28 帧，ScanQA 每场景 22 帧

### 主要结果

**3D 语义理解（Replica, Table 1）：**
- Sparse3DPR 在免训练方法中取得最高 F-mIoU (39.71%)，接近训练方法 LSeg (51.54%) 和 OpenSeg (53.74%)
- mAcc 35.12%，在免训练方法中有竞争力

**3D QA（ScanQA, Table 2）：**
- EM@1: 27.22%（与训练方法 Scene-LLM 的 27.20% 持平）
- CIDEr: 88.07%（最佳）
- BLEU-4: 14.99%（最佳）
- 仅用稀疏 RGB 输入，无需点云或训练

**Space3D-Bench 消融（Table 3）：**
- 完整 Sparse3DPR (HPSG + Subgraph)：EM@1 34.68%，推理时间 0.32s
- 相比 ConceptGraphs (EM@1 20.23%, 2.15s)：EM@1 提升 28.7%，加速 78.2%
- HPSG 相比 Flat SG：EM@1 +1.94% (30.91 vs 28.97)，推理更快 (0.94s vs 1.08s)
- 任务自适应子图提取对所有 SG 类型均有显著提升

### 消融实验

**SG 类型影响（关闭子图提取）：**
- HPSG (EM@1 30.91) > Flat SG (28.97) > Affordance SG (27.17)
- HPSG 的空间连贯层次结构最适合 LLM 推理
- Affordance SG 虽然提升 fluency 但牺牲准确率

**子图提取影响：**
- 开启子图提取后，所有 SG 类型的 EM@1 和推理速度均显著提升
- HPSG + 子图提取 = 最佳组合（EM@1 34.68%, 0.32s）
- Affordance SG + 子图提取反而下降（30.78%），因为功能导向层次导致种子节点选择不准

**视角数量敏感性分析：**
- 4 视角 EM@1 27.85%，28 视角 34.68%
- 16 视角（31.91%）略优于 22 视角（31.58%），说明超过一定阈值后视角质量比数量更重要

## 相关工作

### 3D 场景表示用于 LLM 推理
- **稠密 3D 表示**（CLIP-based: OpenScene, ConceptFusion, OpenSU3D, Open-Fusion）：支持开放词汇但缺乏结构，阻碍组合推理
- **3D 场景图**：
  - 经典方法 (Armeni et al. 2019, Wald et al. 2020)：节点为物体/空间区域，边编码空间/语义关系
  - Hydra (Hughes et al. 2022, 2024)：实时层次场景图，从建筑/房间到物体/agent
  - TB-HSU (Xu et al. 2025)：功能导向层次场景图，局限于预定义类别
  - ConceptGraphs (Gu et al. 2024)：开放词汇但扁平结构
- **Sparse3DPR 区别**：HPSG 以主导平面为锚点，同时支持开放词汇和空间连贯层次

### 3D 场景理解 + LLM
- **训练方法**（Scene-LLM, LL3DA, 3D-LLM, Chat-Scene, 3D-VLP, Chat-3D v2, Grounded 3D-LLM, SpatialLM）：需要大规模 3D 数据集训练，3D 几何与语言对齐困难
- **免训练方法**（SceneGPT, ConceptGraphs, OpenSU3D）：SceneGPT 用稠密 RGB-D，静态上下文化
- **Sparse3DPR 区别**：免训练 + 稀疏 RGB + 动态子图提取

## 潜在未来工作

1. **动态环境的时间推理**：论文明确提到未来将扩展到动态环境的时间推理
2. **更多下游任务**：当前主要在 QA 上验证，可扩展到导航指令跟随、物体操作规划等
3. **减少对预训练模型的依赖**：当前依赖 DUSt3R、SAM2、GroundingDINO、Qwen-VL 等多个模型，pipeline 复杂
4. **更高效的场景图构建**：当前构建 HPSG 涉及多次 LLM 调用（caption 精炼、空间关系推断、场景类型推断），可探索更轻量的方式
5. **自适应视角选择**：敏感性分析显示视角质量比数量重要，可研究智能视角采样策略
6. **开放世界泛化**：在更多样的真实场景（室外、大规模、非结构化环境）中验证
