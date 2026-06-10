# Grounded 3D-Aware Spatial Vision-Language Modeling

## 元信息
- **Authors**: An-Chieh Cheng, Yang Fu, Yatai Ji, Ligeng Zhu, Guanqi Zhan, Zhuoyang Zhang, Zhaojing Yang, Song Han, Yao Lu, Pavlo Molchanov, Vidya Nariyambut Murali, Jan Kautz, Xiaolong Wang, Hongxu Yin, Sifei Liu
- **Affiliations**: UCSD, MIT, NVIDIA
- **Venue**: CVPR 2026 (Poster)
- **arXiv**: [2605.30307](https://arxiv.org/abs/2605.30307)
- **Project Page**: https://www.anjiecheng.me/gr3d
- **开源**: 暂无（代码和权重均标注 Coming Soon）

---

## 费曼讲解

想象你正在训练一个机器人管家。你对它说："帮我把桌上那个红色杯子拿过来。"要做到这件事，机器人需要经历一个三步推理过程：

1. **找到杯子在哪里**（在图像的哪个区域）-- 这是 2D grounding
2. **确定是哪个杯子**（是"桌子上的那个"，不是"架子上的那个"）-- 这是 implicit grounding
3. **知道杯子在真实世界中的 3D 位置**（距离你多远、多高、多大）-- 这是 3D grounding

现有的视觉语言模型（VLM）大多只能做到第一步，即显式地"指哪打哪"。但在真实世界中，很多空间问题并不是直接问"某个东西在哪"，而是像"厨房里架子上的第二个瓶子和洗衣房洗衣机上面的棕色小熊之间有多远？"这种复杂的问题。回答这类问题，模型需要在生成回答的过程中，**自动识别出文本提到的每一个物体，找到它在图像中的位置，然后才能推理它们之间的空间关系**。

GR3D 的核心 idea 就是：**把 grounding（定位）嵌入到语言生成的过程中，让模型像人类一样"边说边看"**。

具体来说，当模型在回答中提到"the second bottle"时，它会：
- 先预测出这个瓶子的 2D bounding box
- 从图像中提取这个区域的视觉特征，生成一个"region token"
- 把这个 region token 插入到正在生成的文本流中
- 继续基于文本 + 视觉证据进行推理

这就好比你在和别人解释的时候，一边说一边用手指给你看："我说的是 *这个*（指一下），然后 *那个*（再指一下），它们之间的距离大概是..."

在此基础上，GR3D 还能把 2D 定位扩展到 3D：给定一个定位好的 2D 区域，模型可以直接预测它在真实世界中的 3D bounding box（位置、大小、朝向）。这通过一种"region prompt"机制实现——把 2D 区域作为查询条件，引导模型进行 3D 推理。为了让模型能处理不同相机焦距带来的尺度差异，他们还设计了一种 intrinsic normalization 策略，把图像按焦距归一化，使得不同相机拍摄的图像在特征空间中具有一致的物体尺度。

整个方法可以用一个简洁的 pipeline 来理解：**先在 2D 平面上定位目标（Grounding），然后基于定位结果预测 3D 结构（Lifting）**。这个 "2D grounding first, then 3D" 的分解策略之所以有效，是因为 2D 定位可以利用海量的 2D 检测数据来学习强大的空间先验，然后再把这些先验迁移到 3D 任务上。

## 摘要翻译

> 我们提出 GR3D，一个集成了三种互补的 grounding 能力的空间视觉语言模型——显式 2D grounding、隐式 2D grounding 和单目 3D grounding——统一在一个框架中。GR3D 引入了一种隐式 grounding 机制，在生成过程中识别实体提及并将对应的区域 token 插入到文本流中，使模型在生成空间 chain-of-thought 回答时能够实时引用视觉证据。与此同时，一种 region-prompted 的单目 3D grounding 设计从 grounded region queries 出发，在相机视角下预测 3D bounding boxes，并由 intrinsic-aware normalization 和 dense geometric supervision 支持。这些 grounding 能力共同使 GR3D 能够将复杂的空间理解问题分解为 grounded 2D perception 加 3D inference。GR3D 在 grounded 和 non-grounded 的空间基准测试上均取得了一致的改进，证明了 grounding 作为增强 VLM 空间理解的有效归纳偏置。这些 grounding 能力整体上增强了超越 grounding 任务本身的一般空间理解。

## 引言翻译

> 视觉-语言模型（VLMs）已迅速发展为通用的感知-语言系统，能够理解场景、遵循开放式指令并支持多样化的多模态任务。随着这些模型开始成为必须在物理世界中行动、操控和导航的具身智能体的核心，它们的空间能力变得至关重要。具身智能不仅要求模型识别场景中存在什么，还需要理解物体在哪里以及它们在空间中的排列方式——这些能力对于将语言 grounding 到诸如伸手、迈步或转向等动作中至关重要。没有可靠的空间 grounding，高层指令与物理交互之间的连接就会很脆弱，限制了 VLM 向真实世界具身感知和控制的可扩展性。
>
> 空间 VLM 的快速发展极大地推动了 2D 空间理解甚至 3D 感知的进步。然而，grounding——即可靠地将语言提及与具体视觉区域关联并将 2D 证据与 3D 结构连接的能力——仍然有限。两个挑战尤其未被充分解决。(i) 隐式 2D grounding 稀缺：大多数系统支持显式的"指向 X"grounding，但缺乏在自由文本中自动检测提及实体并在生成过程中整合对应视觉证据的机制或数据。(ii) 单目 3D grounding 天然是不适定的：从单视角出发，物体的尺度、深度和内参是纠缠在一起的，而 3D 预测需要首先识别文本指的是哪个实例，然后才能估计其 3D 范围和位姿。
>
> 为解决这些限制，我们引入 GR3D，一个将 grounding 作为学习空间表示的核心机制的空间 VLM。GR3D 在统一架构中联合支持三种互补的 grounding 能力：显式 2D grounding 通过语言头以结构化文本格式预测物体区域；隐式 2D grounding 通过动态区域插入将语言提及与视觉证据关联；单目 3D grounding 通过在密集几何监督下预测 bounding boxes 和相机内参将区域理解扩展到 3D。这些机制共同建立了语言、图像区域和几何之间的细粒度对齐。

## 论文总结

GR3D 是一个空间视觉语言模型，在 NVILA-8B-Lite 基础上构建，通过三种 grounding 能力（显式 2D grounding、隐式 2D streaming region insertion、region-prompted 单目 3D grounding）统一了 2D 定位和 3D 检测。其核心创新在于"隐式 grounding"——在 CoT 推理过程中自动识别文本中的实体提及，预测对应的 2D 区域，将区域视觉 token 插入文本流中，然后基于这些 grounded visual evidence 进行后续推理。同时通过 region-prompt 机制将 2D grounding 扩展到 3D，配合 intrinsic-aware normalization 和密集点云监督实现单目 3D 检测。模型在 Omni3D 3D 检测基准上超越所有 VLM 基线和大多数视觉专家模型，在空间推理和 grounding 基准上也取得 SOTA。

## 核心问题

### 解决的问题
GR3D 试图解决空间 VLM 中两个被低估的核心问题：

1. **隐式 2D grounding 缺失**：现有空间 VLM 通常支持显式 grounding（"找到 X"），但无法在自由形式的推理过程中自动识别和定位文本提到的实体。真实世界的空间查询（如"货架上第二个瓶子和洗衣机上面的小熊之间的距离"）需要模型先定位每个提到的物体，再推理关系。

2. **单目 3D grounding 的不适定性**：从单张图像推断 3D 结构面临尺度、深度和相机内参纠缠的问题。文本引用还存在语言歧义性——需要先确定指的是哪个实例。

### 为什么重要
随着 VLM 成为具身智能体的核心（机器人操作、导航），可靠的空间理解是将高层语言指令映射到物理动作的基础。没有 grounding，"把桌上的杯子拿过来"这样的指令无法可靠执行。

### 现有方法不足
- 大多数 VLM 只支持显式 grounding，缺乏隐式机制
- 现有 3D 检测方法（如 DetAny3D）绕过了中间的 2D localization 步骤
- 多视角方法依赖多视角监督，单目场景下不适用
- 相机内参处理不当：Qwen3-VL 对输入分辨率高度敏感，VST 虽然做了类似归一化但仍需将 FoV 作为文本 prompt

## 方法详解

### 整体框架

GR3D 基于 NVILA-8B-Lite 架构构建，包含以下主要组件：

```
输入图像 -> SigLIP 视觉编码器 -> MLP Projector -> Qwen-2-7B LLM
                                          |
                              Spatial PE (空间位置编码)
                                          |
                              Region Encoder (区域编码器)
                                          |
                              Streaming Region Insertion
```

训练分两个阶段：
- **Stage 1: Spatial Pretraining** — 加强空间理解和 2D grounding 能力
- **Stage 2: Detection CoT Finetuning** — 微调 CoT 格式的检测数据

### 2.1 基础空间 VLM

**单视角设置**：SigLIP 编码器从 RGB 图像中提取 dense visual tokens，每个 token 用 2D positional embeddings（来自像素坐标和相对深度线索）增强，使其同时携带外观和几何上下文。区域可以通过 bounding box 内的 pooling 编码为单独的 query token（继承自 SR-3D 的 region-prompt 设计）。

**多视角设置**：所有图像 token 通过深度和像素位置线索映射到统一的空间特征空间。第一视角作为参考坐标系，后续视角变换到第一帧坐标系。

### 2.2 显式 2D Grounding

给定自然语言指令，模型直接在语言输出中以 HTML 风格文本格式预测 2D bounding box（如 `<bbox>[x1, y1, x2, y2]</bbox>`）。不需要额外的检测分支，使用标准语言生成头。

### 2.3 隐式 2D Grounding（核心创新）

**动机**：考虑一个复杂的空间推理问题："厨房里架子上的第二个瓶子和洗衣房洗衣机上的棕色小熊有多远？"人类首先会定位每个提到的物体，然后才推理它们的空间关系。GR3D 的隐式 grounding 机制显式引入了这个中间步骤。

**Streaming Region Insertion 机制**：

1. 模型以 CoT 方式生成回答
2. 当提到一个实体（如 "the second bottle on the shelf"）时，模型先预测对应的 2D bounding box $[x_1, y_1, x_2, y_2]$
3. 立即通过 region encoder 编码该图像区域，得到一个 region token
4. 将该 region token **直接插入到文本流的当前位置**
5. 后续生成同时以文本上下文和视觉证据为条件
6. 对后续提到的每个实体重复此过程

**训练范式**：
- Bounding box 坐标作为文本输出的一部分，通过 teacher forcing 优化
- 坐标预测后，从 ground-truth 区域提取 region token，插入生成流
- Region token 从计算图中 detach（无梯度流过），但作为后续 token 预测的强条件线索

**推理范式**：
- 完全自回归：模型预测坐标 -> 编码预测区域得到 embedding -> 插入序列 -> 继续生成
- 后续推理（关系比较、距离估计）基于文本上下文和动态插入的 region evidence

**与两阶段方法的对比**：可以抽象为"先用 VLM grounding 实体，然后用带 region encoder 的空间 VLM 进行 region-conditioned reasoning"的两步过程。但 GR3D 在单一流中统一了两个阶段，模型根据语言上下文学习何时以及 ground 什么，推理自然地基于 grounded evidence 展开。

### 2.4 单目 3D Grounding

**Region-prompt Formulation**：给定一个定位好的 2D 区域，将其作为空间查询进行 3D 推理。Region 的视觉特征被 pooling 并编码为 region token，融合到文本流中引导 3D box 预测。

**3D Box 表示**：统一的语言化格式，参数化为：
- 中心 $(x_c, y_c, z_c)$
- 尺寸 $(w, h, l)$
- 朝向 $(\theta_p, \theta_r, \theta_y)$（归一化的欧拉角 pitch/roll/yaw）

为确保数据集间一致性，选择使 region 局部 PCA 轴与全局坐标轴偏差最小的旋转变体。

**Intrinsic Normalization（内参归一化）**：给定焦距 $f_x$，按以下方式归一化图像尺寸：

$$W' = \frac{1000}{f_x} \cdot W, \quad H' = \frac{1000}{f_x} \cdot H$$

这使得不同焦距的相机在特征空间中具有一致的物体表观大小，无需显式回归内参。

**多源监督信号**：

1. **Region -> 3D**：有 2D box 时，从 region prompt 直接预测 3D box
2. **Text -> 3D**：无 2D box 时，通过内置文本 grounding 定位实体后回归 3D box
3. **Dense Point Supervision**：从 ground-truth 或预测的深度图中，每张图像随机采样 100 个有效表面点，训练模型预测其 3D 坐标（基于 region prompt 条件）。这种 depth-driven 信号将监督扩展到远超有限的 3D box 标注。
4. **2D Box Augmentation**：对 bounding box 施加轻量 jitter（大小和位置），提高鲁棒性。

### 2.5 数据构建

**隐式 Grounding 语料**：
- 起始于 RefSpatial（包含 OpenImages 2D 样本、CA-1M 3D 视频数据、合成场景）
- 用 Florence-2 为每个文本提及生成候选 2D bounding box 和类别标签（产生密集但有噪声的标注）
- 通过 VLM 验证和重述管线精炼：(1) 验证文本提及和检测区域的一一对应，(2) 将通用类别名重写为简洁的实例级描述

**显式 Grounding 数据**：对含有 ground-truth box 的样本，用 VLM 生成短的实例级指代表达并验证。

**训练数据组成**（全部公开数据）：
- 97K grounded CoT 样本
- 780K 3D 检测样本（Omni3D + EmbodiedScan）
- 272K pointmap 重建样本（DepthLM）

### 2.6 训练细节

**Stage 1（Spatial Pretraining）**：
- 初始化：视觉编码器、projector、LLM 来自 NVILA-Lite 8B，spatial PE 新初始化
- 视觉编码器冻结，其余模块训练
- AdamW，base lr $5 \times 10^{-5}$，warmup ratio 0.03，cosine scheduler
- 约 4 天，8 节点 A100

**Stage 2（Detection CoT Finetuning）**：
- 仅微调 LLM（Qwen-2-7B）
- lr $1.5 \times 10^{-5}$
- 约 4 小时，同样 8 节点 A100

**架构**：SigLIP 视觉编码器，输入分辨率 448，patch size 14，Qwen-2-7B LLM backbone。动态 tiling，最多 12 tiles/图像。

## 实验与可视化

### 数据集与基准

- **3D 检测**：Omni3D benchmark（包含 SUN-RGBD、ARKitScenes、Objectron、HyperSim、KITTI、nuScenes 六个子集）
- **2D 检测**：Omni3D 2D 投影
- **空间推理**：CVBench、BLINK-Depth、ERQA、SAT、RealWorldQA、EMBSpatial
- **通用 VQA**：ChartQA、MME、POPE、AI2D
- **Grounding CoT**：MM-GCoT（AccA、AccG、Consistency 三个指标）
- **2D 指代**：RefCOCO/RefCOCO+/RefCOCOg
- **多视角**：VSI-Bench、ScanRefer、ScanQA、MMSI-Bench、SPAR-Bench
- **空间指代**：RefSpatial

### 主要结果

**3D 检测（Omni3D, Table 1）**：

| 方法 | SUN-RGBD AP3D | ARKit AP3D | Obj. AP3D | HyperSim AP3D | KITTI AP3D | nuScenes AP3D | Avg mAP |
|------|------|------|------|------|------|------|------|
| Cube R-CNN | - | - | - | - | - | - | 23.26 |
| DetAny3D | 26.62 | 59.55 | 72.51 | 11.43 | 44.28 | 41.01 | 24.92 |
| Qwen3-VL-4B | 28.28 | 63.97 | 61.60 | 11.56 | 17.39 | 7.48 | - |
| Qwen3-VL-8B | 28.28 | 62.32 | 61.63 | 11.62 | 5.23 | 11.52 | - |
| **GR3D-8B** | **43.49** | **67.49** | **71.68** | **16.42** | **22.18** | **22.98** | **25.40** |

GR3D 在室内场景上大幅领先，特别是 SUN-RGBD 上从 28.28 提升到 43.49（+15 AP）。

**2D 检测（Omni3D, Table 2）**：GR3D 在所有 6 个子集上均超越 Cube R-CNN 和 Qwen3-VL-8B。

**空间 VQA（Table 3）**：
- Stage 1 空间预训练后，BLINK-Depth 从 73.38 -> 87.90，CVBench 显著提升
- Stage 2 CoT 微调后，通用 VQA 基本保持

**BLINK-Depth**：94.4%（超越 SpatialRGPT-8B 的 87.9% 和 SR3D-8B 的 90.3%），且不需要手动标注 mask

**MM-GCoT（Table 4）**：

| 方法 | Obj. AccA | Obj. AccG | Obj. Cons. | Avg AccA | Avg AccG | Avg Cons. |
|------|------|------|------|------|------|------|
| LLaVA-GCoT-7B | 62.3 | 61.7 | 61.3 | 74.5 | 63.3 | 58.1 |
| **GR3D-8B** | **71.1** | **65.7** | **66.1** | **78.3** | **74.2** | **67.7** |

**RefSpatial（Table 6）**：LOCATION 63.0（vs. RoboRefer-8B 52.0），PLACEMENT 50.0，UNSEEN 41.5

**RefCOCO/+/g（Table 8）**：与 InternVL3.5-8B、Qwen2.5-VL-7B 等顶级 VLM 持平，接近 Grounding-DINO 等视觉专家模型

**多视角 VSI-Bench（Table 7）**：平均 67.6（vs. SR-3D-8B 62.9），在所有子任务上全面超越

### 消融实验（Table 5）

| 2D->3D | Pretrain | Cam Norm | AP$_{15}^{sun}$ | AP$_{3D}^{sun}$ | AP$_{15}^{kit}$ | AP$_{3D}^{kit}$ |
|--------|----------|----------|----------|----------|----------|----------|
| - | - | - | 30.19 | 20.27 | 10.08 | 6.22 |
| ✓ | - | - | 42.29 | 29.87 | 15.61 | 10.03 |
| ✓ | ✓ | - | 41.24 | 30.95 | 21.55 | 14.35 |
| ✓ | ✓ | ✓ | 43.49 | 31.64 | 22.18 | 14.75 |

关键发现：
1. **2D->3D 分解是最大的提升来源**：直接 3D 预测 vs. 先 grounding 再 3D，SUN-RGBD AP3D 从 20.27 -> 29.87（+9.6）
2. **空间预训练对室外场景特别有效**：Omni3D 室外样本少，2D 空间先验帮助迁移，KITTI AP15 从 15.61 -> 21.55
3. **内参归一化提供稳定的小幅改进**

**Pointmap 监督的 Scaling 行为（Fig. 5）**：增加 pointmap 数据比例持续提升 3D 检测性能，显示 dense geometric supervision 的可扩展性。

### 推理延迟（Supp. Table）

| 方法 | 延迟 (s) |
|------|------|
| DetAny3D | 0.98 |
| VST-7B | 2.76 |
| Qwen3-VL-8B | 3.23 |
| **GR3D-8B** | **2.72** |

GR3D 在 VLM 中最快（得益于更高效的 dynamic tiling vision encoder），每次 region insertion 额外仅 0.01s。

## 相关工作

### 空间 VLM
- **SpatialVLM / SpatialPin / VST / SpatialLadder**：聚焦 2D 平面上的空间关系（相对位置、方向、距离）
- **SpatialRGPT**：引入 region branch 做更精细的 region-level 查询
- **SR-3D**（本文直接前作）：扩展到多视角，通过统一 visual token space 连接 2D 和 3D
- **GR3D 的区别**：同时解决隐式 2D grounding 和单目 3D grounding，推理时不需要任何空间标注

### 单目 3D Grounding
- **Cube R-CNN / Omni3D**：多数据集联合训练的通用检测器，但限于预定义类别
- **OVMono3D**：两阶段 "detect-then-lift" pipeline
- **DetAny3D**：promptable 架构，融合 2D foundation model 特征
- **GR3D 的区别**：在统一 VLM 框架中预测 3D box，同时包含动态隐式 2D grounding，grounding 作为增强一般空间对齐和几何一致性推理的关键驱动

### Thinking with Images
- **MM-ReAct / ViperGPT / Visual Sketchpad** 等：通过外部工具或中间视觉表示增强推理
- **GR3D 的区别**：避免显式视觉思维过程和外部工具，通过隐式 2D grounding 和原生 3D 推理在 VLM 生成流中无缝集成

## 潜在未来工作

1. **代码与模型开源**：项目页面标注 Coming Soon，开源后可推动社区复现和改进
2. **更大规模 3D 数据集**：作者指出 Omni3D 覆盖的环境、相机配置和物体类别有限，更大更多样的 3D 数据集将进一步提升性能
3. **多视角与具身推理扩展**：论文展示了多视角扩展的初步结果（VSI-Bench），可进一步扩展到视频流和具身场景中的连续空间推理
4. **推理速度优化**：相比视觉专家模型仍有延迟差距，可通过蒸馏、量化或更高效的 3D 表示来加速
5. **与 VLA 模型结合**：作者已有 NaviLa 等具身导航工作，将 GR3D 的空间 grounding 能力引入 vision-language-action 模型是一个自然方向
6. **更复杂的隐式 grounding 场景**：当前主要在相对简单的实体提及上验证，可扩展到更复杂的多步空间推理（如导航路线规划、遮挡推理等）
7. **Intrinsic estimation 集成**：论文显示使用 GeoCalib 估计焦距仅有 1.2 mAP 的下降，可进一步将 intrinsic estimation 端到端集成到模型中
