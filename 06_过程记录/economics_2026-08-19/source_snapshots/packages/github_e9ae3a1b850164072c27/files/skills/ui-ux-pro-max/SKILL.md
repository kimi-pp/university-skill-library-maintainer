---
name: ui-ux-pro-max
description: "专业UI/UX设计工具 - 生成完整设计系统、搭建着陆页、协助前端实现"
trigger_keywords: "UI设计、UX优化、着陆页、设计系统、前端界面、页面布局、样式设计、配色方案、排版设计"
auto_activate: true
priority: 5
---

# ui-ux-pro-max

## 直接触发指令

当用户请求以下内容时自动激活此技能：
- "设计一个XXX页面"
- "帮我生成设计系统"
- "做一个着陆页"
- "优化UI/UX体验"
- "帮我选择配色和字体"
- "前端界面实现"

## 快速启动

直接使用以下指令快速开始：

```
生成[产品类型]的设计系统，使用[风格关键词]
```

```
帮我创建一个专业的着陆页
```

```
帮我优化这个页面的用户体验
```

## 如何使用此技能

当用户请求 UI/UX 工作时（设计、构建、创建、实现、审查、修复、改进），请遵循以下工作流程：

### 第1步：分析用户需求

从用户请求中提取关键信息：
- **产品类型**: SaaS、电商、作品集、仪表板、着陆页等
- **风格关键词**: 极简、有趣、专业、优雅、深色模式等
- **行业**: 医疗健康、金融科技、游戏、教育等
- **技术栈**: React、Vue、Next.js，或默认使用 `html-tailwind`

### 第2步：生成设计系统（必需）

**始终以 `--design-system` 开始** 以获取带有推理的全面推荐：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

此命令：
1. 并行搜索5个领域（产品、风格、颜色、着陆页、字体）
2. 应用 `ui-reasoning.csv` 中的推理规则来选择最佳匹配
3. 返回完整的设计系统：模式、风格、颜色、字体、效果
4. 包含应避免的反模式

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 第2b步：持久化设计系统（主规则 + 覆盖模式）

要保存设计系统以实现跨会话的分层检索，请添加 `--persist`：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

这将创建：
- `design-system/MASTER.md` — 全局真理来源，包含所有设计规则
- `design-system/pages/` — 页面特定覆盖的文件夹

**带有页面特定覆盖：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

这还将创建：
- `design-system/pages/dashboard.md` — 页面特定偏离主规则的覆盖

**分层检索的工作原理：**
1. 构建特定页面时（例如 "Checkout"），首先检查 `design-system/pages/checkout.md`
2. 如果页面文件存在，其规则**覆盖**主文件
3. 如果不存在，完全使用 `design-system/MASTER.md`

### 第3步：补充详细搜索（如需要）

获取设计系统后，使用领域搜索获取额外详情：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**何时使用详细搜索：**

| 需要 | 领域 | 示例 |
|------|------|------|
| 更多风格选项 | `style` | `--domain style "glassmorphism dark"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX 最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 着陆页结构 | `landing` | `--domain landing "hero social-proof"` |

### 第4步：技术栈指南（默认：html-tailwind）

获取特定于实现的最佳实践。如果用户未指定技术栈，**默认使用 `html-tailwind`**。

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈：`html-tailwind`、`react`、`nextjs`、`vue`、`svelte`、`swiftui`、`react-native`、`flutter`、`shadcn`、`jetpack-compose`

---

## 搜索参考

### 可用领域

| 领域 | 用于 | 示例关键词 |
|------|------|-----------|
| `product` | 产品类型推荐 | SaaS、电商、作品集、医疗健康、美容、服务 |
| `style` | UI 风格、颜色、效果 | 玻璃拟态、极简主义、深色模式、野蛮主义 |
| `typography` | 字体配对、Google 字体 | 优雅、有趣、专业、现代 |
| `color` | 按产品类型的配色 | saas、电商、医疗健康、美容、金融科技、服务 |
| `landing` | 页面结构、CTA 策略 | 英雄、英雄中心、推荐、定价、社会证明 |
| `chart` | 图表类型、库推荐 | 趋势、比较、时间线、漏斗、饼图 |
| `ux` | 最佳实践、反模式 | 动画、可访问性、z-index、加载 |
| `react` | React/Next.js 性能 | 瀑布、捆绑、悬念、记忆化、重新渲染、缓存 |
| `web` | Web 界面指南 | aria、焦点、键盘、语义、虚拟化 |
| `prompt` | AI 提示、CSS 关键词 | (风格名称) |

### 可用技术栈

| 技术栈 | 重点 |
|--------|------|
| `html-tailwind` | Tailwind 工具、响应式、可访问性（默认） |
| `react` | 状态、钩子、性能、模式 |
| `nextjs` | SSR、路由、图像、API 路由 |
| `vue` | 组合式 API、Pinia、Vue 路由 |
| `svelte` | Rune、存储、SvelteKit |
| `swiftui` | 视图、状态、导航、动画 |
| `react-native` | 组件、导航、列表 |
| `flutter` | 小部件、状态、布局、主题 |
| `shadcn` | shadcn/ui 组件、主题、表单、模式 |
| `jetpack-compose` | 可组合函数、修饰符、状态提升、重组 |

---

## 示例工作流程

**用户请求：** "设计一个专业的美容spa服务着陆页"

### 第1步：分析需求
- 产品类型：美容/Spa 服务
- 风格关键词：优雅、专业、柔和
- 行业：美容/健康
- 技术栈：html-tailwind（默认）

### 第2步：生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**输出：** 完整的设计系统，包含模式、风格、颜色、字体、效果和反模式。

### 第3步：补充详细搜索（如需要）

```bash
# 获取动画和可访问性的 UX 指南
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# 如需要，获取替代字体选项
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### 第4步：技术栈指南

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**然后：** 综合设计系统 + 详细搜索并实现设计。

---

## 输出格式

`--design-system` 标志支持两种输出格式：

```bash
# ASCII 框（默认）- 适合终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - 适合文档
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 获得更好结果的技巧

1. **使用具体关键词** - "医疗 SaaS 仪表板" > "应用"
2. **多次搜索** - 不同关键词揭示不同见解
3. **组合领域** - 风格 + 字体 + 颜色 = 完整设计系统
4. **始终检查 UX** - 搜索 "animation"、"z-index"、"accessibility" 以发现常见问题
5. **使用技术栈标志** - 获取特定于实现的最佳实践
6. **迭代** - 如果第一次搜索不匹配，尝试不同关键词

---

## 专业 UI 的常见规则

这些是经常被忽视的问题，会使 UI 看起来不专业：

### 图标和视觉元素

| 规则 | 做 | 不做 |
|------|----|------|
| **不用表情符号图标** | 使用 SVG 图标（Heroicons、Lucide、Simple Icons） | 使用 🎨 🚀 ⚙️ 等表情符号作为 UI 图标 |
| **稳定的悬停状态** | 悬停时使用颜色/不透明度过渡 | 使用导致布局偏移的缩放变换 |
| **正确的品牌标志** | 从 Simple Icons 研究官方 SVG | 猜测或使用错误的标志路径 |
| **一致的图标大小** | 使用固定的 viewBox（24x24）和 w-6 h-6 | 随机混合不同的图标大小 |

### 交互和光标

| 规则 | 做 | 不做 |
|------|----|------|
| **光标指针** | 为所有可点击/可悬停的卡片添加 `cursor-pointer` | 保持可交互元素的默认光标 |
| **悬停反馈** | 提供视觉反馈（颜色、阴影、边框） | 没有元素可交互的指示 |
| **平滑过渡** | 使用 `transition-colors duration-200` | 瞬间状态变化或太慢（>500ms） |

### 浅色/深色模式对比

| 规则 | 做 | 不做 |
|------|----|------|
| **浅色模式玻璃卡片** | 使用 `bg-white/80` 或更高不透明度 | 使用 `bg-white/10`（太透明） |
| **浅色模式文本对比** | 文本使用 `#0F172A`（slate-900） | 正文文本使用 `#94A3B8`（slate-400） |
| **浅色模式辅助文本** | 最低使用 `#475569`（slate-600） | 使用 gray-400 或更浅 |
| **边框可见性** | 浅色模式使用 `border-gray-200` | 使用 `border-white/10`（不可见） |

### 布局和间距

| 规则 | 做 | 不做 |
|------|----|------|
| **浮动导航栏** | 添加 `top-4 left-4 right-4` 间距 | 将导航栏粘在 `top-0 left-0 right-0` |
| **内容内边距** | 考虑固定导航栏高度 | 让内容隐藏在固定元素后面 |
| **一致的 max-width** | 使用相同的 `max-w-6xl` 或 `max-w-7xl` | 混合不同的容器宽度 |

---

## 交付前检查清单

在交付 UI 代码之前，验证以下项目：

### 视觉质量
- [ ] 不用表情符号作为图标（使用 SVG 代替）
- [ ] 所有图标来自一致的图标集（Heroicons/Lucide）
- [ ] 品牌标志正确（从 Simple Icons 验证）
- [ ] 悬停状态不会导致布局偏移
- [ ] 直接使用主题颜色（bg-primary）而不是 var() 包装器

### 交互
- [ ] 所有可点击元素有 `cursor-pointer`
- [ ] 悬停状态提供清晰的视觉反馈
- [ ] 过渡平滑（150-300ms）
- [ ] 键盘导航焦点状态可见

### 浅色/深色模式
- [ ] 浅色模式文本有足够的对比度（最低 4.5:1）
- [ ] 浅色模式中玻璃/透明元素可见
- [ ] 两种模式下边框可见
- [ ] 交付前测试两种模式

### 布局
- [ ] 浮动元素与边缘有适当的间距
- [ ] 没有内容隐藏在固定导航栏后面
- [ ] 在 375px、768px、1024px、1440px 下响应式
- [ ] 移动端没有水平滚动

### 可访问性
- [ ] 所有图片有替代文本
- [ ] 表单输入有标签
- [ ] 颜色不是唯一的指示器
- [ ] 尊重 `prefers-reduced-motion`
