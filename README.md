# taobao-lookbook-generator

淘宝服饰 Lookbook 生图 Codex Skill。根据授权成年模特、商品正反面与细节、完整穿搭参考，生成16张3:4成片，并与 `taobao-lookbook-reviewer` 配套完成逐张审核与有限返工。

## 在 Codex 聊天窗口安装

把下面一整句话发送给 Codex：

```text
请使用 $skill-installer 从 https://github.com/znnw4m6k7k-dotcom/taobao-lookbook-generator/tree/main/taobao-lookbook-generator 安装；安装成功后读取 ~/.codex/skills/taobao-lookbook-generator/references/使用说明-中文.md，并在当前聊天窗口给我一份完整中文说明书和首次使用示例。
```

安装成功后，Skill 会在下一轮对话可用。建议同时安装配套审图 Skill：`taobao-lookbook-reviewer`。

## 终端安装方式

如果需要手动使用 Codex 的标准安装器：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo znnw4m6k7k-dotcom/taobao-lookbook-generator \
  --path taobao-lookbook-generator
```

如果目标目录已经存在，标准安装器会停止，不会覆盖旧版本。

## 使用说明

安装后的中文说明位于：

```text
~/.codex/skills/taobao-lookbook-generator/references/使用说明-中文.md
```
