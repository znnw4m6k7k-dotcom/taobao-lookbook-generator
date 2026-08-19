# Taobao Lookbook Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

为淘宝服饰商品生成专业 Lookbook 图片的 AI Agent Skill。支持标准模式、高级模式和自定义场景模式。

Generate professional Taobao apparel lookbook images with AI. Supports standard, premium, and custom scene modes.

## 功能特点 | Features

✨ **三种生成模式**
- 标准模式：12张棚拍 + 4张街拍，适合常规商品
- 高级模式：16-20张图片，5次重试，适合主推款
- 自定义场景模式：基础棚拍 + 用户提供的场景背景

🎯 **精确特征锁定**
- 自动从参考图提取详细的人物、服装、造型特征
- 三锁系统（identity_lock / product_lock / styling_lock）确保一致性

🔄 **自动审核与重试**
- 每张图自动评级（A/B/C）
- B/C级图片自动重试（标准3次，高级5次）
- A级图片自动进入交付目录

💰 **成本控制**
- 生成前预估成本
- 支持设置预算上限
- 实时追踪实际花费

## 安装 | Installation

### 前置条件

- [Codex](https://codex.anthropic.com) 已安装
- 推荐同时安装 `taobao-lookbook-reviewer` skill

### 在 Codex 聊天窗口安装（推荐）

把下面一整句话复制粘贴到 Codex 聊天窗口：

```text
请使用 $skill-installer 从 https://github.com/znnw4m6k7k-dotcom/taobao-lookbook-generator 安装；安装成功后读取 ~/.codex/skills/taobao-lookbook-generator/references/使用说明-中文.md，并在当前聊天窗口给我一份完整中文说明书和首次使用示例。
```

安装成功后，Skill 会在下一轮对话可用。建议同时安装配套审图 Skill：`taobao-lookbook-reviewer`。

### 手动安装

```bash
cd ~/.codex/skills/
git clone https://github.com/znnw4m6k7k-dotcom/taobao-lookbook-generator.git
```

## 快速开始 | Quick Start

### 准备素材

1. **模特参考图**：正面、侧面、背面（已授权的成年模特）
2. **商品图**：正面、背面、细节图
3. **完整造型图**：包括鞋子和配饰的完整穿搭
4. **商品信息**：SKU、颜色、类型（连衣裙/上装/下装/套装/外套）

### 标准模式

```text
使用 $taobao-lookbook-generator，根据这个素材文件夹生成16张3:4淘宝 Lookbook。
```

生成 12张棚拍 + 4张街拍，自动审核和重试。

### 高级模式

```text
使用 $taobao-lookbook-generator 高级模式，生成20张 Lookbook（16棚拍+4街拍），最多5次重试。
```

适合主推款和重要营销活动。

### 自定义场景模式

```text
使用 $taobao-lookbook-generator 自定义场景模式：
1. 先生成16张标准棚拍图
2. 然后使用场景背景图（scenes/cafe.jpg 和 scenes/plaza.jpg），每个场景8张
3. 保持模特、服装、姿势一致，只替换背景
```

适合品牌专属场景和多平台内容需求。

## 输出说明 | Output

### 标准/高级模式

```
job_folder/
├── final/                    # A级成品图（16-20张）
│   ├── ST-FRONT-01.jpg
│   ├── ST-FRONT-02.jpg
│   └── ...
├── human-review/             # 未通过审核的图片（如有）
├── job-manifest.json         # 完整任务记录
└── cost-log.json            # 成本统计
```

### 自定义场景模式

```
job_folder/
├── final/
│   ├── studio/              # 16张基础棚拍图
│   ├── cafe_interior/       # 场景1（如8张）
│   └── city_plaza/          # 场景2（如8张）
├── human-review/
│   ├── studio/
│   └── city_plaza/
├── job-manifest.json
└── cost-log.json
```

## 配置选项 | Configuration

创建 `job-config.json` 自定义参数：

```json
{
  "sku": "PRODUCT-SKU-001",
  "color": "powder blue",
  "product_type": "dress",
  "mode": "standard",
  "shot_count": 16,
  "max_retry_rounds": 3,
  "budget_cap_usd": 50,
  "custom_scenes": []
}
```

详细配置说明见 [references/configuration-options.md](references/configuration-options.md)

## 成本估算 | Cost Estimation

- **标准模式**：16张 × 1.5倍（含重试） ≈ $24
- **高级模式**：20张 × 1.5倍 ≈ $30
- **自定义场景模式**：
  - 基础：16张 × 1.5倍 ≈ $24
  - 每个场景：8张 × 1.3倍 ≈ $10-11

按每张生成约 $1.00 计算（实际费用取决于使用的图像生成服务）

## 文档 | Documentation

- 📖 [完整使用说明（中文）](references/使用说明-中文.md)
- 📖 [English User Guide](references/user-guide-en.md) *(coming soon)*
- 🔧 [配置选项](references/configuration-options.md)
- 🔄 [自定义场景工作流](references/custom-scene-workflow.md)
- 📋 [完整工作流程](references/workflow-stages.md)
- 🎨 [特征提取指南](references/feature-extraction-guide.md)
- ✅ [审核规范](references/reviewer-spec.md)

## 常见问题 | FAQ

**Q: 生成过程中需要人工介入吗？**

A: 通常无需介入，全自动运行。只有在素材不足或超出预算上限时才会请求确认。

**Q: 如果图片未通过审核怎么办？**

A: 系统会自动重试（标准模式3次，高级模式5次）。重试后仍未通过的图片会放入 `human-review/` 目录。

**Q: 支持哪些商品类型？**

A: 连衣裙、上装、下装、套装、外套。每个 SKU 和颜色需要单独任务。

**Q: 自定义场景模式的背景图有什么要求？**

A: 
- 分辨率：至少2000px宽，建议2400px+
- 格式：JPG或PNG
- 内容：前景空白区域，适合放置全身模特
- 光照：明确的光源方向
- 禁止：背景中有人物、过于杂乱

## 更新日志 | Changelog

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新记录。

## 许可证 | License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢 | Acknowledgments

本 Skill 基于 Claude Agent SDK 构建，依赖 `taobao-lookbook-reviewer` 进行图像质量审核。

---

**注意**: 使用本 Skill 需要确保模特已授权 AI 生成和商业使用。用户对生成内容的合规性负责。
