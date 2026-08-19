---
name: probability-stochastic-information
description: Use when writing, revising, or checking the rigorous Chinese Markdown textbook books/probability-stochastic-information on measure-theoretic probability, stochastic processes, entropy, divergence, channels, coding, and asymptotic information. Enforces explicit measurable objects, theorem/proof boundaries, external input registration, and closed internal dependency tracking.
---

# 《概率、随机过程与信息论：从测度到熵》写作规范

本文件约束 `books/probability-stochastic-information/` 的写作、扩写和校订。全书服从上级 OET 本体严格性标准，并在概率与信息论语境中采用以下局部规则。

## 1. 对象与类型

- 每个概率论对象先声明可测空间、概率空间、随机变量、过程索引集或核的定义域和值域。
- “分布”只指推前测度；“密度”只在指定参考测度并声明绝对连续后使用。
- “过程”是映射族 $(X_t)_{t\in T}$，不是一条样本路径；样本路径是 $\omega\mapsto (X_t(\omega))_{t\in T}$ 的值。
- “条件分布”必须区分抽象条件期望、有限/可数条件概率和正则条件分布核。
- 信息论量先在有限或可数字母表上定义；推广到一般空间时必须说明参考测度、可测性和无穷值。
- 编码定理、遍历定理与一般 AEP 不得伪装成书内短证明。

## 2. 主张终态

每个非平凡主张必须以以下状态之一结束：

1. **书内定理**：给出完整证明；
2. **外部输入定理**：说明精确版本、用途、来源和未重证原因；
3. **推导或计算**：列出起点、等式变形和适用条件；
4. **模型假设或边界说明**：明确不把它当成数学定理。

正文可以使用“外部输入”作为证明边界，但必须能在 [SOURCES.md](SOURCES.md) 和 [THEOREM_INDEX.md](THEOREM_INDEX.md) 中定位。

## 3. 证明责任

- 书内主线包括：测度基本性质、推前分布、期望的线性与单调性接口、Markov 与 Chebyshev 不等式、有限独立乘积计算、条件期望的唯一性与塔性质、弱大数律、Chapman--Kolmogorov 方程、Gibbs 不等式、log-sum 不等式、数据处理不等式的有限版本、Fano 不等式的有限版本、前缀码长度下界、有限 Markov 链熵率公式。
- 外部输入包括：Caratheodory 扩张、Radon--Nikodym、Fubini--Tonelli、Kolmogorov 扩张、正则条件分布存在、强大数律、中心极限定理、Birkhoff 遍历定理、Shannon--McMillan--Breiman 定理、Shannon 信道编码定理。
- 边界情形必须处理：零概率事件、$0\log 0$、无穷期望、非绝对连续分布、非标准 Borel 空间上的正则条件分布失败、非平稳过程的熵率不存在、最大概率并列和容量未达成。

## 4. 叙事与编号

- 章节文件使用两位编号，附录使用大写字母。
- 定义、定理、命题、引理、推论、例、练习使用稳定编号，例如 `定义 4.2`。
- 不使用模板式“本章目标”“依赖”“本章小结”栏目。
- 每章开头从一个数学现象、计算或反例进入；章内至少有一个完整例子或计算。
- 每道练习在 [SOLUTIONS.md](SOLUTIONS.md) 中有答案或完整解题要点。

## 5. 修改后检查

推荐检查：

```bash
python3 books/audit_textbook_narrative.py probability-stochastic-information --strict
git diff --check
```

由于当前 OET 结构审计脚本的书目白名单未包含本目录，若不修改仓库脚本，应使用同等规则对本目录逐文件检查定理边界、围栏和本地链接。
