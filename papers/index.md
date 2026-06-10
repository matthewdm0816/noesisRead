# 论文阅读索引

> 更新时间：2026-06-10

## 已完成分析

| # | 论文 | Venue | 一句话总结 | 开源状况 |
|---|------|-------|-----------|---------|
| 1 | [Proxy3D](proxy3d-efficient-3d-representations/notes.md) | CVPR 2026 | 语义感知聚类将 3D 场景压缩为少量 proxy token，700 token 达到 8000 token 方法的性能 | 完整开源（代码+数据+模型） |
| 2 | [S²-MLLM](s2-mllm-spatial-reasoning-3d-grounding/notes.md) | CVPR 2026 | 训练时隐式学习 3D 结构，推理时零额外开销完成 3D 视觉定位 | 代码开源 |
| 3 | [GS-Reasoner](reasoning-in-space/notes.md) | ICLR 2025 | 双路径池化构建语义-几何混合表示，首个无外部模块的自回归 3D 定位 LLM | 全面开源（代码+模型+数据集） |
| 4 | [OmniEVA](omnieva/notes.md) | ICLR 2026 | 任务自适应 3D 门控路由器 + 具身感知 GRPO，8B 参数在 7/8 具身推理基准 SOTA | 代码 coming soon |
| 5 | [Vid-LLM](vid-llm/notes.md) | ICLR 2026 | 单目视频输入的紧凑 3D-MLLM，跨任务适配器耦合重建与推理 | GitHub placeholder，代码 coming soon |
| 6 | [MSSR](minimal-sufficiency/notes.md) | ICLR 2026 | 双智能体框架构建最小充分信息集，解决 3D 空间推理中感知不足+冗余干扰 | 代码已开源 (MIT) |
| 7 | [APEIRIA](apeiria/notes.md) | ICML 2026 | 三阶段课程蒸馏神经符号推理模式到 3D MLLM，统一符号系统性推理与 LLM 灵活性 | 完整开源（代码 CC-BY-4.0 + 模型） |
| 8 | [EG-3DVG](eg-3dvg/notes.md) | CVPR 2026 | 表达感知(PECA)+几何感知(GMA)解码器+对比学习(ECL)，解决 3D VG 三大挑战 | GitHub placeholder，代码未发布 |
| 9 | [GR3D](grounded-3d-aware-spatial-vlm/notes.md) | CVPR 2026 | 统一显式/隐式 2D grounding 和单目 3D grounding 的空间 VLM，"先定位再推理" | 代码 Coming Soon |
| 10 | [Merge3D](merge3d/notes.md) | CVPR 2026 | 2D 语义+3D 几何乘积融合 token 压缩，70% 压缩率保持强劲性能 | 代码 Coming Soon |
| 11 | [ORD](ord/notes.md) | CVPR 2026 | 对象-关系解耦框架，抑制语义泄漏实现泛化 3D 视觉定位 | 暂未开源 |
| 12 | [PV-Ground](pv-ground/notes.md) | CVPR 2026 | 文本引导点-体素交互+可微关键点采样，ScanRefer +5.1% | GitHub 已公布，代码准备中 |
| 13 | [3D-DRES](3d-dres/notes.md) | AAAI 2026 | 短语级 3D 实例分割新任务+DetailRefer 数据集(54K 描述) | 代码已开源 |
| 14 | [Sparse3DPR](sparse3dpr/notes.md) | AAAI 2026 | 稀疏 RGB 视角免训练 3D 场景解析，层次场景图+任务自适应子图推理 | 暂未开源 |
| 15 | [MRPD](multimodal-robust-prompt-distillation/notes.md) | AAAI 2026 | 三模态教师蒸馏轻量 prompt 提升 3D 点云对抗鲁棒性，推理零开销 | 代码已开源 |
| 16 | [3D-RFT](3d-rft/notes.md) | ICML 2026 | RLVR 首次应用于视频 3D 理解，4B 模型全面超越 8B 基线 | 代码+模型已开源 |
| 17 | [KeyVT](zero-shot-3d-qa/notes.md) | ICML 2026 | 分层视角选择+最优传输 token 压缩，零样本 3D 问答接近训练方法 | 代码已开源 |
| 18 | [Holi-Spatial](holi-spatial/notes.md) | arXiv | 全自动视频流→3D 标注流水线，400 万+标注大规模空间数据集 | 代码已开源 |

## 待分析 — PDF 暂不可用

| # | 论文 | Venue | 摘要要点 | 状态 |
|---|------|-------|---------|------|
| 19 | AffIn-Space | ICML 2026 | 仿射不变表示解决 MLLM 空间推理的视角脆弱性 | 无 arXiv，无公开 PDF |
| 20 | DSGCR | 未知 | 分解谱几何感知跨模态语义表示用于 3D 视觉定位 | 未在任何数据库找到（三轮搜索均未果） |
| 21 | 3D-DLP | ICML 2026 | 自监督 3D 物体中心场景表示学习 | ICML proceedings 未发布，无 arXiv |
| 22 | 3D Scene Assertion Verification | ICML 2026 | 3D 场景断言验证 | 未在任何数据库找到 |

---

**说明**：
- AffIn-Space 为 ICML 2026 poster，需等待会议公开 PDF
- DSGCR 在所有主流学术数据库均未检索到（三轮搜索），建议确认标题
- 3D-DLP 为 ICML 2026，proceedings 尚未发布
- 3D Scene Assertion Verification 未找到公开版本
