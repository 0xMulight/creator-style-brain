# 🧠 Creator Style Brain · 创作风格脑

把**自己授权的**历史短帖/文案整理成一份风格手册，之后交给 Grok Bot、Hermes 或其他 AI 参考。

**不是只写一段提示词**：附带可运行的 Python 分析器、草稿比对和复用提示词生成器。默认完全离线。

## Windows 10 快速体验

1. 安装 Python 3.10+；下载 ZIP 解压。
2. 把本人作品的 `.txt` / `.md` 文件放入 `examples/samples/`，每篇一个文件。
3. 双击 `启动工具.bat`，选择 `1`，生成 `reports/style-guide.md` 和 `reports/style-profile.json`。
4. 选择 `2` 可以检查一篇草稿；选择 `3` 生成复制给 Bot 的风格提示词。

命令行示例（可选）：

```bash
python -m creator_style_brain analyze --input examples/samples --output reports
python -m creator_style_brain check --profile reports/style-profile.json --draft examples/draft.txt
python -m creator_style_brain prompt --profile reports/style-profile.json
python -m unittest discover -s tests -v
```

## 能做 / 不能做

- ✅ 统计开头习惯、段落长度、问号、感叹号、emoji、模板词，并生成手册。
- ✅ 检查长段落、空泛套话等可解释的写作问题。
- ✅ 生成能复用的 Bot 提示词；不上传任何账号数据。
- ❌ 不自动读取你的 X 账号、历史私信或记忆。
- ❌ 不会仅凭三篇文案“训练”出完全懂你的 AI；没有真正的模型微调。
- ❌ 不能判断句子事实真假或保证流量。

**Grok Bot 使用**：把手册正文发给 Bot，要求按它写一篇测试稿，满意后在 Bot 内保存为 Skill。能否直接执行 Python 取决于 Bot 的运行环境；不要默认 GitHub 仓库代码已经在云端安装。

开源协议：MIT · 作者：[@0xMulight](https://github.com/0xMulight)
