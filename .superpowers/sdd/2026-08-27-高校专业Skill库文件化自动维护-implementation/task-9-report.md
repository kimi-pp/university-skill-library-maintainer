# Task 9 实施报告：单写者暂存运行协调器（复审修订）

## 交付

- `paths.py`：项目根目录约束、路径注入防护，以及符号链接/Windows 重解析点拒绝。
- `locking.py`：基于 `msvcrt.locking` 的项目级非阻塞单写者锁；锁文件内容仅作 PID/时间诊断，不作为所有权判断。
- `runner.py`：`prepare`、`apply_reviews`、`finalize` 三阶段协调器；报告与 Office 校验均为仅接收暂存路径的注入回调，未实现 Task 10 的真实文档生成。
- `test_runner.py`：33 个面向安全契约的回归测试。

## 安全与状态契约

- 发现的规范候选和人工去重项完整写入暂存 `候选观察`；未完成 Task 7 审查不得进入 `当前Skill`，且来源别名必须引用既有正式稳定 ID。
- 已有正式条目的新版本审查先在影子台账取得 Task 7 回执和拟议行，`finalize` 才调用 versioning 的完整事务；`apply_reviews` 不提前改写当前版本。
- 生产主台账是唯一提交线：完整不可变 generation（含 manifest）在同目录临时目录就绪后改名；暂存台账写入成功运行记录、delivery hash 与 manifest hash 并复读；最后只原子替换主台账。不写 `current-generation.json`，提交前异常清理本 run generation；下次同 run-id 仅在 manifest、树哈希和生产账本均证明其为无权威 orphan 时才回收。
- 报告/交付回调输出限定在当前 run 的暂存目录；回调和 Office 返回后、generation 复制后、提交前都复核普通文件、链接/重解析点和树哈希。generation authority hash 明确排除 manifest 本身，避免自哈希循环。
- generation manifest 还列出每个 authority 文件的相对路径、字节哈希与文件身份。Windows 在生产台账替换的提交边界持有 manifest、authority 文件及目录的 deny-write/delete HANDLE，并在 HANDLE 仍有效时从路径与 HANDLE 双重重验后提交；新出现的未列文件会被 authority 校验拒绝。
- ledger `os.replace` 后立即标记 committed；即使测试或运行时在该调用已完成但尚未返回时抛出 `BaseException`，也会通过生产账本字节、成功运行记录与 generation authority 识别已线性化的提交，仅作不删除 generation 的终结清理，绝不把已提交 generation 当作回滚对象。
- 回调返回后先逐组件核验 artifact 的 lexical 父链、resolved 根目录和普通文件属性，并扫描整棵暂存树；因此 Office 校验不会接触 junction/reparse 指向的外部内容。
- 启动会校验生产账本最后一次成功运行记录所指的 generation、manifest 和 delivery hash；缺失、哈希不符、重解析点或路径穿越均阻断，避免在损坏权威状态上继续发现。
- 对 settings、目录快照、来源快照、暂存树和生产台账基线执行哈希绑定；任一 TOCTOU 变化会拒绝继续。
- 来源集合必须精确为四个平台；含候选的 `complete`/`partial` 批次需绑定普通证据文件的字节与文件身份。仅 `complete` 来源写入水位。四个平台全失败只在暂存目录写失败报告，绝不发布业务变更。
- 成功、失败及放弃路径均释放 OS 锁并清理本 run 的 Task 7 瞬态 registry；清理只允许确切拥有的普通暂存目录。一个项目终结不会清除同解释器另一项目的审查包。

## TDD 与验证证据

1. 初始 RED：`ModuleNotFoundError: No module named 'skill_maintainer.locking'`。
2. 复审 RED：generation 复制后回调遗留写入会错误放行；成功账本所指 generation 缺失会错误启动；`prepare` 的 `SystemExit` 遗留 staging；包含 `../../` 的有效外部 generation 会被账本路径接受；同 run-id 的无权威 orphan 不会回收。
3. 最终复审 RED：ledger 原子替换边界仍可写 generation report；finalize 预检的 `SystemExit` 遗留状态和锁；callback junction 在 Office 前被调用。
4. 补充 RED：生产 ledger `os.replace` 已成功后抛出的 `SystemExit` 删除了已被成功运行记录引用的 generation。
5. 聚焦测试：`python -m unittest 07_自动维护工作流/tests/test_runner.py -v`，33/33 通过。
6. 完整工作流：`python -m unittest discover -s 07_自动维护工作流/tests -p test_*.py`，163/163 通过。
7. 编译：`python -m compileall -q 07_自动维护工作流/src 07_自动维护工作流/tests` 成功。
8. `git diff --check` 无空白错误。

## 范围边界

未修改 `cli.py`；未联网；未安装或执行候选；未提前实现 Task 10 的真实 Word/Excel 生成或 Office 自动化。
