# Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence

## 元信息
- **Authors**: Yuanyuan Gao, Hao Li, Yifei Liu, Xinhao Ji, Yuning Gong, Yuanjun Liao, Fangfu Liu, Manyuan Zhang, Yuchen Yang, Dan Xu, Xue Yang, Huaxi Huang, Hongjie Zhang, Ziwei Liu, Xiao Sun, Dingwen Zhang, Zhihang Zhong
- **Venue**: arXiv preprint (2026)
- **arXiv**: [2603.07660](https://arxiv.org/abs/2603.07660)
- **DOI**: N/A
- **开源**: [code](https://github.com/Visionary-Laboratory/Holi-Spatial) / [project page](https://visionary-laboratory.github.io/holi-spatial/)

---

## 费曼讲解

想象你有一个机器人，你想让它真正理解三维世界——不只是"识别图片里有把椅子"，而是知道"椅子在桌子的东南方向，距离1.2米"。要训练这样的能力，你需要海量的、带有精确3D标注的数据。

问题在于，现有的3D数据集极其稀缺。ScanNet这样的数据集，靠人拿着深度相机一个个房间去扫描、人工标注物体边界框，费时费力，总共也就几百个场景、50个类别。用这些有限的数据训练出来的模型，就像一个只在几间教室里上过课的学生，换到新环境就懵了。

Holi-Spatial的核心idea非常直接：既然人类标注太贵，那就让AI自动标注。具体来说，就是把一系列AI工具串联起来，形成一条全自动流水线，把普通视频流（不需要深度相机）转换成完整的3D空间标注。

这条流水线分三步走：

**第一步：几何优化。** 用Depth-Anything-V3从单目图像估计深度作为初始值，然后用3D Gaussian Splatting（3DGS）进行场景级别的几何优化。这一步就像先把草稿纸上的素描变成精确的3D模型——多视角一致性约束消除了深度图中的噪声和"浮空鬼影"。

**第二步：图像级感知。** 在优化好的3D场景中采样关键帧，让VLM（Gemini3-Pro）逐帧识别物体类别，并维护一个"类别记忆库"确保跨帧语义一致。然后用SAM3做开放词汇的实例分割，再结合3DGS渲染的深度图，把2D mask提升为3D bounding box。这里有个精巧的工程细节：直接反投影会产生边界噪声，所以他们用mask腐蚀处理2D边界误差，用mesh引导的深度滤波处理3D离群点。

**第三步：场景级精炼。** 把所有视角的检测结果合并（基于3D IoU），对齐到重力方向，然后用三级置信度规则过滤：高置信直接保留，低置信丢弃，中间地带交给VLM agent去"zoom in"重新判断。最后对确认的物体生成详细描述和空间QA对。

最终产物是Holi-Spatial-4M数据集：12K个优化后的3DGS场景，400万+空间标注，包括130万个2D mask、32万个3D框和实例描述、120万个3D grounding对、120万个空间QA对。用这个数据集微调Qwen3-VL，在ScanNet++的3D grounding上提升15% AP50，在MMSI-Bench上提升7.9%准确率。

## 摘要翻译

> 空间智能的根本在于获取大规模、细粒度的3D数据。然而，现有方法主要通过从少量人工标注数据集生成问答（QA）对来构建空间理解基准，而非从原始网页数据系统性地标注新的大规模3D场景。这导致其可扩展性受到严重制约，且这些狭隘策划的数据集中固有的领域差异进一步制约了模型性能。在本工作中，我们提出了Holi-Spatial，这是首个完全自动化、大规模、空间感知的多模态数据集，从原始视频输入构建，无需人工干预，使用我们提出的数据策划流水线。Holi-Spatial支持多层次空间监督，从几何精确的3D高斯溅射（3DGS）重建及渲染深度图，到物体级和关系语义标注，以及相应的空间问答（QA）对。遵循系统化的流水线，我们进一步构建了Holi-Spatial-4M，这是首个大规模、高质量的3D语义数据集，包含12K个优化的3DGS场景、130万个2D mask、32万个3D边界框、32万个实例描述、120万个3D grounding实例，以及120万个涵盖几何、关系和语义推理任务的空间QA对。Holi-Spatial在数据策划质量上表现出色，在ScanNet、ScanNet++和DL3DV数据集上显著超越现有的前馈方法和逐场景优化方法。此外，使用该数据集在空间推理任务上微调视觉语言模型（VLM）也带来了模型性能的显著提升。

## 引言翻译

> 空间智能是使大模型理解真实3D世界的基本桥梁。它要求大模态模型（LMM）超越以语言为中心的2D感知，发展稳健的3D空间能力，从视觉输入中感知、定位和推理3D世界。这些能力在广泛的实际应用中前景广阔，包括机器人操控与导航、场景编辑和增强现实。

> 然而，一个关键限制是原始空间数据的稀缺和不平衡。先前方法通常通过从少量人工标注的3D数据集（如ScanNet和ScanNet++）生成QA对，或通过朴素地将前馈感知模型应用于单图像数据来策划空间监督。虽然这些策略相比通用VLM有所改进，但由于依赖专业扫描硬件和人机协作标注，难以扩展，且语义覆盖有限（如ScanNet仅有50个标注类别）。

> 为解决这些限制，我们注意到相关AI工具的最新进展已超出预期；通过系统性地组合它们，我们可以构建一个自动化的空间标注引擎，甚至可以超越人工标注，实现正向数据飞轮。因此，我们提出Holi-Spatial，一个将原始视频流转换为高保真3D几何和全面语义标注的全自动框架，无需任何显式3D传感器或人机协作标注。Holi-Spatial统一了广泛的空间任务，包括3D重建、新视角合成（NVS）、深度渲染、2D实例分割、实例描述、3D边界框、3D grounding和空间QA。

> Holi-Spatial由三个阶段组成：(i) 几何优化：从单目先验（Depth-Anything-V3）初始化，在几何监督下优化3DGS场景以锐化结构并抑制浮空点。(ii) 图像级感知：采样关键帧，使用VLM推断开放词汇类别，引导SAM3在每张图像上产生高质量开放集mask。(iii) 场景级提升与精炼：通过使用渲染深度和相机内参反投影像素将2D mask提升到3D，使用恢复的相机位姿将所得点变换到世界坐标系。所得3D点作为实例候选。我们通过检查边界框IoU合并跨视角的冗余候选，并使用基于VLM的agent过滤低置信候选；对合并后的最可靠实例，生成详细描述并进一步构建grounding和QA对，用于训练VLM的3D Grounding和空间推理能力。

## 论文总结

本文提出了Holi-Spatial，一个将原始视频流全自动转换为高保真3D几何与全面空间标注的流水线，通过组合Depth-Anything-V3、3DGS几何优化、VLM语义感知和场景级精炼，构建了包含12K场景、400万+标注的Holi-Spatial-4M数据集，在3D grounding和空间推理任务上显著提升了VLM性能。

## 核心问题

**解决什么问题：** 空间智能训练数据的严重稀缺。现有空间数据集（如ScanNet）依赖专业硬件扫描和人工标注，场景数量少、类别有限（仅50类），无法支撑大规模空间理解模型的训练。

**为什么重要：** 空间智能是机器人操控/导航、AR/VR、场景编辑等应用的基础能力。数据瓶颈直接制约了模型的空间理解性能。

**现有方法不足：**
- 3D-native LMMs（如SpatialLM、LLaVA-3D）：依赖人工标注的点云/网格数据，扩展成本高
- 2D-centric spatial LMMs（如VST、Cambrian-S）：依赖少量静态3D扫描，环境多样性有限
- 3DGS-based methods（如M3-Spatial、LangSplat）：需要逐场景训练/微调，耗时且不稳定

## 方法详解

### 整体框架

三阶段流水线：Geometric Optimization -> Image-level Perception -> Scene-level Refinement，将原始视频逐步转化为完整的3D空间标注。

### Stage 1: Geometric Optimization（几何优化）

1. **SfM处理**：用COLMAP等Structure-from-Motion方法从视频流恢复相机内参和外参
2. **单目深度初始化**：使用Depth-Anything-V3 (DA3) 作为spatial foundation model生成密集点云
3. **3DGS几何优化**：将DA3深度作为先验初始化3D Gaussian Splatting，引入表面重建正则化（参考PGSR等方法）强制多视角深度一致性
4. **效果**：消除大尺度浮空点（floaters），产生干净且物理表面一致的场景表示

### Stage 2: Image-level Perception（图像级感知）

1. **关键帧采样**：从视频流均匀采样关键帧 $I = \{I_1, ..., I_T\}$
2. **VLM类别推断**：使用Gemini3-Pro逐帧生成caption，维护动态类别标签记忆 $M_t = M_{t-1} \cup \text{Extract}(I_t)$，确保跨帧语义一致
3. **SAM3实例分割**：基于记忆库prompt，SAM3产生开放词汇实例分割预测 $O_t = \{(M_k, s_k)\}_{k=1}^N$
4. **2D-to-3D OBB生成**（关键创新）：
   - 利用优化后的3DGS深度图 $D_t$，将mask内像素反投影到3D：$P = D_t(\mathbf{u}) \cdot K^{-1} \tilde{\mathbf{u}}$
   - **2D边界误差处理**：对SAM3的mask边缘进行腐蚀（erode），只保留可靠的内部区域
   - **3D离群点处理**：用多视角一致的mesh深度作为引导，过滤3DGS深度中不一致的像素
   - 从精炼后的点云估计初始3D Oriented Bounding Box (OBB)
5. **Floor-aligned OBB后处理**：检测地面推断全局上轴，重对齐每个实例OBB的roll/pitch

### Stage 3: Scene-level Refinement（场景级精炼）

1. **多视角合并**：对所有实例对，若类别相同且 $\text{IoU}_{3D}(B_i, B_j) > \tau_{\text{merge}}$（$\tau_{\text{merge}}=0.2$），则合并。保留最高置信度的源图像索引
2. **三级置信度过滤**：
   - $s_k \geq \tau_{\text{high}} = 0.9$：直接保留
   - $s_k < \tau_{\text{low}} = 0.8$：直接丢弃
   - $0.8 \leq s_k < 0.9$：交由VLM agent验证（使用zoom-in + SAM3重分割工具）
3. **实例描述与QA生成**：对最终确认的实例，用Qwen3-VL-30B生成细粒度描述，按模板程序化生成空间QA对

### 损失函数/优化目标

Stage 1的3DGS优化使用几何正则化损失（参考surface reconstruction 3DGS方法），包括：
- 渲染监督损失（RGB重建）
- 多视角深度一致性损失
- 法线一致性约束

### 训练/推理流程

数据集构建是推理阶段（使用预训练的DA3、Gemini3-Pro、SAM3、Qwen3-VL-30B）。
VLM微调阶段：用Holi-Spatial-4M的1.2M空间QA对微调Qwen3-VL，batch size 1024，1 epoch，32张NVIDIA H800 GPU。

## 实验与可视化

### 实验设置

- **框架评估数据集**：ScanNet、ScanNet++、DL3DV-10K，每个数据集随机采10个场景，人工标注2D mask和3D框作为GT
- **VLM微调评估**：MMSI-Bench、MindCube（空间推理），ScanNet++（3D grounding）
- **基线方法**：SAM3、SA2VA（2D-VLM）；SpatialLM、LLaVA-3D、SceneScript（3D-VLM）；M3-Spatial、LangSplat（3DGS-based）
- **评估指标**：Depth F1-score、2D Seg IoU、3D Det AP25/AP50、QA Accuracy

### 主要结果

**框架评估（Table 2）：**
| 指标 | Holi-Spatial | 最佳基线 | 提升 |
|------|-------------|---------|------|
| ScanNet++ Depth F1 | 0.89 | 0.39 (M3-Spatial) | +0.50 |
| ScanNet++ 3D Det AP50 | 70.05 | 6.23 (SpatialLM) | +64% |
| ScanNet++ 2D Seg IoU | 0.64 | 0.25 (SA2VA) | +0.39 |
| DL3DV Depth F1 | 0.78 | 0.23 (M3-Spatial) | +0.55 |
| DL3DV 3D Det AP50 | 52.67 | 4.38 (SpatialLM) | +48% |

**VLM微调（Table 3, 4）：**
- 空间推理：Qwen3-VL-8B + Ours 在MMSI-Bench上达32.6%（原31.1%），MindCube上达49.1%（原29.4%，+19.7%）
- 3D Grounding：Qwen3-VL-8B + Ours 在ScanNet++上AP50达27.98（基线13.50，+14.48）

### 消融实验（Table 5）

- **3DGS训练 vs 直接用DA3深度**：3DGS精炼后precision从0.13提升到0.81，recall从0.31到0.89。关键发现：DA3深度的多视角反投影产生ghosting，导致物体聚类错误
- **置信度过滤**：precision从0.35提升到0.67（减少误检），但recall从0.74降到0.69（丢失困难样本）
- **Agent召回**：恢复被置信度过滤丢弃的正确实例，最终precision 0.81、recall 0.89，达成最佳平衡

## 相关工作

- **ScanNet / ScanNet++**：经典3D场景理解数据集，依赖深度相机扫描和人工标注，Holi-Spatial在此基础上自动生成更精确的标注（见Figure 2对比）
- **VST / Cambrian-S**：2D-centric空间LLM，通过大规模SFT/RL提升空间能力，但受限于训练数据来源的多样性
- **SpatialLM / LLaVA-3D / SceneScript**：3D-native LMMs，直接消费点云/网格，扩展性差
- **M3-Spatial / LangSplat / LangSurf**：3DGS-based方法，逐场景优化语言对齐特征，耗时且不稳定
- **SAM3**：通用实例分割模型，Holi-Spatial将其与VLM和3D几何结合，实现了开放词汇的3D分割
- **SenseNova-SI-800K**：大规模空间数据集，但场景主要来源于少量静态3D扫描

**核心区别**：Holi-Spatial是首个完全自动化的、从原始视频到全面3D空间标注的流水线，不依赖人工标注或专用3D传感器，且支持最全面的任务覆盖（2D分割 + 3D检测 + grounding + spatial QA + 深度 + 重建）。

## 潜在未来工作

1. **效率优化**：自适应早停策略、基于置信度的更高效验证机制，降低逐场景优化的计算成本
2. **扩展到更多领域**：室外场景、动态场景、长视频序列的处理
3. **处理困难视频**：有限视角、运动模糊、严重遮挡、动态物体等退化情况下的鲁棒性提升
4. **不确定性估计**：对VLM生成的语义标注进行置信度校准和不确定性量化
5. **更强的基准构建**：利用流水线构建更全面的3D空间理解benchmark
6. **数据飞轮**：利用微调后的VLM反哺标注质量，形成正向循环
