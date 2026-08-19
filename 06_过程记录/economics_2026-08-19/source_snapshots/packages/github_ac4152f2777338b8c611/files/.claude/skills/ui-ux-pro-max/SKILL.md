---
name: ui-ux-pro-max
description: "UI/UX 设计智能。包含 50 种风格、21 种调色板、50 种字体搭配、20 种图表、9 种技术栈 (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui)。支持操作：规划、构建、创建、设计、实现、审查、修复、改进、优化、增强、重构、检查 UI/UX 代码。项目类型：网站、落地页、仪表板、管理面板、电商、SaaS、作品集、博客、移动应用、.html, .tsx, .vue, .svelte。元素：按钮、模态框、导航栏、侧边栏、卡片、表格、表单、图表。风格：玻璃拟态、黏土拟态、极简主义、野兽派、新拟态、Bento 网格、暗黑模式、响应式、拟物化、扁平化设计。主题：调色板、无障碍性、动画、布局、排版、字体搭配、间距、悬停、阴影、渐变。集成：shadcn/ui MCP 用于组件搜索和示例。侧重于视觉决策”和“美学设计"
allowed-tools: "RunCommand,tdesign-mcp-server"
---

# UI/UX Pro Max - 设计智能

Web 和移动应用的综合设计指南。包含 9 种技术栈中的 50+ 种风格、97 种调色板、57 种字体搭配、99 条 UX 指南和 25 种图表类型。提供基于优先级的推荐的可搜索数据库。

## 何时应用 (When to Apply)

在以下情况参考这些指南：
- 设计新 UI 组件或页面时
- 选择调色板和排版时
- 审查代码中的 UX 问题时
- 构建落地页或仪表板时
- 实现无障碍性要求时

## 规则优先级分类 (Rule Categories by Priority)

| 优先级 | 分类 | 影响 | 领域 |
|----------|----------|--------|--------|
| 1 | Accessibility (无障碍性) | CRITICAL (关键) | `ux` |
| 2 | Touch & Interaction (触控与交互) | CRITICAL (关键) | `ux` |
| 3 | Performance (性能) | HIGH (高) | `ux` |
| 4 | Layout & Responsive (布局与响应式) | HIGH (高) | `ux` |
| 5 | Typography & Color (排版与色彩) | MEDIUM (中) | `typography`, `color` |
| 6 | Animation (动画) | MEDIUM (中) | `ux` |
| 7 | Style Selection (风格选择) | MEDIUM (中) | `style`, `product` |
| 8 | Charts & Data (图表与数据) | LOW (低) | `chart` |

## 快速参考 (Quick Reference)

### 1. Accessibility (无障碍性 - 关键)

- `color-contrast` - 普通文本对比度至少 4.5:1
- `focus-states` - 交互元素要有可见的焦点环
- `alt-text` - 为有意义的图片添加描述性 alt 文本
- `aria-labels` - 纯图标按钮需添加 aria-label
- `keyboard-nav` - Tab 键顺序与视觉顺序一致
- `form-labels` - 使用带有 for 属性的 label

### 2. Touch & Interaction (触控与交互 - 关键)

- `touch-target-size` - 触摸目标至少 44x44px
- `hover-vs-tap` - 主要交互使用点击/轻触（而非悬停）
- `loading-buttons` - 异步操作期间禁用按钮
- `error-feedback` - 在问题附近显示清晰的错误信息
- `cursor-pointer` - 为可点击元素添加 cursor-pointer

### 3. Performance (性能 - 高)

- `image-optimization` - 使用 WebP, srcset, 懒加载
- `reduced-motion` - 检查 prefers-reduced-motion
- `content-jumping` - 为异步内容预留空间

### 4. Layout & Responsive (布局与响应式 - 高)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - 移动端正文至少 16px
- `horizontal-scroll` - 确保内容适应视口宽度（无横向滚动）
- `z-index-management` - 定义 z-index 标尺 (10, 20, 30, 50)

### 5. Typography & Color (排版与色彩 - 中)

- `line-height` - 正文行高使用 1.5-1.75
- `line-length` - 每行限制 65-75 个字符
- `font-pairing` - 标题/正文字体性格相匹配

### 6. Animation (动画 - 中)

- `duration-timing` - 微交互使用 150-300ms
- `transform-performance` - 使用 transform/opacity，而非 width/height
- `loading-states` - 使用骨架屏或加载转圈

### 7. Style Selection (风格选择 - 中)

- `style-match` - 风格与产品类型匹配
- `consistency` - 所有页面风格保持一致
- `no-emoji-icons` - 使用 SVG 图标，而非 Emoji

### 8. Charts & Data (图表与数据 - 低)

- `chart-type` - 图表类型与数据类型匹配
- `color-guidance` - 使用无障碍调色板
- `data-table` - 提供表格作为无障碍替代方案

## 如何使用 (How to Use)

使用下方的 CLI 工具搜索特定领域。

---

## 先决条件 (Prerequisites)

检查 Python 安装：

```bash
python3 --version || python --version
```

如果未安装 Python，请根据用户操作系统进行安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## 如何使用此技能 (How to Use This Skill)

当用户请求 UI/UX 工作（设计、构建、创建、实现、审查、修复、改进）时，遵循此工作流：

### 第一步：分析用户需求 (Step 1: Analyze User Requirements)

提取关键信息：
- **Product type (产品类型)**: SaaS, 电商, 作品集, 仪表板, 落地页等
- **Style keywords (风格关键词)**: 极简, 俏皮, 专业, 优雅, 暗黑模式等
- **Industry (行业)**: 医疗, 金融科技, 游戏, 教育等
- **Stack (技术栈)**: React, Vue, Next.js, 或默认为 `html-tailwind`

### 第二步：生成设计系统 (必选) (Step 2: Generate Design System)

**始终以 `--design-system` 开始** 以获取带有推理的全面建议：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

此命令：
1. 并行搜索 5 个领域（产品、风格、色彩、落地页、排版）
2. 应用 `ui-reasoning.csv` 中的推理规则选择最佳匹配
3. 返回完整的设计系统：模式、风格、色彩、排版、效果
4. 包含应避免的反模式

**示例 (Example):**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 第二步b：持久化设计系统 (Master + Overrides 模式) (Step 2b: Persist Design System)

要保存设计系统以实现**跨会话的分层检索**，请添加 `--persist`：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

这将创建：
- `design-system/MASTER.md` — 包含所有设计规则的全局真理源 (Source of Truth)
- `design-system/pages/` — 页面特定覆盖规则的文件夹

**使用页面特定覆盖 (With page-specific override):**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

这还将创建：
- `design-system/pages/dashboard.md` — 页面特定的规则（偏离 Master 的部分）

**分层检索如何工作 (How hierarchical retrieval works):**
1. 构建特定页面（如 "Checkout"）时，首先检查 `design-system/pages/checkout.md`
2. 如果页面文件存在，其规则**覆盖** Master 文件
3. 如果不存在，仅使用 `design-system/MASTER.md`

**上下文感知检索提示词 (Context-aware retrieval prompt):**
```
我正在构建 [Page Name] 页面。请阅读 design-system/MASTER.md。
同时检查 design-system/pages/[page-name].md 是否存在。
如果页面文件存在，优先使用其规则。
如果不存在，仅使用 Master 规则。
现在，生成代码...
```

### 第三步：补充详细搜索 (按需) (Step 3: Supplement with Detailed Searches)

获取设计系统后，使用领域搜索获取更多细节：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**何时使用详细搜索 (When to use detailed searches):**

| 需求 | 领域 | 示例 |
|------|--------|---------|
| 更多风格选项 | `style` | `--domain style "glassmorphism dark"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX 最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 落地页结构 | `landing` | `--domain landing "hero social-proof"` |

### 第四步：技术栈指南 (默认: html-tailwind) (Step 4: Stack Guidelines)

获取特定实现的最佳实践。如果用户未指定技术栈，**默认为 `html-tailwind`**。

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## 搜索参考 (Search Reference)

### 可用领域 (Available Domains)

| 领域 | 用途 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型推荐 | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UI 风格、色彩、效果 | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | 字体搭配、Google Fonts | elegant, playful, professional, modern |
| `color` | 按产品类型的调色板 | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | 页面结构、CTA 策略 | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | 图表类型、库推荐 | trend, comparison, timeline, funnel, pie |
| `ux` | 最佳实践、反模式 | animation, accessibility, z-index, loading |
| `react` | React/Next.js 性能 | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Web 界面指南 | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI 提示词、CSS 关键词 | (style name) |

### 可用技术栈 (Available Stacks)

| 技术栈 | 侧重 |
|-------|-------|
| `html-tailwind` | Tailwind 工具类, 响应式, 无障碍性 (默认) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms, patterns |
| `jetpack-compose` | Composables, Modifiers, State Hoisting, Recomposition |

---

## 示例工作流 (Example Workflow)

**User request:** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp" (制作专业护肤服务的落地页)

### 第一步：分析需求 (Step 1: Analyze Requirements)
- Product type: Beauty/Spa service
- Style keywords: elegant, professional, soft
- Industry: Beauty/Wellness
- Stack: html-tailwind (default)

### 第二步：生成设计系统 (必选) (Step 2: Generate Design System)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Output:** 包含模式、风格、色彩、排版、效果和反模式的完整设计系统。

### 第三步：补充详细搜索 (按需) (Step 3: Supplement with Detailed Searches)

```bash
# 获取动画和无障碍性的 UX 指南
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# 如果需要，获取替代字体选项
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### 第四步：技术栈指南 (Step 4: Stack Guidelines)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Then:** 综合设计系统 + 详细搜索结果，并实现设计。

---

## 输出格式 (Output Formats)

`--design-system` 标志支持两种输出格式：

```bash
# ASCII box (默认) - 最适合终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - 最适合文档
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 获取更好结果的技巧 (Tips for Better Results)

1. **关键词要具体 (Be specific with keywords)** - "healthcare SaaS dashboard" > "app"
2. **多次搜索 (Search multiple times)** - 不同的关键词揭示不同的见解
3. **组合领域 (Combine domains)** - 风格 + 排版 + 色彩 = 完整设计系统
4. **始终检查 UX (Always check UX)** - 搜索 "animation", "z-index", "accessibility" 以发现常见问题
5. **使用技术栈标志 (Use stack flag)** - 获取特定实现的最佳实践
6. **迭代 (Iterate)** - 如果第一次搜索不匹配，尝试不同的关键词

---

## 专业 UI 的通用规则 (Common Rules for Professional UI)

这些是导致 UI 看起来不专业的常见被忽视问题：

### 图标与视觉元素 (Icons & Visual Elements)

| 规则 | Do (建议) | Don't (禁止) |
|------|----|----- |
| **No emoji icons (无 Emoji 图标)** | 使用 SVG 图标 (Heroicons, Lucide, Simple Icons) | 使用 🎨 🚀 ⚙️ 等 Emoji 作为 UI 图标 |
| **Stable hover states (稳定的悬停状态)** | 悬停时使用颜色/不透明度过渡 | 使用改变布局的缩放变换 |
| **Correct brand logos (正确的品牌 Logo)** | 从 Simple Icons 查找官方 SVG | 猜测或使用错误的 Logo 路径 |
| **Consistent icon sizing (一致的图标尺寸)** | 使用固定的 viewBox (24x24) 和 w-6 h-6 | 随意混合不同图标尺寸 |

### 交互与光标 (Interaction & Cursor)

| 规则 | Do (建议) | Don't (禁止) |
|------|----|----- |
| **Cursor pointer (指针光标)** | 为所有可点击/悬停卡片添加 `cursor-pointer` | 交互元素保留默认光标 |
| **Hover feedback (悬停反馈)** | 提供视觉反馈（颜色、阴影、边框） | 没有任何元素可交互的指示 |
| **Smooth transitions (平滑过渡)** | 使用 `transition-colors duration-200` | 状态突变或过慢 (>500ms) |

### 亮/暗模式对比度 (Light/Dark Mode Contrast)

| 规则 | Do (建议) | Don't (禁止) |
|------|----|----- |
| **Glass card light mode (亮色模式玻璃卡片)** | 使用 `bg-white/80` 或更高不透明度 | 使用 `bg-white/10` (太透明) |
| **Text contrast light (亮色模式文本对比度)** | 使用 `#0F172A` (slate-900) 作为文本 | 使用 `#94A3B8` (slate-400) 作为正文 |
| **Muted text light (亮色模式柔和文本)** | 最低使用 `#475569` (slate-600) | 使用 gray-400 或更浅 |
| **Border visibility (边框可见性)** | 亮色模式使用 `border-gray-200` | 使用 `border-white/10` (不可见) |

### 布局与间距 (Layout & Spacing)

| 规则 | Do (建议) | Don't (禁止) |
|------|----|----- |
| **Floating navbar (悬浮导航栏)** | 添加 `top-4 left-4 right-4` 间距 | 导航栏贴死 `top-0 left-0 right-0` |
| **Content padding (内容内边距)** | 考虑固定导航栏的高度 | 让内容隐藏在固定元素后面 |
| **Consistent max-width (一致的最大宽度)** | 使用相同的 `max-w-6xl` 或 `max-w-7xl` | 混合不同的容器宽度 |

---

## 交付前检查清单 (Pre-Delivery Checklist)

交付 UI 代码前，验证这些项目：

### 视觉质量 (Visual Quality)
- [ ] 未使用 Emoji 作为图标（改用 SVG）
- [ ] 所有图标来自一致的图标集 (Heroicons/Lucide)
- [ ] 品牌 Logo 正确（经 Simple Icons 验证）
- [ ] 悬停状态不会导致布局偏移
- [ ] 直接使用主题颜色 (bg-primary) 而非 var() 包装器

### 交互 (Interaction)
- [ ] 所有可点击元素都有 `cursor-pointer`
- [ ] 悬停状态提供清晰的视觉反馈
- [ ] 过渡平滑 (150-300ms)
- [ ] 键盘导航有可见的焦点状态

### 亮/暗模式 (Light/Dark Mode)
- [ ] 亮色模式文本有足够对比度（最低 4.5:1）
- [ ] 玻璃/透明元素在亮色模式下可见
- [ ] 边框在两种模式下都可见
- [ ] 交付前测试两种模式

### 布局 (Layout)
- [ ] 悬浮元素与边缘有适当间距
- [ ] 没有内容隐藏在固定导航栏后面
- [ ] 在 375px, 768px, 1024px, 1440px 下响应式良好
- [ ] 移动端无横向滚动

### 无障碍性 (Accessibility)
- [ ] 所有图片都有 alt 文本
- [ ] 表单输入框有 label
- [ ] 颜色不是唯一的指示器
- [ ] 遵守 `prefers-reduced-motion`
