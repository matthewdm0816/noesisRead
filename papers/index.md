# 论文阅读索引

> 更新时间：2026-05-23

## 已完成分析

| # | 论文 | Venue | 一句话总结 | 开源状况 |
|---|------|-------|-----------|---------|
| 1 | [Proxy3D](proxy3d-efficient-3d-representations/notes.md) | CVPR 2026 | 语义感知聚类将 3D 场景压缩为少量 proxy token，700 token 达到 8000 token 方法的性能 | 完整开源（代码+数据+模型） |
| 2 | [S²-MLLM](s2-mllm-spatial-reasoning-3d-grounding/notes.md) | CVPR 2026 | 训练时隐式学习 3D 结构，推理时零额外开销完成 3D 视觉定位 | 代码开源 |
| 3 | [GS-Reasoner](reasoning-in-space/notes.md) | ICLR 2025 | 双路径池化构建语义-几何混合表示，首个无外部模块的自回归 3D 定位 LLM | 全面开源（代码+模型+数据集） |
| 4 | [OmniEVA](omnieva/notes.md) | ICLR 2026 | 任务自适应 3D 门控路由器 + 具身感知 GRPO，8B 参数在 7/8 具身推理基准 SOTA | 代码 coming soon |
| 5 | [Vid-LLM](vid-llm/notes.md) | ICLR 2026 | 单目视频输入的紧凑 3D-MLLM，跨任务适配器耦合重建与推理 | GitHub placeholder，代码 coming soon |
| 6 | [MSSR](minimal-sufficiency/notes.md) | ICLR 2026 | 双智能体框架构建最小充分信息集，解决 3D 空间推理中感知不足+冗余干扰 | 代码已开源 (MIT) |

## 待分析 — PDF 暂不可用

| # | 论文 | Venue | 摘要要点 | 状态 |
|---|------|-------|---------|------|
| 7 | AffIn-Space | ICML 2026 | 仿射不变表示解决 MLLM 空间推理的视角脆弱性 | 无 arXiv，无公开 PDF |
| 8 | PV-Ground | CVPR 2026 | 文本引导点-体素交互，ScanRefer +5.1% | CVPR 2026 未开幕，6 月后公开 |
| 9 | ORD | CVPR 2026 | 对象-关系解耦用于泛化 3D 视觉定位 | CVPR 2026 未开幕，6 月后公开 |
| 10 | EG-3DVG | CVPR 2026 | 表达感知 + 几何感知解码器用于 3D 视觉定位 | CVPR 2026 未开幕，6 月后公开 |
| 11 | Merge3D | CVPR 2026 | 2D-3D 联合 token 合并，70% token 压缩 + 3x 加速 | CVPR 2026 未开幕，6 月后公开 |
| 12 | GR3D | CVPR 2026 | 统一显式/隐式 2D grounding 和单目 3D grounding 的空间 VLM | CVPR 2026 未开幕 |
| 13 | DSGCR | 未知 | 分解谱几何感知跨模态语义表示用于 3D 视觉定位 | 未在任何数据库找到 |

---

**说明**：
- 5 篇 CVPR 2026 论文将在 2026 年 6 月 6 日 CVPR 开幕后通过 CVF Open Access 获取
- AffIn-Space 为 ICML 2026 poster，需等待会议公开
- DSGCR 在所有主流学术数据库均未检索到，建议确认标题
