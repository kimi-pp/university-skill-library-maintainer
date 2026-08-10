# 硕士学位论文评审技能 (Thesis Review Skill)

## 概述

这是一个用于全面评审中文硕士学位论文的技能，检查格式规范、语言质量、学术内容、结构组织和参考文献等方面的问题。

## 功能特性

### 格式检查
- 中英文标点符号混用检测
- 表格中小数位数过多检查（通常保留2位）
- 标题层级和编号连续性检查

### 语言与逻辑检查
- 段落连贯性分析
- 逻辑矛盾检测
- 语言流畅度评估

### 学术内容检查
- 统计表达正确性（p值格式、显著性表述）
- 图表标题清晰度
- 图表编号连续性
- 统计术语准确性

### 结构检查
- 摘要平衡性（避免"头重脚轻"）
- 方法部分逻辑顺序
- 标题与内容对齐度
- 子标题合理性

### 参考文献检查
- 参考文献编号连续性
- 格式一致性检查

## 使用方法

### 基本使用

```bash
python thesis_review.py
```

默认输入文件：`test_files/thesis.docx`
默认输出目录：`thesis-review-workspace/iteration-1/eval-comprehensive-review/with_skill/outputs/`

### 测试样本论文

```bash
python test_comprehensive.py
```

使用包含故意设计问题的样本论文进行测试，展示完整的评审功能。

### 生成测试文件

```bash
python scripts/generate_test_docx.py
```

生成包含各种常见问题的测试论文文件。

## 输出格式

评审结果以Word文档形式输出，包含以下部分：

1. **总体评价**
   - 主要优点
   - 主要问题统计
   - 修改优先级分布

2. **具体问题及修改建议**
   - 格式问题
   - 语言与逻辑问题  
   - 学术内容问题
   - 结构问题
   - 参考文献问题

3. **关键修改项 (Top 10)**
   - 按优先级排序的前10个关键问题

4. **鼓励与肯定**
   - 论文做得好的方面

## 技术要求

- Python 3.6+
- python-docx 库
- 支持中文编码的环境

### 安装依赖

```bash
pip install python-docx
```

## 文件结构

```
thesis-review/
├── thesis_review.py          # 主评审脚本
├── test_comprehensive.py     # 测试脚本
├── scripts/
│   └── generate_test_docx.py # 测试文件生成脚本
├── test_files/
│   ├── thesis.docx          # 简单测试论文
│   ├── thesis_sample.docx   # 包含问题的样本论文
│   └── 论文终稿.docx        # 中文名称测试文件
├── thesis-review-workspace/
│   └── iteration-1/
│       └── eval-comprehensive-review/
│           └── with_skill/
│               └── outputs/  # 评审结果输出目录
└── SKILL.md                  # 技能定义文件
```

## 示例输出

运行 `test_comprehensive.py` 对样本论文的评审结果：

```
开始论文评审...
评审完成，共发现25个问题
评审意见已保存至: thesis-review-workspace/.../sample_thesis_review_20260413_145347.docx

============================================================
样本论文评审完成!
输入文件: test_files/thesis_sample.docx
输出文件: thesis-review-workspace/.../sample_thesis_review_20260413_145347.docx
发现问题: 25个
============================================================

按类别统计:
  formatting: 7个问题
  academic_content: 15个问题
  structure: 3个问题

高优先级问题:
  - 标题编号不连续: 3.1 后应为 2，实际为 3.3 (标题: 3.3 模型评估)
  - 标题编号不连续: 3.3 后应为 4，实际为 3.2 (标题: 3.2 模型构建)
  - 标题中的关键词"人工智能在医疗诊断中的应用研究"在正文前部出现频率较低 (论文标题)

中优先级问题 (示例):
  - 中英文标点符号混用 (Paragraph 8)
  - 中英文标点符号混用 (Paragraph 20)
  - 中英文标点符号混用 (Paragraph 38)

做得好的方面:
  - 章节结构明确，标题层次清晰
  - 包含数据表格，增强论证说服力
  - 包含参考文献部分，体现学术规范
```

## 自定义使用

要评审自己的论文，可以修改 `thesis_review.py` 中的文件路径：

```python
# 修改输入文件路径
input_path = "path/to/your/thesis.docx"

# 修改输出目录
output_dir = "path/to/output/directory/"
```

## 注意事项

1. 技能主要针对中文硕士学位论文设计
2. 部分检查基于启发式规则，可能需要人工复核
3. 参考文献真实性验证需要网络连接和WebSearch工具支持
4. 统计表达检查遵循一般学术规范，具体学科可能有特殊要求

## 开发说明

技能基于 `python-docx` 库实现文档解析，使用正则表达式进行模式匹配，采用模块化设计便于扩展新的检查规则。