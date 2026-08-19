---
title: algorithmic-art Skill — 原始文档
source: https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/SKILL.md
created: 2026-05-30
tags:
  - skill
  - algorithmic-art
  - p5js
  - generative-art
  - claude-code
---

# Algorithmic Art Skill (SKILL.md)

> 来源：Anthropic Skills 仓库 `skills/algorithmic-art/SKILL.md`
> 捕获时间：2026-05-30（通过 Claude skill 系统加载）
> 用途：指导 Claude 创建算法哲学 + p5.js 生成艺术 + 交互 HTML 制品

---

## 概述

Algorithmic philosophies are computational aesthetic movements that are then expressed through code. Output `.md` files (philosophy), `.html` files (interactive viewer), and `.js` files (generative algorithms).

This happens in two steps:
1. Algorithmic Philosophy Creation (.md file)
2. Express by creating p5.js generative art (.html + .js files)

---

## 第一部分：Algorithmic Philosophy Creation

创建 ALGORITHMIC PHILOSOPHY（非静态图像或模板），通过以下方式诠释：
- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation and controlled chaos

### 关键理解
- **输入**：用户的微妙输入或指令，作为基础但不限制创作自由
- **创建**：一种算法哲学/生成美学运动
- **下一步**：同一版本接收哲学并用代码表达——创建 p5.js 草图，90% 算法生成 + 10% 基本参数

### 如何生成算法哲学

**命名运动**（1-2 词）：如 "Organic Turbulence" / "Quantum Harmonics" / "Emergent Stillness"

**阐述哲学**（4-6 段）：

表达哲学如何通过以下方式在算法上体现：
- 计算过程和数学关系
- 噪声函数和随机模式
- 粒子行为和场动力学
- 时间演化和系统状态
- 参数变化和涌现复杂性

**关键准则**：
- 避免冗余：每个算法方面只提一次
- **反复强调工艺**：最终算法应呈现出经过无数次迭代精心打磨的感觉——"meticulously crafted algorithm"、"painstaking optimization"、"master-level implementation"
- **留出创作空间**：在算法方向上具体，但要足够简洁，让下一个 Claude 有空间做出极高水准的解释性实现选择

### 示例哲学

1. **"Organic Turbulence"** — 受自然法则约束的混沌，从无序中涌现秩序。流场由分层 Perlin 噪声驱动，数千粒子跟随向量力，轨迹积累成有机密度图。

2. **"Quantum Harmonics"** — 离散实体展现波状干涉模式。粒子在网格上初始化，每个携带相位值，通过正弦波演化。简单谐波运动生成复杂的涌现曼荼罗。

3. **"Recursive Whispers"** — 跨尺度的自相似性，有限空间中的无限深度。分支结构递归细分，每次分支略微随机化但受黄金比例约束。

4. **"Field Dynamics"** — 通过物质效应使不可见的力可见。由数学函数或噪声构建的向量场，粒子在边缘诞生，沿场线流动。

5. **"Stochastic Crystallization"** — 随机过程结晶为有序结构。随机圆填充或 Voronoi 镶嵌，通过松弛算法演化。

### 本质原则
- **算法哲学**：创建要通过代码表达的计算世界观
- **过程优于产品**：美从算法执行中涌现——每次运行独一无二
- **参数表达**：思想通过数学关系、力、行为交流——而非静态构图
- **艺术自由**：下一个 Claude 在算法上诠释哲学
- **纯生成艺术**：关于创建活的算法，而非带随机性的静态图像
- **专家工艺**：反复强调最终算法必须感觉精心制作、经过无数次迭代精炼

---

## 第二部分：概念种子推导

**关键步骤**：在实现算法之前，识别原始请求中的微妙概念线索。

**本质原则**：概念是嵌入算法本身的微妙、小众引用——不总是字面的，始终是精致的。熟悉主题的人应该凭直觉感受，而其他人只是体验一件大师级的生成作品。

---

## 第三部分：P5.js 实现

### 步骤 0：先读模板

**在写任何 HTML 之前**：读取 `templates/viewer.html`，研究确切结构、样式和 Anthropic 品牌，将其作为**字面起点**。

**保留**：
- 布局结构（header、sidebar、主画布区）
- Anthropic 品牌（Poppins/Lora 字体、浅色调、渐变背景）
- Sidebar 组织（Seed → Parameters → Colors? → Actions）

**替换**：
- p5.js 算法
- 参数定义
- Parameters 区域 UI 控件

### 技术要求

**种子随机性（Art Blocks 模式）**：
```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

**参数结构**：
```javascript
let params = {
  seed: 12345,
  // 控制算法的参数
  // - Quantities（多少？）
  // - Scales（多大？多快？）
  // - Probabilities（多可能？）
  // - Ratios（什么比例？）
  // - Angles（什么方向？）
  // - Thresholds（行为何时改变？）
};
```

**核心算法**：算法从哲学流出，而非从模式菜单选择。

**工艺要求**：
- **平衡**：有复杂性但无视觉噪声，有秩序但不僵化
- **色彩和谐**：深思熟虑的调色板，非随机 RGB
- **构图**：即使在随机中，保持视觉层次和流动
- **性能**：平滑执行
- **可复现性**：相同 seed 始终产生相同输出

---

## 第四部分：交互制品创建

### 固定 vs 可变

**固定**（始终包含）：
- 布局结构（header、sidebar、主画布区）
- Anthropic 品牌（UI 颜色、字体、渐变）
- Seed 区域：显示 + Prev/Next/Random/Jump + Go
- Actions 区域：Regenerate + Reset + Download PNG

**可变**（每个作品定制）：
- 整个 p5.js 算法
- 参数对象
- Parameters 区域的滑块/控件
- Colors 区域（可选——有些作品用固定色、有些是单色）

### 必需功能

1. **参数控件**：数值滑块、颜色选择器、实时更新、重置按钮
2. **种子导航**：当前种子显示、Prev/Next/Random/Jump、100 变体生成
3. **单一制品结构**：自包含 HTML，p5.js CDN，全部内联

### Sidebar 结构

1. **Seed（固定）**：种子显示 + Prev/Next/Random/Jump
2. **Parameters（可变）**：为该艺术创建控件
3. **Colors（可选/可变）**：可调色时包含
4. **Actions（固定）**：Regenerate + Reset + Download PNG

---

## 第五部分：变体与探索

- 通过种子导航探索变体
- 可添加种子预设按钮
- 可添加 Gallery Mode 显示多种子缩略图
- 全部在同一制品内

---

## 第六部分：创作过程

**用户请求 → 算法哲学 → 实现**

1. 解读用户意图
2. 创建算法哲学（4-6 段）
3. 用代码实现
4. 设计适当参数
5. 构建匹配的 UI 控件

**常量**：Anthropic 品牌、种子导航、自包含 HTML 制品
**变量**：算法本身、参数、UI 控件、视觉结果

---

## 资源

- `templates/viewer.html`：**所有 HTML 制品的必需起点**
- `templates/generator_template.js`：p5.js 最佳实践和代码结构参考

**关键提醒**：模板是起点，不是灵感。算法是你创造独特之物的地方。

---

*原始文档来源：github.com/anthropics/skills · 捕获：Claudian 2026-05-30*
