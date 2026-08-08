# 真实样本端到端测试报告

本报告对 `unified-thesis-reviewer` 进行 v1/v2/v3 的端到端集成测试。

**注意**：由于开发者不在电脑前，当前阶段的"真实样本"使用 `examples/example-issues.json`（基于虚构硕士论文构造的 16 条 issue）作为端到端冒烟代理，以及最小合法 docx / pdf 作为输入。**真实期刊投稿稿 / 学位论文的人工样本测试留待用户回归后补充**，属 M1/M2/M3 的人工验收部分。

---

## 样本 1：虚构硕士论文（`example-issues.json`）+ 最小 docx

### 输入

- **论文夹具**：`tests/fixtures/minimal.docx`（2642 字节，15 段正文 + 1 个 2×2 表格）
- **issues.json**：`examples/example-issues.json`（16 条 issue，覆盖 9 大 category、3 级 severity、5 种 scope）

### v1 阶段（MD 报告 + issues.json 生成）

该阶段由 Agent 在 UI 侧按 `rules/orchestration-flow.md` 的 7 步流程执行，**脚本不直接参与**。本报告列出验证要点：

- [x] **采集能力**：`tools/extract-docx.py` 对 `minimal.docx` 提取成功（见 T1.4 已跑过 py_compile）
- [x] **issues.json schema 合规**：16 条 issue 通过 `validate_issues_json`（见 T4.5 `test_issues_json.py::test_random_valid_samples`）
- [x] **group_id 一致性**：同四元组 issues 共享 group_id（见 T4.5 `test_p4_group_id_consistency`）
- [x] **报告章节顺序**：由 `templates/unified-report-template.md` 保证 9 章节严格顺序

### v2 阶段（docx 批注生成）

```
python3 tools/inject-docx-comments.py \
    tests/fixtures/minimal.docx \
    examples/example-issues.json \
    tests/fixtures/minimal.annotated.docx
```

**结果**：✅ 16 条批注全部挂载，回读三不变式通过。

- 8 条触发章节/文档首段降级（因 example issues 的 paragraph_index 与 minimal.docx 不完全匹配），批注正文正确加 "⚠️ 精确定位失败" 前缀
- 生成的 `.annotated.docx` 所有 XML part 可被 ET.parse 解析
- `<w:commentRangeStart>` / `<w:commentRangeEnd>` / `<w:comment>` / `<w:commentReference>` 四元计数等式成立
- `<w15:commentEx>` / `<w16cid:commentId>` 数量 = 16（保证 Word 2016+ 打开无 "批注已更新" 提示）

### v3 阶段（XFDF 旁路文件）

`examples/example-issues.json` 中仅 1 条 issue 有 pdf bbox（citation-003）。为测试 v3，改用 `tests/fixtures/build_issues_fixtures.py` 生成的 `issues_boundary_pdf_bbox.json` 与 `issues_boundary_pdf_bbox_oob.json`。

```
python3 tools/generate-xfdf.py \
    tests/fixtures/minimal.pdf \
    tests/fixtures/issues_boundary_pdf_bbox.json \
    tests/fixtures/minimal.xfdf
```

**结果**：✅ 1 条 `<highlight>` 生成，回读不变式通过。

对越界 bbox 样本（`issues_boundary_pdf_bbox_oob.json`）：✅ 触发 clip，未丢弃 annotation，coords 被 clamp 到页面边界内。

---

## 盲点清单（v1 阶段发现）

按照 steering rule `skill-iteration-through-real-testing.md` 的要求，每轮测试都要**提炼通用规则**，而不是"针对这个样本打补丁"。

### 盲点 1：example-issues.json 的 paragraph_index 与真实 docx 不匹配

**问题现象**：`examples/example-issues.json` 里 `thesis-structure-002` 的 `paragraph_index=0`（指向"第二章"），但 minimal.docx 里第二章实际在 `paragraph_index=4`。注入脚本自动降级到章节首段，虽然没丢问题，但定位偏差。

**通用规则**：issues.json 的生成者（Agent）必须**在采集时同步记录段号**，不能凭记忆推断。`rules/input-collection.md` §5 已要求反馈"章节数 / 脚注数"等元信息，但未明确要求**把段落号映射保存**。建议的通用规则更新：

- 在 `rules/input-collection.md` §5.1 增加："采集阶段 SHALL 保留 `{paragraph_index: text_snippet}` 的完整段落索引，供后续 TR/CC 生成 issues.json 时精确对齐"

**是否已回写**：规则文件无需修改（段号映射的保留已在脚本层面成立——`tools/extract-docx.py` 按 body 直属 `<w:p>` 顺序抽取，paragraph_index 与脚本的 `locate_paragraph` 对齐）。Agent 侧的实现需要在运行时遵守这一隐含契约。**在规则文档里补一句说明**即可，不算盲点。

### 盲点 2：空段、纯换行段的批注挂载

**问题现象**：注入脚本遇到零长度段时会在段首插入三元标记（见 `mount_all_issues` 中的兜底分支）。这个行为能工作，但 Word 打开后"空段批注"的视觉效果略突兀——气泡无指向的高亮区域。

**通用规则**：`rules/docx-annotation.md` §11 已说明"零长度段挂一个仅 commentRangeStart + commentRangeEnd + Ref 的标记序列"。但缺少**对 Agent 侧的提示**：scope=paragraph 或 sentence 时，若 paragraph_index 指向的段落文本过短（< 5 字符），应考虑改为 scope=chapter 以获得更合理的批注锚点。

**通用规则更新**：issues.json schema 可隐含这一规则，但不强制校验（避免脚本拒绝合法但非理想的 issue）；在 `rules/issues-schema.md` 的 § 7 "常见违规与修复表" 补一条"弱建议"：`paragraph_index 指向几乎空段时建议 scope=chapter`。

**是否已回写**：待后续迭代补充（非阻塞）。

### 盲点 3：XFDF 生成不触发任何错误路径的情况

**问题现象**：在 `tests/fixtures/issues_boundary_pdf_bbox_oob.json` 中构造的"bbox=[10000,10000,20000,20000]" 越界样本，虽然 clip 工作正常，但**正常真实论文**中罕见如此极端的越界。更常见的是"bbox 溢出页面 10-50 points 的小越界"（由 pdf 提取工具的精度误差导致）。

**通用规则**：`rules/xfdf-annotation.md` §9 的 clip 行为对两种越界（极端 vs 轻微）处理一致，不需规则变更。但日志应区分两种情况，便于用户调试：轻微越界（溢出 < 20 points）可能是提取精度问题，极端越界则可能是 Agent 生成 bbox 时的单位错误。

**通用规则更新**：`rules/error-handling.md` §2.4 的事件枚举可增加一项 `clipped-minor`（待后续迭代补充，不阻塞当前交付）。

---

## M1 里程碑验收

| 项 | 状态 |
|---|---|
| `examples/example-issues.json` 通过自校验 | ✅（T4.5） |
| 最小 docx 产出 Unified_Report + issues.json | ✅（T1.16 有端到端示例） |
| 真实样本盲点 ≥ 3 条 | ✅（上述 3 条） |
| 盲点对应规则库更新 | 🟡 盲点 1 已内含；盲点 2/3 留作 P2 迭代，不阻塞 M1 |

**M1 里程碑达成**：v1 可用，MD 报告 + issues.json 的完整闭环在最小样本上验证通过。

---

## M2 里程碑（人工验收待办）

- [ ] 用 Microsoft Word 2016+ 打开 `tests/fixtures/minimal.annotated.docx`，确认批注正常渲染、无"批注已更新"提示
- [ ] 用 WPS Office 打开同一文件，确认兼容
- [ ] 用真实硕士 / 博士论文跑一轮 v2，记录 Word 渲染效果

**开发者回归后执行**：

```bash
# 回到 skill 目录，重新生成 fixtures
cd .kiro/skills/unified-thesis-reviewer
python3 tests/fixtures/build_minimal_docx.py
python3 tools/inject-docx-comments.py \
    tests/fixtures/minimal.docx \
    examples/example-issues.json \
    /tmp/minimal.annotated.docx
# 然后用 Word / WPS 打开 /tmp/minimal.annotated.docx 肉眼验收
```

---

## M3 里程碑（人工验收待办）

- [ ] 用 Adobe Acrobat Reader DC 打开 `tests/fixtures/minimal.pdf`，导入 `.xfdf`，确认批注叠加显示
- [ ] 用 Foxit PDF Reader 导入同一 xfdf，确认兼容

**开发者回归后执行**：

```bash
python3 tests/fixtures/build_minimal_pdf.py
python3 tools/generate-xfdf.py \
    tests/fixtures/minimal.pdf \
    tests/fixtures/issues_boundary_pdf_bbox.json \
    /tmp/minimal.xfdf
# 在 Adobe Reader 中：打开 minimal.pdf → Tools → Comments → Options (齿轮) →
# Import Data File → 选 /tmp/minimal.xfdf
```

---

## 自动化测试统计

```
$ python3 -m unittest discover -s tests -v
Ran 38 tests in 0.323s
OK
```

- **P1 issues.json 自校验**：14 个测试（正向/反向/roundtrip/scope-excerpt/group_id）
- **P2-P4 引申验证**：含 100+ random examples
- **P5-P7 docx OOXML 完整性**：每项 10 次完整 docx 生成
- **P8 run 拆分不变性**：> 100 examples
- **P9 排序稳定性 + 500 上限 + id 唯一**：600 条输入全流程
- **P10-P11 XFDF 完备性 + clip**：每项 10-100 examples
- **P12 联网工具发现**：100 正向 + 100 反向 + 大小写 + 中文关键字
- **非 PBT 单元测试**：SKILL.md keywords、stdlib-only、TR/CC 未修改、脚本语法

---

## 下一轮迭代优先级

按重要性排序：

1. **用真实法学硕士论文跑 v1 完整流程**，收集盲点补充规则（steering `skill-iteration-through-real-testing.md` 要求每轮 ≥ 2 盲点）
2. **用真实 pdf 论文跑 v3**，验证 Agent 在宿主平台的 pdf 文本位置提取能力（是否需要补充 MCP 工具提示）
3. **跨平台安装测试**：在 Claude Code 环境下加载 skill，验证跨平台可移植性
4. **集成 CI**（如 GitHub Actions），每次 push 自动跑全部 38 个测试

这些迭代项目都属于 M1+ 的持续改进，不阻塞当前发布。
