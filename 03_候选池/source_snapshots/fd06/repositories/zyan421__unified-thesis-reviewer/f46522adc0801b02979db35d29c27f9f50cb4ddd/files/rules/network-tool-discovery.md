# 联网工具发现规则

本文件定义 `unified-thesis-reviewer` 在 §4 TR 流程中、`rules/online-verification-unified.md` 触发联网核实之前，如何**在运行时**识别当前宿主环境有哪些可用的联网工具。本 skill **不硬编码**任何具体工具名，而是靠"**工具名关键字子串匹配**"识别。

## 索引

- 识别原则：§1
- 关键字白名单（12+ 项）：§2
- 6 平台对照表：§3
- 识别失败的降级：§4
- 示例判定表：§5

---

## §1 识别原则

1. **运行时而非文档时**：不在 SKILL.md 或本文件中写死工具名。Agent 在执行到联网核实阶段时扫描当前可用工具列表，按 §2 关键字匹配
2. **子串包含**：只要工具名（不区分大小写）**包含** §2 白名单中**任一关键字子串**，即视为具备联网能力
3. **不区分联网能力的"种类"**：无论是搜索（search）、抓取（fetch）、浏览（browse）还是专用法律检索（裁判文书 / 北大法宝），都归为"具备联网能力"，由 `rules/online-verification-unified.md` 统一走四步式
4. **多个工具并存时**：优先按 Agent 判断选择最合适的工具（例如核实裁判文书优先用"裁判文书"关键字命中的工具；核实学术文献优先用 "scholar" 关键字命中的工具），但不做硬性绑定

---

## §2 关键字白名单

以下 12 项关键字任一命中即视为联网工具可用（子串匹配，不区分大小写）：

| # | 关键字 | 说明 |
|---|---|---|
| 1 | `search` | 通用搜索（web_search、remote_web_search、brave_search、google_search 等） |
| 2 | `web` | 通用 web 访问（web_fetch、web_browse、web_lookup 等） |
| 3 | `browse` | 浏览器自动化（oc_browse、browser_use、browser_automation 等） |
| 4 | `fetch` | HTTP 抓取（web_fetch、fetch_url、http_fetch 等） |
| 5 | `google` | Google 搜索专用连接器 |
| 6 | `bing` | Bing 搜索专用连接器 |
| 7 | `baidu` | 百度搜索专用连接器 |
| 8 | `scholar` | 学术检索（Google Scholar、Semantic Scholar、Scholar API） |
| 9 | `裁判文书` | 中国裁判文书网连接器 |
| 10 | `北大法宝` | 北大法宝法律数据库连接器 |
| 11 | `威科先行` | 威科先行法律信息库连接器 |
| 12 | `法律检索` | 通用法律检索插件 / 法律数据库连接器 |

扩展规则：若未来出现明显属于"联网"语义但不在白名单的工具名（如 `crawl`、`scrape`、`lookup`、`api_call`、`query_web`），Agent 可在具体任务中临时判定为联网工具可用，但不要把它写入本文件以免白名单泛滥。白名单的稳定性 > 覆盖率。

---

## §3 6 平台对照表

下表列出各主要平台的典型联网工具名，说明如何命中 §2 的关键字。**具体工具名未来可能变化**——本表只作示例，不作硬编码依据。

| 平台 | 典型工具名 | 命中的关键字 | 备注 |
|---|---|---|---|
| **Claude Code** | `web_search`、`web_fetch` | web / search / fetch | 原生内置，联网能力最稳定 |
| **Kiro** | `remote_web_search`、`web_fetch`、`grep_search`（本地）| web / search / fetch | 注意：`grep_search` 是本地代码检索，**不**算联网工具 |
| **Hermes** | 平台注入的浏览器工具 / `hermes_web_search` 等 | 按平台实际工具名判断 | 由宿主配置决定，Agent 在运行时扫描 |
| **OpenClaw** | MCP 注入的 `search_*` / `fetch_*` | search / fetch | OpenClaw 的插件生态较丰富，常同时有搜索与抓取工具 |
| **Coze** | 插件市场的搜索 / 浏览插件（名字通常含 `search_engine` / `browser` / `web`） | search / web / browse | Coze 插件的命名通常含语义词根 |
| **MCP 标准** | `brave_search` / `google_search` / `scholar_search` / `裁判文书查询` 等 | search / google / scholar / 裁判文书 等 | MCP 服务器的工具名多样，多关键字命中的情况常见 |

注：**IMA** 等纯对话平台目前不自带联网工具；若宿主环境确实没有任何命中 §2 的工具，按 §4 降级。

---

## §4 识别失败的降级

扫描完当前可用工具列表后，若 **没有任何工具名**命中 §2 白名单：

- 判定当前宿主环境**不具备联网能力**
- 在 Unified_Report 的联网核实章节显著标注：

  > ⚠️ 当前环境不具备联网能力，以下条目仅作标记，需用户自行核实

- 按 `rules/online-verification-unified.md` 的"无联网降级"分支处理：对每个待核实条目仅完成四步式的**前两步**（定位 + 原文复述），后两步留空并注明"待核实"
- 建议用户在具备联网工具的环境中重新运行本 skill，或向导师/评阅人提供该清单

不要臆测真实情况，不要编造"核实结果"。

---

## §5 示例判定表

以下是若干工具名的判定样例，展示匹配规则的一致性：

| 工具名 | 命中的关键字 | 判定 |
|---|---|---|
| `web_search` | web、search | 联网 |
| `Web_Fetch` | web、fetch | 联网（不区分大小写） |
| `remote_web_search` | web、search | 联网 |
| `brave_search` | search | 联网 |
| `google_scholar` | google、scholar | 联网 |
| `裁判文书查询` | 裁判文书 | 联网 |
| `北大法宝_case_search` | 北大法宝、search | 联网 |
| `威科先行_law_lookup` | 威科先行 | 联网 |
| `oc_browse_page` | browse | 联网 |
| `coze_search_engine` | search | 联网 |
| `grep_search` | search | 本地代码检索，**不**算联网——但按本规则仍被判联网，需 Agent 在实际调用前二次判断"这个工具能否访问外网"；若不能，从候选列表剔除 |
| `read_file` | — | 非联网 |
| `execute_bash` | — | 非联网（除非其本身去 curl 访问外网，但此时应优先使用专门的 fetch 工具） |
| `list_directory` | — | 非联网 |
| `fs_write` | — | 非联网 |

关于 `grep_search` 的特殊说明：少数平台会把它命名为可联网的"代码仓库搜索"，此时按关键字 search 命中；但多数平台它只是本地 ripgrep 封装，不联网。Agent 在调用前可尝试用一次核实查询确认"能否访问外网"，失败则从候选列表剔除。这种情况不破坏"关键字匹配"的总原则——只是在运行时做一次二次确认。

---

## §6 与 `rules/online-verification-unified.md` 的关系

- 本文件只回答"**有没有**联网工具"
- "**如何使用**联网工具"由 `rules/online-verification-unified.md` 的四步式规范
- "**使用失败怎么办**"由 `rules/online-verification-unified.md` 的单条失败分支规范
- 本文件的识别结果作为布尔信号传入联网核实流程：`has_network_tool() → True / False`
