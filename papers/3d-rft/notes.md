# 3D-RFT: Reinforcement Fine-Tuning for Video-based 3D Scene Understanding

## 元信息
- **Authors**: Xiongkun Linghu, Jiangyong Huang, Baoxiong Jia, Siyuan Huang
- **Venue**: ICML 2026
- **arXiv**: [2603.04976](https://arxiv.org/abs/2603.04976)
- **DOI**: ...
- **开源**: [code](https://github.com/3D-RFT/3D-RFT) / [model](https://huggingface.co/EricLHK/3D-RFT)

---

## 费曼讲解

想象你在训练一个机器人看一段房间视频后回答问题："桌子在哪里？""椅子有几把？"现有的做法是 SFT（监督微调）——把标准答案喂给模型，让它逐字模仿。这就像让学生抄答案：抄得再像，也不代表真会做题。尤其当答案是一串 3D 坐标数字时，逐 token 的交叉熵损失根本不知道"预测的盒子偏了一点"和"完全预测错误"之间有多大区别——评价指标（3D IoU、F1）是连续的几何计算，但训练目标却在离散的 token 空间里优化，两者严重不对齐。

3D-RFT 的核心 idea 很直觉：既然考试用 3D IoU 和 F1 打分，那训练时也直接用这些分数当奖励信号，让模型通过强化学习"刷题"。具体分两步走：第一步，用 SFT 给模型"启蒙"——教会它基本的 3D 感知能力和输出格式（先用 `<think>` 写推理过程，再用 `<answer>` 给答案）。第二步，用 GRPO（一种不需要额外 critic 网络的 PPO 变体）做强化微调——对每个问题采样一组回答，用任务特定的可验证奖励函数打分（3D 检测用 IoU+F1，3D 定位用帧匹配+IoU，空间推理用准确率），然后让模型朝高分方向优化。

这就好比：先抄答案打基础（SFT），再刷真题冲高分（RL）。结果一个 4B 参数的小模型，在 3D 检测、定位和空间推理上全面超越了 8B 的大模型。

## 摘要翻译

> 可验证奖励的强化学习（RLVR）已成为提升大语言模型（LLM）推理能力的变革性范式，但其在 3D 场景理解领域的潜力仍未被充分探索。现有方法主要依赖监督微调（SFT），其中逐 token 的交叉熵损失作为间接代理目标，导致训练目标与任务性能之间存在错位。为弥合这一差距，我们提出了 3D-RFT（Reinforcement Fine-Tuning for Video-based 3D Scene Understanding），这是首个将 RLVR 扩展到基于视频的 3D 感知和推理的框架。3D-RFT 通过直接优化模型以匹配评估指标来转变范式。3D-RFT 首先通过 SFT 激活 3D 感知多模态大语言模型（MLLM），然后使用群组相对策略优化（GRPO）配合严格可验证的奖励函数进行强化微调。我们设计了直接源于 3D IoU 和 F1-Score 等指标的任务特定奖励函数，以提供更有效的信号来指导模型训练。大量实验表明，3D-RFT-4B 在多种基于视频的 3D 场景理解任务上达到了最优性能。值得注意的是，3D-RFT-4B 在 3D 视频检测、3D 视觉定位和空间推理基准上显著超越了更大规模的模型（如 VG LLM-8B）。我们进一步揭示了 3D-RFT 的良好特性（如鲁棒的有效性）以及关于训练策略和数据影响的有价值见解。我们希望 3D-RFT 能为 3D 场景理解的未来发展提供一个稳健且有前景的范式。

## 引言翻译

> 多模态大语言模型（MLLM）的显著成功推动了多个领域的进步，包括 3D 场景理解、机器人操作和具身导航。将 3D 场景视为视频流是一种可扩展的替代方案，相比传统的点云和深度方法，它绕过了对专用传感器的需求。通过利用广泛可用的 RGB 相机和 MLLM 的时序能力，这一范式已成为近期研究的核心焦点。虽然一些工作仍注入显式 3D 特征，但其他工作直接从视频帧中提取 3D 先验。VG LLM 验证了这种方法在跨帧检测和 3D 视觉定位等任务上的有效性。
>
> 然而，这些方法主要依赖 SFT 作为学习范式，由于仅依赖答案的监督方式，存在固有的性能天花板。具体而言，在 3D 感知任务中，模型输出是由文本浮点数序列表示的 3D 边界框。SFT 通过模仿学习优化这些序列，最小化逐 token 的交叉熵损失。这造成了关键的错位：优化发生在离散的 token 空间中，而评估在连续的 3D 坐标系统中进行。由于输出 token 必须被解码并解析为几何结构才能计算 3D IoU 等指标，标准 SFT 目标只是间接代理，无法捕捉预测的真实几何质量。
>
> 如何克服仅答案监督的固有天花板？RLVR 提供了一个有原则的解决方案，通过直接优化模型以匹配可验证奖励——这些奖励直接来源于明确的评估指标或预定义规则。与 SFT 通过逐 token 交叉熵损失约束模型模仿真实序列不同，强化学习（RL）基于标量奖励分数优化策略。这提供了与评估过程严格对齐的优越优化目标，鼓励序列探索，不受逐 token 惩罚的限制。近期的突破，如 GPT-o1 和 DeepSeek-R1，已广泛证明了 RLVR 在推进数学推理和代码生成方面的成功。
>
> 一个自然的问题是：这种指标驱动的 RL 范式能否推广到基于视频的 3D 场景理解？为此，我们引入了 3D-RFT，一个统一框架，成功地将 RL 扩展到多样化的基于视频的 3D 场景理解任务，涵盖 3D 感知和 3D 空间推理。
>
> 3D-RFT 根本性地转变了训练目标。虽然 SFT 依赖间接代理——最小化预测和真实概率之间的交叉熵损失——这导致训练目标和评估指标之间的错位。相比之下，3D-RFT 利用直接来源于可验证奖励信号（如 3D IoU、准确率）的策略梯度，确保模型被显式优化以获得最终任务性能。为克服现有 MLLM 缺乏原生 3D 感知能力的问题，我们设计了稳健的两阶段训练流程：1）SFT 预热：首先通过 SFT 向 MLLM 注入基本的 3D 感知和场景理解能力，建立稳定的策略初始化。2）RL 训练：然后使用 GRPO 算法和严格遵循评估协议的可验证奖励函数对模型进行微调。例如，在 3D 视觉定位中，我们解析预测的 9 自由度框，将其投影到全局坐标系统，并计算全局 3D IoU 作为奖励信号。这种方法有效地将学习范式从任务无关的序列模仿转变为指标驱动的策略优化。

## 论文总结

3D-RFT 提出了首个将可验证奖励强化学习（RLVR）应用于基于视频的 3D 场景理解的框架，通过两阶段训练（SFT 预热 + GRPO 强化微调），直接使用 3D IoU、F1-Score、准确率等评估指标作为奖励信号来优化模型，使得 4B 参数模型在 3D 视频检测、3D 视觉定位和空间推理任务上全面超越了 8B 基线模型。

## 核心问题

**问题**：基于视频的 3D 场景理解（检测、定位、空间推理）目前主要依赖 SFT 训练，但 SFT 的逐 token 交叉熵损失与实际评估指标（3D IoU、F1 等）之间存在严重的优化目标错位。模型在离散 token 空间被优化，却在连续 3D 坐标空间中被评估——这种"间接代理"问题导致性能天花板。

**重要性**：3D 场景理解是机器人、具身智能和 AR/VR 的基础能力。将 3D 场景视为视频流已成为趋势，但训练范式亟需升级。

**现有方法不足**：
1. SFT 的 token-level CE loss 无法反映几何质量（如 box 偏移几厘米 vs 完全错误）
2. 现有 3D MLLM 的提升主要来自数据扩展和几何特征注入，训练目标本身未被改进
3. 已有少量将 RLVR 应用于 3D 的尝试（vsGRPO、SpaceR 等），但效果有限或未经系统验证

## 方法详解

### 整体框架

3D-RFT 采用两阶段训练流程：

**Stage 1: SFT Warm Up** — 用 SFT 数据训练 3D-aware VLM，建立初始策略。模型学习：(a) 基本 3D 感知能力，(b) 结构化输出格式（`<think>...</think>` + `<answer>...</answer>`）。损失函数为标准的 negative log-likelihood：

$$\mathcal{L}_{\text{SFT}}(\theta) = -\sum_{t=1}^{T} \log \pi_\theta(\mathbf{y^*_t} \mid \mathbf{x}, \mathbf{I}, \mathbf{y^*_{<t}})$$

**Stage 2: RL Training** — 使用 GRPO 对模型进行强化微调。对每个 prompt 采样一组 $G$ 个输出，计算组内归一化的优势值，然后用策略梯度优化：

$$\mathcal{L}_{\text{GRPO}}(\theta) = -\frac{1}{\sum_{i=1}^G T_i} \sum_{i=1}^{G} \sum_{t=1}^{T_i} \mathcal{L}_{i,t}(\theta) + \beta \mathbb{D}_\text{KL}[\pi_\theta \| \pi_{\text{ref}}]$$

其中优势值通过组内奖励的均值和标准差归一化：$A_i = \frac{R_i - \text{mean}(\{R_1, \dots, R_G\})}{\text{std}(\{R_1, \dots, R_G\})}$

### 模型架构

基于 VG LLM-4B：MLLM backbone 为 Qwen2.5-VL-3B-Instruct，视觉几何 backbone 为 VGGT-1B。VGGT 特征与 Qwen 视觉特征通过逐元素相加融合。

### 可验证奖励设计

总奖励由两部分组成：**Format Reward**（格式奖励）+ **Task Reward**（任务奖励）。

**Format Reward** $R_{\text{Format}}$：检查输出是否符合 `<think>...<answer>...</answer>` 的结构化格式，有效为 1，无效为 0。

**Task Rewards 针对三个任务分别设计**：

1. **3D Video Detection**：
   - IoU Reward: 对每个预测框，找最大匹配的 GT 框计算 3D IoU，取平均：$R_{\text{IoU}}^{(\text{Det})} = \frac{1}{N} \sum_{i=1}^{N} \mathcal{I}_i$
   - F1-Score Reward: 以 $\tau_{F1}=0.25$ 为阈值判断 TP/FP/FN，计算 $R_{\text{F1}} = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$
   - 总奖励：$R_{\text{Det}} = R_{\text{IoU}}^{(\text{Det})} + R_{\text{F1}}$

2. **3D Visual Grounding**：
   - Temporal Reward: 帧索引回归，使用平滑线性衰减，容忍阈值 $\tau_{\text{frame}}=5$：$R_{\text{frame}} = \max(0, 1 - \frac{|f_{\text{pred}} - f_{\text{gt}}|}{\tau_{\text{frame}}})$
   - IoU Reward: 将预测框从局部相机坐标变换到全局坐标后计算 3D IoU
   - 总奖励：$R_{\text{Grd}} = R_{\text{frame}} + R_{\text{IoU}}^{(\text{Grd})}$

3. **3D Spatial Reasoning**：
   - Multiple Choice: 精确匹配 $R_{\text{MC}} = \mathbb{1}(y = y^*)$
   - Numerical: Mean Relative Accuracy (MRA)，在 $\{0.50, 0.55, \dots, 0.95\}$ 阈值下计算相对误差

### Loss Backward Chunking

GRPO 需要同时维护多个采样的计算图，视频+高分辨率视觉编码器导致显存爆炸。解决方案：将全局 batch 分成 $M$ 个 micro-chunk，逐 chunk 计算梯度并累积，将峰值显存从 $O(B \cdot G)$ 降到 $O(M_{\text{micro}})$。

### 训练设置

- 8x NVIDIA A100 GPU
- 3D 感知任务：full fine-tuning
- 3D 空间推理：LoRA 微调，KL 散度惩罚系数设为 0

## 实验与可视化

### 数据集

- **3D 视频检测**：ScanNetDetection（来自 EmbodiedScan，958 训练场景，243 测试场景）
- **3D 视觉定位**：ScanRefer（37K 对象定位文本-框对，562 室内扫描）
- **3D 空间推理**：VSI-298K（VSI-207K + Sr-91K，来自 VLM-3R 和 SpaceR）+ CoT-10K（Qwen3-VL-32B-Thinking 生成）
- **评估**：VSI-Bench

### 基线

VG LLM-4B/8B、Qwen2.5-VL-3B/7B、VLM-3R-7B、Cambrian-S-3B、VST-SFT/RL-3B、vsGRPO-2B/7B、SpaceR-7B、Spatial-MLLM-4B、ViLaSR-7B、SpatialLadder-3B 等。

### 主要结果

**3D 视频检测（ScanNetDetection，Tab. 1）**：
- 3D-RFT-4B vs VG LLM-4B（4 帧）：Precision +12.5%，Recall +2.5%，F1 +5.5%
- 3D-RFT-4B 超越 VG LLM-8B（4B vs 8B），F1 达 43.7 vs 41.2
- 大物体（bathtub +16.5%，table +6.9%）改善最显著

**3D 视觉定位（ScanRefer，Tab. 2）**：
- 3D-RFT-4B vs VG LLM-4B：Acc@0.25 +6.5%，Acc@0.5 +4.1%
- 3D-RFT-4B 超越 VG LLM-8B：42.9% vs 41.6%（Acc@0.25）

**3D 空间推理（VSI-Bench，Tab. 4）**：
- 3D-RFT-4B 达到 62.8% 平均准确率，全面超越所有基线
- 相比 SFT 基线 VG LLM-4B（47.3%），提升 +15.5%
- 在数值推理类别上提升尤其显著（Obj. Count 71.2，Abs. Dist. 53.5）
- 超越更大规模模型如 VLM-3R-7B（60.9%）

### 消融实验

**RFT 与 3D 先验（Tab. 3）**：
- 无论是否有 VGGT 3D 先验，SFT -> RL 均带来一致提升
- 有 VGGT：36.4% -> 42.9%（Acc@0.25）
- 无 VGGT：31.9% -> 38.2%
- 连续 SFT（SFT -> SFT）提升有限（31.9% -> 34.2%），RL 提升远超之

**CoT 数据质量影响（Fig. 4, 5）**：
- 高质量 CoT 数据（Qwen3-VL-32B-Thinking 生成）显著优于低质量 CoT（Qwen2.5-VL-72B-Instruct 生成）
- DA + 高质量 TA 数据是 RFT 成功的基础
- 仅用 DA 数据训练会导致 OOD 泛化差和不可靠的推理行为

### 训练动态（Fig. 6, 7）

- **3D 检测**：F1 持续上升，IoU reward 先升后略降（策略从几何精修转向召回最大化），表明 RFT 稳定有效
- **3D 空间推理**：约 4000 步后出现饱和迹象，因离散文本空间的反馈更粗糙

## 相关工作

1. **MLLMs for 3D Scene Understanding**：早期基于点云（3D-LLM、Chat-3D 等），近期转向视频流方案（Video-3D LLM、VG LLM、LEO-VL）。提升手段包括几何增强和数据扩展，但训练目标本身未被质疑。

2. **Reinforcement Learning for MLLMs**：RLVR 在数学/代码领域已验证成功（DeepSeek-R1、Kimi k1.5），在视频理解领域也有进展（Video-R1、VideoChat-R1），但系统性地将 RLVR 应用于 3D 场景理解的工作较少。vsGRPO 和 SpaceR 做了初步尝试，3D-RFT 是首个系统覆盖感知+推理的框架。

**本文区别**：
- 首次将 RLVR 系统性地扩展到基于视频的 3D 感知和推理
- 设计了直接源于评估指标的可验证奖励函数（IoU、F1、Accuracy）
- 揭示了 SFT 的"间接代理"问题是性能瓶颈，并用 RL 直接解决
- 提出 Loss Backward Chunking 解决 GRPO 在长视频上的显存问题

## 潜在未来工作

1. **多任务统一训练**：当前是任务独立的 RFT，如何平衡不同任务的奖励实现高效混合训练
2. **3D 感知任务的 CoT 数据**：因高质量 3D 推理标注稀缺，感知任务未使用 CoT 数据；获取此类数据并分析其影响是重要方向
3. **过程奖励（Process Reward）**：当前仅用结果奖励，3D 理解需要更强的感知能力作为推理前提，过程奖励可保证推理链的正确性
4. **小物体检测**：小物体（如 bin）改善有限，更高视觉分辨率可能有益
5. **数据质量与多样性**：CoT 数据质量对 RL 效果敏感，自动化的 CoT 数据筛选和增强值得探索
