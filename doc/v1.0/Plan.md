# Plan

## Guiding Principles
- 以几何与传统图像处理为主，避免引入训练成本。
- 先保证单卡、简单背景下的准确性与稳定性，再扩展复杂场景。
- 输出结构标准化，便于后续测量模块接入。
- 以可复现为优先，参数可控、可调、可记录。

## Technical Framework / Stack
- Python 3.x
- OpenCV（核心图像处理）
- NumPy（数值与几何计算）
- 可选：scikit-image（辅助滤波与轮廓处理）

## Data Model Plan
- Input: `image_path` / `image`（BGR 或 RGB）
- Output: 结构化字典 / JSON
- Output field `bbox`: 四点坐标（按顺时针排列）或旋转矩形参数
- Output field `confidence`: 0-1 浮点
- Output field `scale`: `px_per_mm` 或 `mm_per_px`
- Output field `meta`: 图像尺寸、处理耗时、参数配置

## UI / UX Plan
- 初期为 CLI：输入图片路径，输出 JSON 与可视化标注图。
- 输出可视化：保存一张标注 bbox 的结果图，便于人工核验。

## Implementation Phases
- Phase 1: 最小可用检测
- Phase 1 task: 读图与预处理（缩放、去噪、灰度化）
- Phase 1 task: 边缘检测与轮廓提取
- Phase 1 task: 轮廓筛选（面积、长宽比、矩形拟合误差）
- Phase 1 task: 输出 bbox 与简单置信度
- Phase 2: 精度与稳定性提升
- Phase 2 task: 透视校正与四点精确拟合
- Phase 2 task: 自适应阈值与光照鲁棒性
- Phase 2 task: 置信度计算优化（几何一致性 + 边缘清晰度）
- Phase 3: 标定与评估
- Phase 3 task: 像素到毫米比例计算（基于标准卡片尺寸）
- Phase 3 task: 评估脚本与误差统计
- Phase 3 task: 生成测试报告

## Definition of Done
- 在简单背景、单卡场景下稳定输出 bbox、confidence、scale。
- 有可重复的测试流程与样例输入输出。
- 生成结果可视化图用于人工核验。
- 文档齐全：使用说明、参数说明、已知限制。

## Notes
- 默认标准卡片尺寸：ISO/IEC 7810 ID-1（85.60 × 53.98 mm）。
