# Computer-Vision Body / Posture Assessment Pilot / 计算机视觉体态评估试点

> **Cluster / 集群**: E (Data & AI) + F (compliance) + S (health boundary)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Biometric & minors' legal basis re-verify via `tools/05` BEFORE any pilot; vendor CV-accuracy claims 🔄 via `tools/04`.
> **Cross-references / 交叉引用**: `data/09-algorithm-kernel-library.md#algo-cv-posture` · `references/04-ai-application-landscape.md#ai-07-ai-body-assessment` · `references/12-biometrics-and-cctv.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04`/`tools/05` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this pilot charter to scope and safely run a CV-based body/posture assessment** (posture demo, rep counting, or safety monitoring) as an *assist* — never as a medical or coach-replacement tool.
**用本试点章程界定并安全运行「CV 体态评估」**（体态演示、动作计数或安全监控）作为*辅助*——绝不作医疗或教练替代工具。

> **FDMM gate / FDMM 门槛**: Requires **FDMM ≥ L3** with a vendor CV module (do NOT build CV from scratch). The vendor must show evaluation on footage **like your club's** (`data/09#algo-cv-posture`).
> **FDMM 门槛**：需 **FDMM ≥ L3** 且用供应商 CV 模块（勿自研）。供应商须在你*同类*视频上展示评估（`data/09#algo-cv-posture`）。

> **If below the gate / 若未达门槛**: do not pilot. Use a coach-led visual posture check (no camera, no data). Revisit CV only at L3 with a vetted vendor and legal sign-off.
> **若未达门槛**：不试点。改用教练肉眼体态检查（无摄像头无数据）。L3 + 合格供应商 + 法务签字后再考虑 CV。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **Use-case scoped** (posture demo vs rep count vs safety — pick one, see §3.1). / 用例已定界（体态/计数/安全——只选一，见 §3.1）。
- [ ] **HI-1 legal basis per market** confirmed via `tools/05` (biometric/imagery). / 各市场 HI-1 法律依据经 `tools/05` 确认（生物识别/影像）。
- [ ] **Consent flow built** (explicit, separable, withdrawable). / 同意流已建（明确、可分、可撤回）。
- [ ] **Minors excluded** by policy + system check. / 未成年按政策+系统排除。
- [ ] **No cameras in changing rooms / showers** (HI-5 absolute). / 更衣室/淋浴禁摄像头（HI-5 绝对禁区）。
- [ ] **Coach in the loop** to explain any output (HI-2/6). / 教练在回路解读输出（HI-2/6）。
- [ ] **Ground-truth plan** for accuracy validation (§3.4). / 精度验证的真值方案（§3.4）。
- [ ] **No-medical-claims script** locked (HI-6). / 非医疗宣称话术已锁定（HI-6）。

---

## ③ THE TEMPLATE / 模板

### 3.1 Use-case scoping / 用例定界 {#p1-scoping}

> Pick exactly ONE primary use case for the pilot. Mixing them muddies validation and consent.
> 试点只选**一个**主用例。混用会搅乱验证与同意。

| Use case / 用例 | In scope? / 纳入? | Risk level / 风险级 | Note / 备注 |
|---|---|---|---|
| Posture demo (observation only) / 体态演示（仅观察） | ☐ | Medium / 中 | must say "observation not diagnosis" / 须说"观察非诊断" |
| Rep counting / 动作计数 | ☐ | Medium / 中 | assist only / 仅辅助 |
| Safety monitoring (fall detect) / 安全监控（跌倒检测） | ☐ | High / 高 | needs HI-2 redundancy / 需 HI-2 冗余 |

### 3.2 HI-1 compliance gate (DO THIS BEFORE PILOT) / HI-1 合规闸门（试点前必做） {#p2-hi1-gate}

> **HI-1 hard invariant**: biometric & minors' data recommendations MUST cite the target market's legal basis. No legal basis = no pilot.
> **HI-1 硬不变量**：涉生物识别与未成年人数据的建议必须带目标市场合规依据。无依据=不开试点。

| Market / 市场 | Biometric/imagery legal basis / 生物识别影像依据 | Minors rule / 未成年规则 | Verified via tools/05? / 经tools/05核验? |
|---|---|---|---|
| CN / 中国 | PIPL art.26 public-area imaging + separate consent / PIPL第26条公共场所图像+单独同意 | exclude <18 / 排除<18 | ☐ date ___ |
| JP / 日本 | APPI — purpose + consent / APPI 目的+同意 | exclude / 排除 | ☐ date ___ |
| SG / 新加坡 | PDPA consent + proportionality / PDPA 同意+比例 | exclude / 排除 | ☐ date ___ |
| AU / 澳洲 | Privacy Act + health-privacy / 隐私法+健康隐私 | exclude / 排除 | ☐ date ___ |
| IN / 印度 | DPDP 2023 (rules pending) / DPDP 2023（细则待定） | exclude / 排除 | ☐ date ___ |
| … / 其他 | verify per market / 逐市场核验 | exclude / 排除 | ☐ |

:::dynamic-hook topic="biometric-imagery-per-market" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: biometric/imagery rules differ sharply — CN requires separate consent for public-area facial capture; JP/KR/SG/AU/IN each have distinct consent + proportionality + minors exclusions. Verify the exact article + minors clause for YOUR market via tools/05 before any camera goes live. / 截至 2026-07：生物识别/影像规则差异大——中国公共场所人脸采集需单独同意；日/韩/新/澳/印各有不同同意+比例+未成年排除。任何摄像头上线前经 tools/05 核验你市场的确切条款与未成年条款。
:::

**Consent flow requirements / 同意流要求**:
- Explicit, written, separable from membership contract (not buried). / 明确、书面、与会籍合同分离（不藏）。
- Withdrawable within 72h, stops all processing (HI-1/§11 refs/13). / 72h 内可撤回，停止全部处理。
- Minors: **excluded by default**, no parental override for biometric scoring. / 未成年：**默认排除**，生物评分不开放家长代同意。

### 3.3 Camera & zone rules / 摄像头与区域规则 {#p3-zones}

- [ ] **Changing rooms & showers: absolute no-go** (HI-5). Physically impossible to mount. / 更衣室淋浴：绝对禁区（HI-5），物理上不可装。
- [ ] Training floor only, signage posted, purpose stated. / 仅训练区，贴标识、标明用途。
- [ ] Data minimisation: store score/observation, not raw video where possible (HI-8). / 最小化：尽量存分数/观察而非原始视频（HI-8）。

### 3.4 Accuracy validation protocol / 精度验证协议 {#p4-accuracy}

> Vendor "98% accurate" lab claims drop in a real, loud, crowded gym. Validate on YOUR footage against ground truth.
> 厂商「98% 准」实验室宣称在真实吵闹拥挤场馆会掉。在你*自己的*视频上对照真值验证。

| Exercise / 动作 | Vendor claim / 厂商宣称 | Ground-truth count / 真值计数 | CV count / CV计数 | Error / 误差 | Pass? / 通过? |
|---|---|---|---|---|---|
| Squat / 深蹲 | ___% | ___ | ___ | ___% | ☐ |
| Push-up / 俯卧撑 | ___% | ___ | ___ | ___% | ☐ |
| … | | | | | |

- Ground truth = 2 human annotators agree. / 真值=2 人标注一致。
- Test across body types (bias check). / 跨体型测试（偏见检查）。
- Pilot passes only if error < agreed threshold on YOUR footage. / 仅当在你视频上误差<约定阈值才过。

### 3.5 Coach workflow integration / 教练工作流集成 {#p5-coach-workflow}

- [ ] Output shown to coach first, coach explains to member (HI-2/6). / 输出先给教练，教练向会员解读（HI-2/6）。
- [ ] Output phrased as "observation", not score/diagnosis. / 输出措辞为「观察」非分数/诊断。
- [ ] Coach can dismiss/annotate any output. / 教练可驳回/标注任何输出。

### 3.6 Member communication script / 会员沟通话术 {#p6-script}

> Use verbatim; do NOT add medical language.
> 照读；勿加医疗措辞。

```
EN: "We use a camera tool to give your coach a friendly movement observation,
like 'leans forward on squats'. It is NOT a medical diagnosis and not a
replacement for your coach. You can opt out any time."
中文："我们用摄像头工具给教练一个友好的动作观察，比如'深蹲时前倾'。
这不是医疗诊断，也不替代教练。你可随时退出。"
```

### 3.7 No-medical-claims boundary (HI-6) / 非医疗宣称边界（HI-6） {#p7-no-medical}

> **HI-6**: health/medical-grade conclusions MUST be referred to qualified professionals; the Skill never diagnoses. The pilot report = observation only.
> **HI-6**：医疗级结论必须转介专业人士；本 Skill 不做诊断。试点报告=仅观察。

- ❌ "You have scoliosis / 你有脊柱侧弯" → forbidden. / 禁。
- ❌ "Corrects your injury / 矫正你的伤" → forbidden. / 禁。
- ✅ "Observation: shoulders uneven during press / 观察：推举时双肩不平" → allowed, coach-framed. / 允许，由教练转述。

---

## ④ Common mistakes / 常见误区

- **No HI-1 legal basis** → unlawful imaging, fines, member trust loss. / 无 HI-1 依据→违法成像、罚款、失 trust。
- **Cameras in changing rooms** → HI-5 violation, immediate stop. / 更衣室装摄像头→HI-5 违规，立即停。
- **Lab-only accuracy** → fails in real gym, false confidence. / 仅实验室精度→真实场馆失效、虚假自信。
- **Medical wording** → HI-6 breach, liability. / 医疗措辞→HI-6 违规、担责。
- **Minors included** → HI-1 hard fail. / 纳入未成年→HI-1 硬失败。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `data/09-algorithm-kernel-library.md#algo-cv-posture` — method, eval, build-vs-buy, min-data. / 方法、评估、建买、最小数据。
- `references/12-biometrics-and-cctv.md` — biometric & camera compliance. / 生物识别与摄像头合规。
- `references/04-ai-application-landscape.md#ai-07-ai-body-assessment` — use-case flags. / 用例标记。
- `references/13-data-and-llm-engine.md#k-32-member-360` — sensitive-tag ban list (K3). / 敏感标签禁单。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: FDMM L3 gate + vendor-eval-on-your-footage + HI-1 legal basis per market + HI-5 zone ban + HI-8 minimisation.
- **Operator / 运营者**: scoped use case, consent flow, ground-truth validation sheet, coach-in-loop workflow, comms script — pilot run safely.
- **Member / 会员**: explicit withdrawable consent (HI-1), minors protected, no medical claims (HI-6), observation-not-diagnosis, coach explains (HI-2).
本文件覆盖架构师（FDMM L3 门槛+供应商在你视频评估+各市场 HI-1 依据+HI-5 禁区+HI-8 最小化）、运营者（定界用例、同意流、真值验证表、教练在回路工作流、沟通话术——安全跑试点）、会员（明确可撤回同意 HI-1、未成年受护、非医疗宣称 HI-6、观察非诊断、教练解读 HI-2）。
