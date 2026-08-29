# 项目执行契约

仅在运行、排障或审核本工作流时读取本文件。现行项目规则优先于本摘要。

## 持久化与范围

- `workflow-settings.toml` 只保存配置；Excel 主台账保存当前 Skill、来源别名、专业任务映射、版本历史、候选观察、目录基线、来源水位和运行记录。
- 不创建 SQLite、Access、JSON/CSV 业务仓或后台数据库。
- 范围只含 13 个非军事学门类及 `99 跨学科通用`；同一稳定 ID 全局只保存一次，可映射多个专业范围。
- 正式推荐至少达到“全部通过（未实测）”。条件候选与需适配候选只进入对应查验区。

## 阶段与证据

`run-now` 与 `scheduled-run` 必须在同一长驻进程内持有单写者锁和瞬态 capability，顺序固定为：

1. `prepare` 在本轮私有暂存目录获取来源证据与固定包，发出 `material_review_required`；
2. Codex 只读检查固定包并回传与 run ID、版本、canonical source、内容哈希精确绑定的 `material_observations`；
3. 进程消费仍在内存中的快照 capability，构建可信 ReviewPacket，再发出 `review_required`；
4. Codex 依据项目规则与专业六维画像回传项目判断和 ledger row；
5. `finalize` 完成 Office 复读并发出逐页视觉闸，批准后才原子发布。

不得跨进程调用 `prepare`、`apply-reviews`、`finalize`，不得从磁盘恢复 capability。市场元数据或搜索响应 JSON 不得冒充 Skill 固定包；无法取得完整固定包的市场或 Hugging Face 条目只进入候选观察。

任一证据缺失、身份或哈希变化、Office 复读失败、逐页拒绝或发布冲突都保留旧 authority，不得留下半提交代次。

## Word 渲染依赖

Task 11 的 `RendererCommand` 接受显式 `argv`，随后自动追加 `--pdf ABSOLUTE` 与 `--output-dir ABSOLUTE`。项目自带入口为 `07_自动维护工作流/src/skill_maintainer/pdf_renderer.py`；它接收这两个参数以及基础 argv 中的 `--python-packages`、`--pdftoppm`，stdout 只返回一行 UTF-8 JSON，并按序列出 `page-1.png` 等页面及每页 `body_nonwhite_pixels`。

每次运行先调用 Codex 工作区依赖加载器（`load_workspace_dependencies`）。加载器返回 Python executable、Python packages、override binaries 和 fallback binaries，不直接返回渲染命令。把原始加载器文本与绝对项目根传入 `build_workspace_renderer_command(loader_output, project_root)`；该接口验证字段完整、绝对普通路径、共同运行时根和项目入口，沿加载器目录中的固定 `pdftoppm.cmd` 包装链解析同一运行时内的 `pdftoppm.exe`/`pdfinfo.exe`，然后构造：

```text
RendererCommand.argv = (
  <loader Python>, <project>/07_自动维护工作流/src/skill_maintainer/pdf_renderer.py,
  --python-packages, <loader Python packages>,
  --pdftoppm, <loader-contained pdftoppm.exe>
)
```

渲染入口拒绝相对路径、链接/重解析点、非普通 PDF、非空输出目录、越界页面名和缺失依赖；失败返回非零且不输出成功 JSON。不得从默认 PATH、用户名或缓存目录结构猜测任何路径；字段、入口或依赖不可用时停止发布。

## 自动任务契约

自动任务提示词只绑定：

1. 绝对项目根；
2. 绝对 TOML 路径；
3. 已应用 TOML SHA-256；
4. 固定 Skill 命令 `scheduled-run`。

不接受目标、平台或专业范围覆盖。`apply-settings` 由代理先调用本地 CLI 做验证，再使用应用的自动任务更新工具；禁止生成原始指令文本冒充工具调用。更新后必须回读并核对项目、计划、提示词和哈希。

## 退出与通知

| 情况 | 处理 |
|---|---|
| 锁冲突、间隔未到或无变化 | 安全无操作；无变化成功不通知 |
| 配置未应用、禁用或手动 | 不联网、不研究、不发布 |
| 专业目录门变化 | 先重建范围合同，再恢复发现 |
| 单平台失败 | 继续其他平台并标记覆盖降级 |
| 全来源或关键验证失败 | 保留旧台账，通知失败 |
| 有正式变化或人工决定事项 | 发布验证通过的交付并通知摘要 |
