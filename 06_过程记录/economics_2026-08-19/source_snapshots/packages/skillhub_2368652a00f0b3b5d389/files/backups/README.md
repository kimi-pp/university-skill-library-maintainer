# backups / 备份快照目录

> Runtime-generated directory. **Do NOT pre-populate by hand** — every snapshot is
> produced automatically by `scripts/self_iterate.py` before an L2+ (or any applied)
> change, or via a baseline snapshot taken at first-run bootstrap.
> 运行时目录。**请勿手工预填**——每个快照都由 `scripts/self_iterate.py` 在 L2+（或任何落地）
> 变更前自动生成，或于首次运行引导时做基线快照。

---

## EN · Purpose / 用途
Pre-apply point-in-time snapshots so every L0–L3 change is **reversible in one command**.
The self-iteration engine writes here immediately before modifying any content file, then
records the action in the tamper-evident hash chain (`scripts/hash_chain.jsonl`). A failed
golden-QA regression or a human-reported bad answer triggers a restore from the matching
snapshot (see `playbooks/11` §4 and `tools/09`).

## 中文 · 用途
变更前的时间点快照，使每次 L0–L3 变更**一键可回滚**。自迭代引擎在改动任何内容文件前
立即写入此处，并向防篡改哈希链（`scripts/hash_chain.jsonl`）记账。黄金问答回归不及格或人工
报坏答案时，从对应快照恢复（见 `playbooks/11` §4 与 `tools/09`）。

---

## EN · Naming convention / 命名规范
Each snapshot is a directory named by UTC-local timestamp:

    backups/YYYY-MM-DD-HHMM/

Example: `backups/2026-07-28-1430/`. A single run that applies N proposals creates exactly
one such directory containing copies of **only the affected files** (preserving their relative
paths) plus a `manifest.json`.

## 中文 · 命名规范
每个快照目录以时间戳命名：

    backups/YYYY-MM-DD-HHMM/

例：`backups/2026-07-28-1430/`。一次应用 N 个提案只生成一个目录，内含**仅受影响文件**
（保留相对路径）及 `manifest.json`。

---

## EN · manifest.json format / manifest 格式
```json
{
  "run_id": "2026-07-28-1430",
  "created": "2026-07-28T14:30:00",
  "reason": "pre-apply snapshot for 2 proposal(s)",
  "files": ["data/03-software-vendor-directory.md", "references/06-..."]
}
```

## 中文 · manifest 格式
见上。记录本次快照的 `run_id`、生成时间、原因，以及受影响文件相对路径清单。

---

## EN · Retention policy / 保留策略
Keep the **12 most-recent monthly snapshots** plus the **last-known-good** snapshot.
The monthly patrol (`playbooks/11` Phase 0) prunes older ones. Quarantined-change rollbacks
must retain their source snapshot until the change is resolved.

## 中文 · 保留策略
保留**最近 12 个月度快照** + **最后已知良版**。月度巡检（`playbooks/11` 阶段0）清理更旧者。
被隔离变更的回滚源快照须保留至变更解决。

---

## EN · Restore procedure / 恢复步骤
```bash
python3 scripts/self_iterate.py rollback 2026-07-28-1430
```
This copies every file listed in `manifest.json` back to its original location inside the
skill root, then appends a `ROLLBACK` record to the hash chain. The engine never restores
paths that escape the skill root.

## 中文 · 恢复步骤
```bash
python3 scripts/self_iterate.py rollback 2026-07-28-1430
```
将 `manifest.json` 所列文件复制回 skill 根内原位置，并向哈希链追加 `ROLLBACK` 记录。引擎
绝不恢复逸出 skill 根的路径。

> **Honesty red line / 诚实红线**: a rollback is a success of the mechanism, not a failure
> to hide. It is logged openly in the hash chain. / 回滚是机制之成，非需掩盖之败，公开记入哈希链。
