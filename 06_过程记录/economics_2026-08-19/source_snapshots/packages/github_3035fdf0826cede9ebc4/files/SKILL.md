---
name: design-generator
description: |
  工业级设计系统生成器。通过三层指令架构（L1基础审美→L2组件行为→L3场景特征）实现业务解耦，一键切换20+核心视觉场景，输出Google规范代码。
  
  触发场景：
  - 生成UI原型/页面/组件："生成登录页"、"创建卡片组件"、"做一个仪表盘"
  - 切换视觉风格："换成赛博朋克风格"、"切换金融科技主题"、"用极光渐变风格"
  - 设计系统生成："生成设计令牌"、"创建组件规范"、"输出CSS变量"
  - 场景关键词：赛博朋克/霓虹/极光/金融科技/企业级/SaaS/游戏化/极简/毛玻璃/新拟态
  - 组件关键词：按钮/表单/卡片/导航/表格/弹窗/反馈
  
  支持输出：HTML快速原型、Vue组件、设计令牌CSS、完整页面
  预置场景：material-light/dark、apple-minimal、cyberpunk、neon-dark、aurora、fintech-minimal、enterprise-dark、dashboard-pro、gamified等20+场景
version: 1.0.0
license: MIT
---

# Design Generator - 工业级设计系统生成器

## Purpose

**配置驱动的UI设计系统生成器**，让AI具备工业级审美能力。

核心价值：
- **业务解耦**：三层架构分离，场景配置独立于组件逻辑
- **一键切换**：20+预置场景，秒级切换视觉风格
- **规范输出**：Google代码风格 + WCAG AA无障碍标准
- **双格式输出**：HTML快速原型 / Vue组件库

适用场景：
- 快速原型验证（MVP、概念演示）
- 设计系统搭建（设计令牌、组件规范）
- 视觉风格探索（多方案对比）
- 组件库开发（Vue SFC）

## Scope

### In scope
| 能力 | 说明 |
|------|------|
| 快速原型 | HTML/Vue 页面原型，开箱即用 |
| 设计令牌 | CSS变量系统，颜色/间距/圆角/阴影/字体 |
| 组件规范 | 按钮/表单/卡片/导航/数据展示/反馈组件 |
| 场景切换 | 20+预置场景，一键切换视觉风格 |
| 代码规范 | Google风格，语义化HTML，BEM命名 |
| 无障碍 | WCAG AA标准，键盘可访问，屏幕阅读器支持 |

### Out of scope
- 纯后端开发（API、数据库、服务端逻辑）
- 移动端原生应用（iOS Swift / Android Kotlin）
- 复杂业务逻辑实现（工作流引擎、权限系统）
- 纯品牌策略设计（品牌定位、视觉识别系统）

## Trigger Commands

### 页面生成
```
"生成一个登录页面"
"创建一个仪表盘页面，用金融科技风格"
"做一个赛博朋克风格的落地页"
"帮我设计一个产品展示页"
```

### 组件生成
```
"生成一个按钮组件"
"创建一个表单组件，Vue格式"
"做一个卡片组件，用极光渐变风格"
"生成导航栏组件"
```

### 风格切换
```
"切换到赛博朋克风格"
"换成金融科技主题"
"用极光渐变风格重新生成"
"切换成企业级深色主题"
```

### 设计系统
```
"生成设计令牌"
"输出CSS变量"
"创建组件规范文档"
"生成设计系统配置"
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户输入                                  │
│  "生成一个赛博朋克风格的登录页面"                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    1. 解析需求 (Parser)                          │
│  • 提取场景：cyberpunk                                           │
│  • 提取组件：form, button, card                                  │
│  • 提取技术栈：html (默认)                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    2. 加载配置 (Merger)                          │
│  • 加载 L1: base.json (基础物理规则)                             │
│  • 加载 L2: form.json + button.json (组件行为)                  │
│  • 加载 L3: cyberpunk.json (场景特征)                            │
│  • L3 覆盖 L1 默认值                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    3. 生成输出 (Generator)                       │
│  • 生成 tokens.css (设计令牌)                                    │
│  • 生成 LoginForm.html (组件代码)                                │
│  • 应用 Google 代码风格                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    4. 验证质量 (Validator)                       │
│  • 检查无障碍性 (WCAG AA)                                        │
│  • 检查响应式覆盖                                                │
│  • 检查交互状态完整性                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        输出结果                                  │
│  ├── tokens.css          # 设计令牌                              │
│  ├── styles.css          # 基础样式                              │
│  ├── index.html          # 完整页面                              │
│  └── DESIGN_SPEC.md      # 设计规范文档                          │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Architecture

| 层级 | 职责 | 示例 |
|------|------|------|
| **L1 基础审美层** | 定义圆角、阴影、网格、排版的物理规则 | `base.json`, `material3.json` |
| **L2 组件行为层** | 定义按钮状态、表单验证、交互逻辑 | `button.json`, `form.json` |
| **L3 场景特征层** | 覆盖 L1 默认值，实现场景切换 | `cyberpunk.json`, `fintech-minimal.json` |

### 配置继承规则

```
L3 场景配置
    │
    │ extends + overrides
    ▼
L1 基础配置
    │
    │ 定义默认值
    ▼
最终输出
```

## Available Scenarios (20 个核心场景)

### Modern Standard (标准现代风格)

| 场景标识 | 场景名称 | 视觉特征 | 适用场景 |
|----------|----------|----------|----------|
| `material-light` | Material Design 3 浅色 | 紫色主调，圆角卡片，柔和阴影 | 通用应用、内容平台 |
| `material-dark` | Material Design 3 深色 | 深色背景，霓虹紫，发光效果 | 夜间模式、媒体应用 |
| `apple-minimal` | Apple HIG 极简 | SF Pro字体，系统蓝，大圆角 | iOS风格应用、极简产品 |
| `glassmorphism` | 毛玻璃拟态 | 半透明模糊背景，渐变边框 | 创意展示、品牌页面 |
| `neumorphism` | 新拟态 | 柔和阴影凸起，单色调 | 概念设计、艺术项目 |

### Tech Future (科技未来风格)

| 场景标识 | 场景名称 | 视觉特征 | 适用场景 |
|----------|----------|----------|----------|
| `cyberpunk` | 赛博朋克 | 霓虹青/品红，锐利边角，发光效果 | 游戏、科技产品、创意展示 |
| `neon-dark` | 霓虹深色 | 深色背景，霓虹发光，故障艺术 | 夜间应用、娱乐平台 |
| `holographic` | 全息投影 | 透明科幻感，渐变光效 | AR/VR、未来科技 |
| `matrix` | 黑客帝国 | 绿色代码雨，终端风格 | 开发者工具、技术社区 |
| `aurora` | 极光渐变 | 紫青粉渐变，流动光效 | 创意产品、品牌展示 |

### Professional (专业商务风格)

| 场景标识 | 场景名称 | 视觉特征 | 适用场景 |
|----------|----------|----------|----------|
| `fintech-minimal` | 金融科技极简 | 蓝色主调，数据驱动，清晰表格 | 金融应用、数据仪表盘 |
| `enterprise-dark` | 企业级深色 | 深色主题，专业稳重，灰蓝色调 | 企业后台、管理系统 |
| `dashboard-pro` | 专业仪表盘 | 高信息密度，数据可视化 | 数据分析、监控平台 |
| `corporate-clean` | 企业简洁 | 干净专业，深蓝主调 | 企业官网、商务应用 |
| `saas-modern` | 现代 SaaS | 紫色活力，渐变按钮 | SaaS产品、订阅服务 |

### Playful (趣味创意风格)

| 场景标识 | 场景名称 | 视觉特征 | 适用场景 |
|----------|----------|----------|----------|
| `colorful-gradient` | 多彩渐变 | 活力四射，彩虹渐变 | 创意产品、年轻用户 |
| `playful-round` | 活泼圆润 | 友好亲切，大圆角，明亮色彩 | 儿童应用、社交产品 |
| `gamified` | 游戏化 | 趣味互动，金色成就，徽章系统 | 游戏平台、激励系统 |
| `cartoon-soft` | 卡通柔和 | 温馨可爱，柔和色彩，圆润造型 | 家庭应用、教育产品 |
| `retro-pop` | 复古波普 | 大胆配色，几何图形，波普艺术 | 创意展示、艺术项目 |

## Quick Start

### 示例 1：生成赛博朋克登录页

```
用户: 生成一个赛博朋克风格的登录页面

AI:
1. 加载 cyberpunk.json 场景配置
2. 合并 L1 基础层 + L2 表单组件
3. 输出 tokens.css + styles.css + index.html
```

### 示例 2：切换金融科技风格

```
用户: 切换到金融科技风格

AI:
1. 加载 fintech-minimal.json
2. 覆盖颜色、圆角、阴影
3. 重新生成 tokens.css
```

### 示例 3：生成 Vue 组件

```
用户: 生成一个 Vue 按钮组件，使用极光渐变风格

AI:
1. 加载 aurora.json 场景配置
2. 加载 button.json 组件配置
3. 输出 Button.vue
```

### 示例 4：创建完整仪表盘

```
用户: 创建一个金融仪表盘，包含统计卡片、图表区域、交易列表

AI:
1. 加载 fintech-minimal.json 场景配置
2. 加载 card.json + data-display.json 组件配置
3. 输出完整仪表盘页面
```

## Output Structure

```
output/
├── tokens.css              # 设计令牌 (CSS 变量)
├── styles.css              # 基础样式
├── components/             # 组件代码
│   ├── Button.vue
│   ├── Card.vue
│   └── Form.vue
├── pages/                  # 页面代码
│   └── LoginPage.vue
└── DESIGN_SPEC.md          # 设计规范文档
```

## Token Format

生成的 `tokens.css` 示例：

```css
/* Design Tokens - cyberpunk */
/* Generated by design-generator */

:root {
  /* COLORS */
  --color-primary: #00FFFF;
  --color-primary-hover: #33FFFF;
  --color-secondary: #FF00FF;
  --color-background: #0A0A0F;
  --color-surface: #1A1A2E;
  --color-text-primary: #E0E0E0;
  
  /* RADIUS */
  --radius-sm: 0;
  --radius-md: 2px;
  --radius-lg: 2px;
  
  /* SHADOW */
  --shadow-glow-primary: 0 0 20px rgba(0, 255, 255, 0.5);
  --shadow-md: 0 0 20px rgba(0, 255, 255, 0.4);
  
  /* SPACING */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-4: 16px;
  
  /* TYPOGRAPHY */
  --font-sans: 'Orbitron', 'Rajdhani', sans-serif;
  --font-size-base: 1rem;
  --font-weight-medium: 500;
}
```

## Component Config Format

组件配置示例 (`configs/components/button.json`)：

```json
{
  "layer": "L2",
  "component": "Button",
  "base": {
    "display": "inline-flex",
    "borderRadius": "var(--radius-md)"
  },
  "sizes": {
    "sm": { "height": "32px" },
    "md": { "height": "40px" },
    "lg": { "height": "48px" }
  },
  "variants": {
    "primary": {
      "default": { "background": "var(--color-primary)" },
      "hover": { "boxShadow": "var(--shadow-md)" },
      "disabled": { "opacity": "0.5" }
    }
  }
}
```

## Non-Negotiables

1. **先定义 tokens，再使用** - 所有颜色、间距、圆角必须使用 CSS 变量
2. **L3 覆盖 L1** - 场景配置可以覆盖基础配置，但不能覆盖组件行为
3. **完整状态覆盖** - 所有交互组件必须包含 default/hover/active/focus/disabled 状态
4. **无障碍合规** - 颜色对比度 ≥ 4.5:1，点击区域 ≥ 44x44px
5. **禁止硬编码** - 不允许在代码中直接写入颜色值或尺寸

## References

- `references/layer-architecture.md` - 三层架构详解
- `references/code-standards.md` - Google 代码规范
- `references/tech-stack-selector.md` - 技术栈选择
- `references/accessibility-guide.md` - 无障碍设计

## Directory Structure

```
design-generator/
├── SKILL.md                    # 本文件
├── engine/                     # Python 核心引擎
│   ├── parser.py               # 配置解析器
│   ├── token_generator.py      # 令牌生成器
│   ├── component_generator.py  # 组件生成器
│   ├── scenario_merger.py      # 场景合并器
│   └── validator.py            # 输出验证器
├── configs/                    # JSON 配置层
│   ├── foundations/            # L1 基础层 (5个)
│   ├── components/             # L2 组件层 (6个)
│   └── scenarios/              # L3 场景层 (20个)
├── templates/                  # 代码模板
│   ├── html/
│   └── vue/
├── references/                 # 参考文档
├── examples/                   # 示例输出
└── showcases/                  # 范例库（后期补充）
```