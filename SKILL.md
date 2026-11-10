---
name: creator-style-brain
description: Analyze authorized writing samples locally, extract reproducible style metrics, generate an editable style guide, and check future drafts. Use when a creator wants their own repeatable voice.
license: MIT
compatibility: Python 3.10+; Windows 10/macOS/Linux; local command execution only
metadata:
  author: "0xMulight"
  version: "1.0.0"
---

# Creator Style Brain

## 使用时机

用户希望用自己授权的历史作品提取风格、给草稿做风格检查，或把写作习惯固化为可复用说明。

## 所需输入

- 1篇以上本人或有明确使用授权的 `.txt` / `.md` 作品（建议5篇以上）。
- 可选的待修改草稿。
- 电脑/执行环境需 Python 3.10+，否则只用纯文本规则人工完成。

## 执行步骤

1. 明确作品来源与授权；涉及隐私先提醒用户脱敏。
2. 在**项目根目录**执行 `python -m creator_style_brain analyze --input examples/samples --output reports`。
3. 读取 `reports/style-guide.md`，请用户确认“不喜欢的词”和开头习惯。不能把统计数据伪装成模型推断。
4. 如提供草稿，执行 `python -m creator_style_brain check --profile reports/style-profile.json --draft examples/draft.txt`，输出需修改位置。
5. 若要给 Bot 复用，执行 `python -m creator_style_brain prompt --profile reports/style-profile.json`，把提示词**文本**交给 Bot。
6. 用一篇新稿做人工A/B校验，记录用户调整意见，再更新风格手册。

## 验收

- 输出文件存在且不为空；报告开头样例确实取自提供的作品。
- 不编造作者经历或受众数据，不直接复制外部创作者的个人表述。
- 不自动发布、联网、保存私人数据到云端；未安装Python时不要宣称脚本已运行。

