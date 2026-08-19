---
name: ui-ux-pro-max
description: "UI/UX 设计智能助手，适用于 Web 和移动端。包含 50+ 设计风格、161 配色方案、57 字体搭配、161 产品类型、99 UX 指南和 25 种图表类型，覆盖 10 种技术栈（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind、shadcn/ui、HTML/CSS）。适用场景：规划、建设、创建、设计、实施、审查、修复、改进、优化、增强、重构和检查 UI/UX 代码。项目类型：网站、落地页、仪表盘、管理后台、电商、SaaS、作品集、博客和移动端应用。组件类型：按钮、弹窗、导航栏、侧边栏、卡片、表格、表单和图表。设计风格：玻璃拟态、粘土拟态、极简主义、 brutality、 新拟态、 Bento Grid、暗色模式、响应式设计、写实主义和扁平化设计。涉及主题：色彩系统、无障碍访问、动画、布局、排版、字体搭配、间距、交互状态、阴影和渐变。集成：shadcn/ui MCP 组件搜索和示例。"
---

# UI/UX Pro Max - 设计智能助手

面向 Web 和移动端应用的综合设计指南。包含 50+ 设计风格、161 配色方案、57 字体搭配、161 种带推理规则的产品类型、99 条 UX 指南和 25 种图表类型，覆盖 10 种技术栈。支持优先级的可搜索数据库。

## 何时使用

当任务涉及 **UI 结构、视觉设计决策、交互模式或用户体验质量控制** 时，应使用此技能。

## 与 plan-for-all 的衔接

在 plan-for-all 架构中，本技能是由 `brainstorming` 主管调度的同级阶段之一，且在存在 UI 需求时先于 `writing-plans` 执行。

- 输入：已收敛的需求与 design 约束（功能目标、用户流程、边界、验收标准）
- 输出：可被 `writing-plans` 直接引用的 UI 规格（信息层级、页面结构、关键组件、交互状态、视觉方向、可访问性约束）
- 边界：不替代需求收敛，不决定非 UI 功能范围，不直接替代实现计划

### 必须落盘的 UI 规格输出（硬门禁）

当任务包含 UI 工作时，本技能必须产出并落盘：

- `docs/plan-for-all/specs/YYYY-MM-DD-<topic>-ui-spec.md`

建议基于 `templates/ui_refinement_spec.md` 生成，至少覆盖：

- 信息架构与页面结构
- 页面清单与关键用户流
- 组件清单与状态矩阵（默认、悬停、按下、禁用、错误、加载）
- 视觉方向与设计 token（颜色、排版、间距、圆角、阴影）
- 响应式与断点策略
- 可访问性与交互动效约束

未生成该文件时（任务涉及前端相关内容时），不得进入 `writing-plans`。

### 必须使用

以下情况必须调用此技能：

- 设计新页面（落地页、仪表盘、管理后台、SaaS、移动端应用）
- 创建或重构 UI 组件（按钮、弹窗、表单、表格、图表等）
- 选择配色方案、排版系统、间距标准或布局系统
- 审查 UI 代码的用户体验、无障碍访问或视觉一致性
- 实现导航结构、动画或响应式行为
- 做出产品级设计决策（风格、信息层次、品牌表达）
- 提升界面的感知质量、清晰度或可用性

### 推荐使用

以下情况推荐使用此技能：

- UI 看起来"不够专业"但原因不明
- 收到关于可用性或体验的反馈
- 发布前 UI 质量优化
- 跨平台设计对齐（Web / iOS / Android）
- 构建设计系统或可复用组件库

### 跳过

以下情况不需要此技能：

- 纯后端逻辑开发
- 仅涉及 API 或数据库设计
- 与界面无关的性能优化
- 基础设施或 DevOps 工作
- 非视觉脚本或自动化任务

**判断标准**：如果任务会改变功能的**外观、感觉、动效或交互方式**，则应使用此技能。

## 规则优先级分类

*供人类/AI 参考：按优先级 1→10 决定首先关注哪个规则类别；需要时使用 `--domain <领域>` 查询详情。脚本不读取此表。*

| 优先级 | 类别 | 影响 | 领域 | 关键检查（必须有）| 反模式（避免）|
|----------|----------|--------|--------|------------------------|------------------------|
| 1 | 无障碍访问 | 关键 | `ux` | 对比度 4.5:1、Alt 文本、键盘导航、Aria 标签 | 移除焦点环、无标签的图标按钮 |
| 2 | 触控与交互 | 关键 | `ux` | 最小尺寸 44×44px、间距 8px+、加载反馈 | 仅依赖悬停、瞬时状态变化（0ms）|
| 3 | 性能 | 高 | `ux` | WebP/AVIF、懒加载、预留空间（CLS < 0.1）| 布局抖动、累积布局偏移 |
| 4 | 风格选择 | 高 | `style`, `product` | 匹配产品类型、一致性、SVG 图标（不用 emoji）| 随机混用扁平与拟物风格、emoji 作为图标 |
| 5 | 布局与响应式 | 高 | `ux` | 移动端优先断点、Viewport meta、无横向滚动 | 横向滚动、固定 px 容器宽度、禁用缩放 |
| 6 | 排版与色彩 | 中 | `typography`, `color` | 基准 16px、行高 1.5、语义色彩令牌 | 正文文本 < 12px、灰度文字、组件中使用原始 hex |
| 7 | 动画 | 中 | `ux` | 时长 150–300ms、动效传达意义、空间连续性 | 纯装饰动画、动画化 width/height、无 reduced-motion |
| 8 | 表单与反馈 | 中 | `ux` | 可见标签、错误靠近字段、辅助文本、渐进披露 | 仅占位符标签、错误仅在顶部、一次性全部显示 |
| 9 | 导航模式 | 高 | `ux` | 可预测的返回、底部导航 ≤5、深度链接 | 导航过载、返回行为异常、无深度链接 |
| 10 | 图表与数据 | 低 | `chart` | 图例、工具提示、无障碍色彩 | 仅依赖色彩传达信息 |

## 快速参考

### 1. 无障碍访问（关键）

- `color-contrast` - 普通文本最小 4.5:1 对比度（大文本 3:1）
- `focus-states` - 可交互元素上的可见焦点环（2–4px）
- `alt-text` - 有意义图片的描述性 alt 文本
- `aria-labels` - 图标按钮的 aria-label；原生中的 accessibilityLabel
- `keyboard-nav` - Tab 顺序匹配视觉顺序；完整键盘支持
- `form-labels` - 使用带 for 属性的 label
- `skip-links` - 为键盘用户添加跳转到主要内容
- `heading-hierarchy` - 顺序 h1→h6，不跳级
- `color-not-only` - 不要仅用色彩传达信息（添加图标/文字）
- `dynamic-type` - 支持系统文本缩放；避免文字增长时截断
- `reduced-motion` - 尊重 prefers-reduced-motion；请求时减少/禁用动画
- `voiceover-sr` - 有意义的 accessibilityLabel/accessibilityHint；VoiceOver/屏幕阅读器的逻辑阅读顺序
- `escape-routes` - 在弹窗和多步流程中提供取消/返回
- `keyboard-shortcuts` - 保留系统和无障碍快捷键；为拖放提供键盘替代方案

### 2. 触控与交互（关键）

- `touch-target-size` - 最小 44×44pt（Apple）/ 48×48dp（Material）；如需要超出视觉边界扩展点击区域
- `touch-spacing` - 触控目标之间最小 8px/8dp 间距
- `hover-vs-tap` - 使用点击/tap 作为主要交互；不要仅依赖悬停
- `loading-buttons` - 异步操作期间禁用按钮；显示加载动画或进度
- `error-feedback` - 错误位置附近显示清晰的错误消息
- `cursor-pointer` - 为可点击元素添加 cursor-pointer（Web）
- `gesture-conflicts` - 避免在主要内容上水平滑动；优先垂直滚动
- `tap-delay` - 使用 touch-action: manipulation 减少 300ms 延迟（Web）
- `standard-gestures` - 一致使用平台标准手势；不要重新定义
- `system-gestures` - 不要阻止系统手势
- `press-feedback` - 按压时有视觉反馈（涟漪/高亮）
- `haptic-feedback` - 为确认和重要操作使用触觉反馈；避免过度使用
- `gesture-alternative` - 不要依赖纯手势交互；始终为关键操作提供可见控件
- `safe-area-awareness` - 保持主要触控目标远离刘海、灵动岛、手势条和屏幕边缘
- `no-precision-required` - 避免需要精确点击小图标或窄边
- `swipe-clarity` - 滑动操作必须显示清晰的 affordance 或提示
- `drag-threshold` - 开始拖动前使用移动阈值以避免意外拖动

### 3. 性能（高）

- `image-optimization` - 使用 WebP/AVIF、响应式图片（srcset/sizes）、懒加载非关键资源
- `image-dimension` - 声明 width/height 或使用 aspect-ratio 防止布局偏移
- `font-loading` - 使用 font-display: swap/optional 避免文本不可见
- `font-preload` - 仅预加载关键字体；避免过度使用预加载
- `critical-css` - 优先处理首屏 CSS
- `lazy-loading` - 通过动态导入/路由级拆分懒加载非首屏组件
- `bundle-splitting` - 按路由/功能拆分代码
- `third-party-scripts` - 异步/延迟加载第三方脚本
- `reduce-reflows` - 避免频繁的布局读写；批量处理 DOM 读取后写入
- `content-jumping` - 为异步内容预留空间避免布局跳动
- `lazy-load-below-fold` - 为首屏以下图片和重媒体使用 loading="lazy"
- `virtualize-lists` - 虚拟化 50+ 项列表以提高内存效率和滚动性能
- `main-thread-budget` - 每帧工作保持在 ~16ms 以内以实现 60fps
- `progressive-loading` - 超过 1s 的操作使用骨架屏而非阻塞性加载动画
- `input-latency` - 点击/滚动输入延迟保持在 ~100ms 以内
- `tap-feedback-speed` - 在 100ms 内提供点击视觉反馈
- `debounce-throttle` - 对高频事件（滚动、调整大小、输入）使用防抖/节流
- `offline-support` - 提供离线状态消息和基本回退
- `network-fallback` - 为慢网络提供降级模式

### 4. 风格选择（高）

- `style-match` - 风格匹配产品类型
- `consistency` - 所有页面使用相同风格
- `no-emoji-icons` - 使用 SVG 图标（Heroicons、Lucide），不用 emoji
- `color-palette-from-product` - 根据产品/行业选择配色
- `effects-match-style` - 阴影、模糊、圆角与选定风格对齐
- `platform-adaptive` - 尊重平台惯例（iOS HIG vs Material）
- `state-clarity` - 使悬停/按下/禁用状态在视觉上可区分
- `elevation-consistent` - 对卡片、弹窗、 sheets 使用一致的elevation/阴影
- `dark-mode-pairing` - 一起设计 light/dark 变体以保持品牌、对比度和风格一致
- `icon-style-consistent` - 使用统一的图标集/视觉语言
- `system-controls` - 优先使用原生/系统控件
- `blur-purpose` - 使用模糊表示背景关闭（弹窗、sheets），不用作装饰
- `primary-action` - 每个屏幕应只有一个主要 CTA

### 5. 布局与响应式（高）

- `viewport-meta` - width=device-width initial-scale=1（永不禁用缩放）
- `mobile-first` - 移动端优先设计，然后扩展到平板和桌面
- `breakpoint-consistency` - 使用系统性断点（如 375 / 768 / 1024 / 1440）
- `readable-font-size` - 移动端正文文本最小 16px
- `line-length-control` - 移动端每行 35–60 字符；桌面 60–75 字符
- `horizontal-scroll` - 移动端无横向滚动
- `spacing-scale` - 使用 4pt/8dp 增量间距系统
- `touch-density` - 保持组件间距舒适
- `container-width` - 桌面上一致的 max-width
- `z-index-management` - 定义分层 z-index 比例
- `fixed-element-offset` - 固定 navbar/bottom bar 必须为底层内容预留安全内边距
- `scroll-behavior` - 避免干扰主滚动体验的嵌套滚动区域
- `viewport-units` - 移动端优先使用 min-h-dvh 而非 100vh
- `orientation-support` - 保持布局在横屏模式下可读和可操作
- `content-priority` - 移动端首先显示核心内容
- `visual-hierarchy` - 通过尺寸、间距、对比度建立层次结构

### 6. 排版与色彩（中）

- `line-height` - 正文行高使用 1.5-1.75
- `line-length` - 每行限制 65-75 字符
- `font-pairing` - 标题/正文字体个性匹配
- `font-scale` - 一致的类型比例（如 12 14 16 18 24 32）
- `contrast-readability` - 浅色背景上使用深色文字
- `text-styles-system` - 使用平台类型系统
- `weight-hierarchy` - 使用字重强化层次结构
- `color-semantic` - 定义语义色彩令牌而非原始 hex
- `color-dark-mode` - 暗色模式使用去饱和/更浅的色调变体
- `color-accessible-pairs` - 前景/背景配对必须满足 4.5:1（AA）或 7:1（AAA）
- `color-not-decorative-only` - 功能色（错误红、成功绿）必须包含图标/文字
- `truncation-strategy` - 优先换行而非截断
- `letter-spacing` - 尊重每平台的默认字间距
- `number-tabular` - 数据列使用等宽数字
- `whitespace-balance` - 有意识地使用空白分组相关内容

### 7. 动画（中）

- `duration-timing` - 微交互使用 150–300ms；复杂过渡 ≤400ms
- `transform-performance` - 仅使用 transform/opacity；避免动画化 width/height/top/left
- `loading-states` - 加载超过 300ms 时显示骨架屏或进度指示
- `excessive-motion` - 每个视图最多动画化 1-2 个关键元素
- `easing` - 入场使用 ease-out；出场使用 ease-in
- `motion-meaning` - 每个动画必须表达因果关系
- `state-transition` - 状态变化应平滑动画化
- `continuity` - 页面/屏幕过渡应保持空间连续性
- `parallax-subtle` - 谨慎使用视差；必须尊重 reduced-motion
- `spring-physics` - 优先使用 spring/physics 曲线
- `exit-faster-than-enter` - 出场动画短于入场动画
- `stagger-sequence` - 列表/网格项入场交错 30–50ms
- `shared-element-transition` - 使用共享元素/英雄过渡
- `interruptible` - 动画必须可中断
- `no-blocking-animation` - 动画期间绝不阻止用户输入
- `fade-crossfade` - 使用交叉淡入淡出替换内容
- `scale-feedback` - 按压时轻微缩放（0.95–1.05）
- `gesture-feedback` - 拖动、滑动必须提供实时视觉响应
- `hierarchy-motion` - 使用 translate/scale 方向表达层次
- `motion-consistency` - 统一时长/缓动令牌
- `opacity-threshold` - 淡出元素不应停留在不透明度 0.2 以下
- `modal-motion` - 弹窗/sheets 应从触发源动画入场
- `navigation-direction` - 前进导航左/上滑；后退右/下滑
- `layout-shift-avoid` - 动画不得导致布局偏移

### 8. 表单与反馈（中）

- `input-labels` - 每个输入有可见标签
- `error-placement` - 在相关字段下方显示错误
- `submit-feedback` - 提交后加载然后成功/错误状态
- `required-indicators` - 标记必填字段
- `empty-states` - 无内容时有帮助的消息和操作
- `toast-dismiss` - 3-5s 自动消失
- `confirmation-dialogs` - 破坏性操作前确认
- `input-helper-text` - 为复杂输入提供持久辅助文本
- `disabled-states` - 禁用元素使用降低的不透明度
- `progressive-disclosure` - 渐进披露复杂选项
- `inline-validation` - 在 blur 时验证（非按键时）
- `input-type-keyboard` - 使用语义输入类型触发正确键盘
- `password-toggle` - 提供显示/隐藏密码切换
- `autofill-support` - 使用 autocomplete 属性
- `undo-support` - 允许撤销破坏性或批量操作
- `success-feedback` - 确认完成操作
- `error-recovery` - 错误消息包含明确恢复路径
- `multi-step-progress` - 多步流程显示步骤指示器
- `form-autosave` - 长表单应自动保存草稿
- `sheet-dismiss-confirm` - 确认关闭有未保存更改的 sheet/modal
- `error-clarity` - 错误消息必须说明原因和如何修复
- `field-grouping` - 逻辑分组相关字段
- `read-only-distinction` - 只读状态应与禁用状态可区分
- `focus-management` - 提交错误后自动聚焦第一个无效字段
- `error-summary` - 多个错误时在顶部显示摘要
- `touch-friendly-input` - 移动端输入高度 ≥44px
- `destructive-emphasis` - 破坏性操作使用语义危险色
- `toast-accessibility` - Toast 不得窃取焦点；使用 aria-live="polite"
- `aria-live-errors` - 表单错误使用 aria-live 区域
- `contrast-feedback` - 错误和成功状态色彩必须满足 4.5:1 对比度
- `timeout-feedback` - 请求超时必须显示明确反馈和重试选项

### 9. 导航模式（高）

- `bottom-nav-limit` - 底部导航最多 5 项
- `drawer-usage` - 使用 drawer/sidebar 处理辅助导航
- `back-behavior` - 返回导航必须可预测和一致
- `deep-linking` - 所有关键屏幕必须可通过深度链接/URL 访问
- `tab-bar-ios` - iOS：使用底部 Tab Bar 作为顶级导航
- `top-app-bar-android` - Android：使用顶部 App Bar
- `nav-label-icon` - 导航项必须有图标和文字标签
- `nav-state-active` - 当前位置必须在导航中视觉突出
- `nav-hierarchy` - 主导航和辅助导航必须清晰分离
- `modal-escape` - 弹窗和 sheets 必须提供清晰的关闭 affordance
- `search-accessible` - 搜索必须易于触及
- `breadcrumb-web` - Web：3+ 级深度使用面包屑
- `state-preservation` - 返回时必须恢复之前的滚动位置、筛选状态和输入
- `gesture-nav-support` - 支持系统手势导航
- `tab-badge` - 谨慎使用导航项上的 badge
- `overflow-menu` - 操作超出可用空间时使用 overflow/more 菜单
- `bottom-nav-top-level` - 底部导航仅用于顶级屏幕
- `adaptive-navigation` - 大屏幕（≥1024px）优先侧边栏；小屏幕使用底部/顶部导航
- `back-stack-integrity` - 绝不静默重置导航栈
- `navigation-consistency` - 导航放置必须在所有页面保持一致
- `avoid-mixed-patterns` - 不要在同一层次混用 Tab + Sidebar + Bottom Nav
- `modal-vs-navigation` - 弹窗不得用于主要导航流程
- `focus-on-route-change` - 页面转换后将焦点移到主要内容区域
- `persistent-nav` - 核心导航必须从深层页面可及
- `destructive-nav-separation` - 危险操作必须在视觉和空间上与正常导航项分离
- `empty-nav-state` - 导航目标不可用时解释原因

### 10. 图表与数据（低）

- `chart-type` - 图表类型匹配数据类型
- `color-guidance` - 使用无障碍配色方案
- `data-table` - 提供表格替代方案
- `pattern-texture` - 用图案、纹理或形状补充色彩
- `legend-visible` - 始终显示图例
- `tooltip-on-interact` - 悬停/点击时提供工具提示
- `axis-labels` - 标注轴和可读刻度
- `responsive-chart` - 图表必须在小屏幕上重排或简化
- `empty-data-state` - 无数据时显示有意义的空状态
- `loading-chart` - 图表数据加载时使用骨架占位符
- `animation-optional` - 图表入场动画必须尊重 prefers-reduced-motion
- `large-dataset` - 1000+ 数据点聚合或采样
- `number-formatting` - 使用地区感知数字、日期、货币格式
- `touch-target-chart` - 交互式图表元素必须有 ≥44pt 点击区域
- `no-pie-overuse` - 超过 5 类时避免饼图/甜甜圈图
- `contrast-data` - 数据线/条与背景 ≥3:1
- `legend-interactive` - 图例应可点击切换系列可见性
- `direct-labeling` - 小数据集直接在图表上标注值
- `tooltip-keyboard` - 工具提示内容必须键盘可及
- `sortable-table` - 数据表必须支持排序
- `axis-readability` - 轴刻度不得拥挤
- `data-density` - 限制每个图表的信息密度
- `trend-emphasis` - 强调数据趋势而非装饰
- `gridline-subtle` - 网格线应低对比度
- `focusable-elements` - 交互式图表元素必须键盘可导航
- `screen-reader-summary` - 为屏幕阅读器提供文本摘要
- `error-state-chart` - 数据加载失败显示错误消息和重试操作
- `export-option` - 为数据密集型产品提供 CSV/图片导出
- `drill-down-consistency` - 钻取交互必须保持清晰的返回路径
- `time-scale-clarity` - 时间序列图表必须清楚标注时间粒度

---

## 如何使用

使用 CLI 工具搜索特定领域。

---

## 前置要求

检查 Python 是否已安装：

```bash
python3 --version || python --version
```

如果未安装，根据用户操作系统安装：

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

## 如何使用此技能

以下情况使用此技能：

| 场景 | 触发示例 | 起始步骤 |
|----------|-----------------|------------|
| **新项目/页面** | "创建一个落地页"、"创建一个仪表盘" | 步骤 1 → 步骤 2（设计系统）|
| **新组件** | "创建一个定价卡片"、"添加一个弹窗" | 步骤 3（领域搜索：style, ux）|
| **选择风格/颜色/字体** | "什么风格适合金融科技应用？"、"推荐一个配色方案" | 步骤 2（设计系统）|
| **审查现有 UI** | "审查这个页面的 UX 问题"、"检查无障碍访问" | 快速参考检查清单 |
| **修复 UI bug** | "按钮悬停坏了"、"布局加载时偏移" | 快速参考 → 相关章节 |
| **改进/优化** | "让它更快"、"改善移动端体验" | 步骤 3（领域搜索：ux, react）|
| **实现暗色模式** | "添加暗色模式支持" | 步骤 3（领域：style "dark mode"）|
| **添加图表/数据可视化** | "添加分析仪表盘图表" | 步骤 3（领域：chart）|
| **技术栈最佳实践** | "React 性能提示"、"SwiftUI 导航" | 步骤 4（技术栈搜索）|

按以下流程执行：

### 步骤 1: 分析用户需求

从用户请求中提取关键信息：
- **产品类型**：娱乐（社交、视频、音乐、游戏）、工具（扫描仪、编辑器、转换器）、生产力（任务管理器、笔记、日历）或混合
- **目标用户**：C 端消费者用户；考虑年龄组、使用场景（通勤、休闲、工作）
- **风格关键词**：活泼、活力、极简、暗色模式、内容优先、沉浸式等
- **技术栈**：React Native（此项目唯一技术栈）

### 步骤 2: 生成设计系统（必需）

**始终首先使用 `--design-system`** 获取带推理的全面推荐：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<产品类型> <行业> <关键词>" --design-system [-p "项目名称"]
```

此命令：
1. 并行搜索领域（product、style、color、landing、typography）
2. 应用来自 `ui-reasoning.csv` 的推理规则选择最佳匹配
3. 返回完整设计系统：模式、风格、颜色、排版、效果
4. 包含要避免的反模式

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 步骤 2b: 持久化设计系统（主模式 + 覆盖模式）

为**跨会话的分层检索**保存设计系统，添加 `--persist`：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<查询>" --design-system --persist -p "项目名称"
```

这会创建：
- `design-system/MASTER.md` — 全局真理源，包含所有设计规则
- `design-system/pages/` — 页面特定覆盖文件夹

**带页面特定覆盖：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<查询>" --design-system --persist -p "项目名称" --page "dashboard"
```

这还会创建：
- `design-system/pages/dashboard.md` — 页面特定偏离主文件

**分层检索工作原理：**
1. 构建特定页面（如 "Checkout"）时，首先检查 `design-system/pages/checkout.md`
2. 如果页面文件存在，其规则**覆盖**主文件
3. 如果不存在，仅使用 `design-system/MASTER.md`

**上下文感知检索提示：**
```
我正在构建 [页面名称] 页面。请阅读 design-system/MASTER.md。
同时检查 design-system/pages/[page-name].md 是否存在。
如果页面文件存在，优先使用其规则。
如果不存在，仅使用 Master 规则。
现在，生成代码...
```

### 步骤 3: 根据需要补充详细搜索

获取设计系统后，使用领域搜索获取更多细节：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <领域> [-n <最大结果数>]
```

**何时使用详细搜索：**

| 需求 | 领域 | 示例 |
|------|--------|---------|
| 产品类型模式 | `product` | `--domain product "entertainment social"` |
| 更多风格选项 | `style` | `--domain style "glassmorphism dark"` |
| 配色方案 | `color` | `--domain color "entertainment vibrant"` |
| 字体搭配 | `typography` | `--domain typography "playful modern"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX 最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 单个 Google 字体 | `google-fonts` | `--domain google-fonts "sans serif popular variable"` |
| 落地页结构 | `landing` | `--domain landing "hero social-proof"` |
| React Native 性能 | `react` | `--domain react "rerender memo list"` |
| App 界面 a11y | `web` | `--domain web "accessibilityLabel touch safe-areas"` |
| AI 提示/CSS 关键词 | `prompt` | `--domain prompt "minimalism"` |

### 步骤 4: 技术栈指南

获取特定技术栈的实现指南：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack react-native
```

---

## 搜索参考

### 可用领域

| 领域 | 用途 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型推荐 | SaaS、电商、作品集、医疗保健、美容、服务 |
| `style` | UI 风格、颜色、效果 | glassmorphism、极简主义、暗色模式、brutalism |
| `typography` | 字体搭配、Google Fonts | 优雅、活泼、专业、现代 |
| `color` | 按产品类型的配色方案 | saas、电商、医疗保健、美容、金融科技、服务 |
| `landing` | 页面结构、CTA 策略 | hero、hero-centric、testimonial、pricing、social-proof |
| `chart` | 图表类型、库推荐 | trend、comparison、timeline、funnel、pie |
| `ux` | 最佳实践、反模式 | animation、accessibility、z-index、loading |
| `google-fonts` | 单个 Google Fonts 查询 | sans serif、monospace、japanese、variable font、popular |
| `react` | React/Next.js 性能 | waterfall、bundle、suspense、memo、rerender、cache |
| `web` | App 界面指南（iOS/Android/React Native）| accessibilityLabel、touch targets、safe areas、Dynamic Type |
| `prompt` | AI 提示、CSS 关键词 | （风格名称）|

### 可用技术栈

| 技术栈 | 关注点 |
|-------|-------|
| `react-native` | 组件、导航、列表 |

---

## 示例流程

**用户请求：** "创建一个 AI 搜索首页。"

### 步骤 1: 分析需求
- 产品类型：工具（AI 搜索引擎）
- 目标用户：寻找快速、智能搜索的 C 端用户
- 风格关键词：现代、极简、内容优先、暗色模式
- 技术栈：React Native

### 步骤 2: 生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "AI search tool modern minimal" --design-system -p "AI Search"
```

**输出：** 包含模式、风格、颜色、排版、效果和反模式的完整设计系统。

### 步骤 3: 根据需要补充详细搜索

```bash
# 获取现代工具产品的风格选项
python3 skills/ui-ux-pro-max/scripts/search.py "minimalism dark mode" --domain style

# 获取搜索交互和加载的 UX 最佳实践
python3 skills/ui-ux-pro-max/scripts/search.py "search loading animation" --domain ux
```

### 步骤 4: 技术栈指南

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "list performance navigation" --stack react-native
```

**然后：** 综合设计系统 + 详细搜索并实现设计。

---

## 输出格式

`--design-system` 标志支持两种输出格式：

```bash
# ASCII 框（默认）- 最佳终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - 最佳文档格式
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 更好结果的技巧

### 查询策略

- 使用**多维关键词** — 结合产品 + 行业 + 调性 + 密度：`"entertainment social vibrant content-dense"` 而非仅 `"app"`
- 为同一需求尝试不同关键词：`"playful neon"` → `"vibrant dark"` → `"content-first minimal"`
- 首先使用 `--design-system` 获取全面推荐，然后使用 `--domain` 深挖不确定的维度
- 始终添加 `--stack react-native` 获取特定技术栈指导

### 常见难点

| 问题 | 解决方法 |
|---------|---------|
| 无法决定风格/颜色 | 使用不同关键词重新运行 `--design-system` |
| 暗色模式对比度问题 | 快速参考 §6: `color-dark-mode` + `color-accessible-pairs` |
| 动画感觉不自然 | 快速参考 §7: `spring-physics` + `easing` + `exit-faster-than-enter` |
| 表单 UX 差 | 快速参考 §8: `inline-validation` + `error-clarity` + `focus-management` |
| 导航感觉混乱 | 快速参考 §9: `nav-hierarchy` + `bottom-nav-limit` + `back-behavior` |
| 小屏幕布局破坏 | 快速参考 §5: `mobile-first` + `breakpoint-consistency` |
| 性能/卡顿 | 快速参考 §3: `virtualize-lists` + `main-thread-budget` + `debounce-throttle` |

### 交付前检查清单

- 运行 `--domain ux "animation accessibility z-index loading"` 作为 UX 验证
- 通读快速参考 **§1–§3**（关键 + 高）作为最终审查
- 在 375px（小手机）和横屏方向上测试
- 在启用 **reduced-motion** 和 **Dynamic Type** 最大尺寸下验证行为
- 独立检查暗色模式对比度（不要假设浅色模式值可用）
- 确认所有触控目标 ≥44pt 且无内容隐藏在安全区域外

---

## 专业 UI 的常见规则

这些是常被忽视的问题，会影响 UI 的专业性：
范围说明：以下规则适用于 App UI（iOS/Android/React Native/Flutter），不适用于桌面 Web 交互模式。

### 图标和视觉元素

| 规则 | 标准 | 避免 | 为什么重要 |
|------|----------|--------|----------------|
| **不用 Emoji 作为结构图标** | 使用矢量图标（如 Lucide、react-native-vector-icons）| 使用 emoji（🎨 🚀 ⚙️）作为导航、设置或系统控制 | Emoji 依赖字体，跨平台不一致，无法通过设计令牌控制 |
| **仅使用矢量资源** | 使用 SVG 或平台矢量图标 | 使用模糊或像素化的栅格 PNG 图标 | 确保可扩展性、清晰渲染和暗色模式适应性 |
| **稳定的交互状态** | 使用颜色、不透明度或elevation过渡进行按下状态，不改变布局边界 | 移动周围内容的布局偏移变换 | 防止不稳定交互并保持移动端流畅动效/感知质量 |
| **正确的品牌 Logo** | 使用官方品牌资产并遵循使用指南 | 猜测 logo 路径、非官方重新着色或修改比例 | 防止品牌滥用并确保法律/平台合规 |
| **一致的图标尺寸** | 将图标尺寸定义为设计令牌（如 icon-sm、icon-md = 24pt）| 随意混用 20pt / 24pt / 28pt | 保持整个界面的节奏和视觉层次 |
| **笔触一致性** | 在同一视觉层内使用一致的笔触宽度（如 1.5px 或 2px）| 随意混用粗细笔触样式 | 不一致的笔触降低感知精致度和凝聚力 |
| **填充 vs 描边纪律** | 在同一层次级别使用一种图标样式 | 在同一层次级别混用填充和描边图标 | 保持语义清晰和风格一致 |
| **触控目标最小值** | 最小 44×44pt 交互区域（如果图标较小使用 hitSlop）| 无扩展点击区域的小图标 | 满足无障碍和平台可用性标准 |
| **图标对齐** | 将图标与文本基线对齐并保持一致的内边距 | 图标未对齐或其周围间距不一致 | 防止微妙的视觉不平衡，降低感知质量 |
| **图标对比度** | 遵循 WCAG 对比度标准：小元素 4.5:1，较大 UI 符号 3:1 | 与背景融合的低对比度图标 | 确保浅色和暗色模式下的无障碍访问 |

### 交互（App）

| 规则 | 做 | 不做 |
|------|----|----- |
| **点击反馈** | 在 80-150ms 内提供清晰的按下反馈（涟漪/不透明度/elevation）| 点击无视觉响应 |
| **动画时间** | 微交互保持在 150-300ms，带平台原生缓动 | 瞬时过渡或慢动画（>500ms）|
| **无障碍焦点** | 确保屏幕阅读器焦点顺序匹配视觉顺序且标签有描述性 | 无标签控件或混乱的焦点遍历 |
| **禁用状态清晰度** | 使用禁用语义（disabled/原生 disabled props）、降低强调且无点击操作 | 看起来可点击但什么都不做的控件 |
| **触控目标最小值** | 保持点击区域 >=44x44pt iOS，>=48x48dp Android | 小的点击目标或无内边距的图标仅点击区域 |
| **手势冲突预防** | 每个区域保持一个主要手势，避免嵌套/冲突的点击/拖动交互 | 导致意外操作的嵌套手势 |
| **语义原生控件** | 优先使用原生交互原语（Button、Pressable、平台等价物）及适当的无障碍角色 | 使用通用容器作为主要控件，无语义 |

### 浅色/暗色模式对比度

| 规则 | 做 | 不做 |
|------|----|----- |
| **表面可读性（浅色）** | 保持卡片/表面与背景充分分离 | 过度透明的表面模糊层次结构 |
| **文本对比度（浅色）** | 浅色表面上保持正文文本对比度 >=4.5:1 | 低对比度灰色正文文本 |
| **文本对比度（暗色）** | 暗色表面上保持主要文本对比度 >=4.5:1，辅助文本 >=3:1 | 与背景融合的暗色模式文本 |
| **边框和分隔线可见性** | 确保分隔线在两种主题中都可见（不仅是浅色模式）| 在一种模式中消失的主题特定边框 |
| **状态对比度 parity** | 在浅色和暗色主题中保持按下/聚焦/禁用状态可区分 | 仅定义一种主题的交互状态 |
| **令牌驱动的主题** | 使用映射到每主题的语义色彩令牌 | 硬编码每屏幕十六进制值 |
| **遮罩和弹窗可读性** | 使用足够强的弹窗遮罩以隔离前景内容（通常 40-60% 黑色）| 弱遮罩使背景视觉竞争 |

### 布局与间距

| 规则 | 做 | 不做 |
|------|----|----- |
| **安全区域合规** | 为所有固定 header、tab bar 和 CTA bar 尊重 top/bottom 安全区域 | 将固定 UI 放在刘海、状态栏或手势区域下 |
| **系统栏间隙** | 为状态/导航栏和手势 home 指示器添加间距 | 让可点击内容与 OS chrome 碰撞 |
| **一致的内容宽度** | 保持每种设备类（手机/平板）的可预测内容宽度 | 屏幕间混合任意宽度 |
| **8dp 间距节奏** | 使用一致的 4/8dp 间距系统用于内边距/间隙/部分间距 | 无节奏的随机间距增量 |
| **可读文本度量** | 在大设备上保持长文本可读（平板上避免边到边段落）| 大设备上伤害可读性的全宽长文本 |
| **部分间距层次** | 定义清晰的垂直节奏层（如 16/24/32/48）按层次 | 类似 UI 级别的间距不一致 |
| **按断点自适应gutters** | 在更大宽度和横屏上增加水平内边距 | 所有设备尺寸/方向上相同的窄 gutter |
| **滚动和固定元素共存** | 添加 bottom/top 内容 inset 使列表不被固定 bars 隐藏 | 滚动内容被 sticky headers/footers 遮挡 |

---

## 交付前检查清单

交付 UI 代码前，验证以下项目：
范围说明：此检查清单适用于 App UI（iOS/Android/React Native/Flutter）。

### 视觉质量
- [ ] 不使用 emoji 作为图标（使用 SVG 代替）
- [ ] 所有图标来自一致的图标系列和风格
- [ ] 使用正确比例和留白空间的官方品牌资产
- [ ] 按下状态视觉不移动布局边界或导致抖动
- [ ] 一致使用语义主题令牌（无临时每屏幕硬编码颜色）

### 交互
- [ ] 所有可点击元素提供清晰的按下反馈（涟漪/不透明度/elevation）
- [ ] 触控目标满足最小尺寸（>=44x44pt iOS，>=48x48dp Android）
- [ ] 微交互时间保持在 150-300ms 范围内，带原生感缓动
- [ ] 禁用状态视觉清晰且不可交互
- [ ] 屏幕阅读器焦点顺序匹配视觉顺序，交互标签有描述性
- [ ] 手势区域避免嵌套/冲突交互（点击/拖动/返回滑动冲突）

### 浅色/暗色模式
- [ ] 浅色和暗色模式中主要文本对比度 >=4.5:1
- [ ] 浅色和暗色模式中辅助文本对比度 >=3:1
- [ ] 分隔线/边框和交互状态在两种模式中可区分
- [ ] 弹窗/drawer 遮罩不透明度足以保持前景可读性（通常 40-60% 黑色）
- [ ] 两种主题都在交付前测试（不从单一主题推断）

### 布局
- [ ] Header、tab bar 和 bottom CTA bar 尊重安全区域
- [ ] 滚动内容不被固定/sticky bars 遮挡
- [ ] 在小手机、大手机和平板上验证（竖屏 + 横屏）
- [ ] 水平 inset/gutter 按设备尺寸和方向正确自适应
- [ ] 组件、部分和页面级别维护 4/8dp 间距节奏
- [ ] 较大设备上长文本度量保持可读性（无边到边段落）

### 无障碍访问
- [ ] 所有有意义图片/图标有辅助标签
- [ ] 表单字段有标签、提示和清晰的错误消息
- [ ] 色彩不是唯一指示器
- [ ] 支持 reduced motion 和动态文本大小，无布局破坏
- [ ] 正确宣布辅助功能 traits/roles/states（selected、disabled、expanded）
