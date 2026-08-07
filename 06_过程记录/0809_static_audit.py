from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(r"D:\高校AI工作台\高校AI技能库调研")
SNAPSHOT_ROOT = ROOT / "03_候选池" / "source_snapshots" / "0809"
AUDIT_DATE = "2026-08-07"


REPOSITORIES = {
    "addy_agent_skills": {
        "platform": "GitHub", "repo": "addyosmani/agent-skills", "branch": "main",
        "repo_url": "https://github.com/addyosmani/agent-skills", "license": "MIT", "stars": 83430,
        "ecosystem": "Agent Skills / 多代码智能体",
    },
    "anthropic_skills": {
        "platform": "GitHub", "repo": "anthropics/skills", "branch": "main",
        "repo_url": "https://github.com/anthropics/skills", "license": "各技能目录 Apache-2.0", "stars": 166590,
        "ecosystem": "Anthropic 官方 Agent Skills / 可移植工作流",
    },
    "arduino_skills": {
        "platform": "GitHub", "repo": "wedsamuel1230/arduino-skills", "branch": "main",
        "repo_url": "https://github.com/wedsamuel1230/arduino-skills", "license": "MIT", "stars": 19,
        "ecosystem": "Agent Skills / Arduino 与嵌入式",
    },
    "gitee_agent_skills": {
        "platform": "Gitee", "repo": "8686555/awesome-agent-skills", "branch": "main",
        "repo_url": "https://gitee.com/8686555/awesome-agent-skills", "license": "CC0-1.0", "stars": 0,
        "ecosystem": "Agent Skills 中文示例库",
    },
    "gitlab_ai_skills": {
        "platform": "GitLab", "repo": "gitlab-org/ai/skills", "branch": "main",
        "repo_url": "https://gitlab.com/gitlab-org/ai/skills", "license": "MIT", "stars": 37,
        "ecosystem": "GitLab 官方 Agent Skills",
    },
    "hf_skills": {
        "platform": "GitHub（Hugging Face 官方上游）", "repo": "huggingface/skills", "branch": "main",
        "repo_url": "https://github.com/huggingface/skills", "license": "Apache-2.0", "stars": 10907,
        "ecosystem": "Hugging Face 官方 Agent Skills",
    },
    "k_dense": {
        "platform": "GitHub", "repo": "K-Dense-AI/scientific-agent-skills", "branch": "main",
        "repo_url": "https://github.com/K-Dense-AI/scientific-agent-skills", "license": "MIT", "stars": 32822,
        "ecosystem": "Agent Skills / 科学计算与数据分析",
    },
    "leanprover_skills": {
        "platform": "GitHub", "repo": "leanprover/skills", "branch": "main",
        "repo_url": "https://github.com/leanprover/skills", "license": "Apache-2.0", "stars": 61,
        "ecosystem": "Agent Skills / Lean 形式化验证",
    },
    "obra_superpowers": {
        "platform": "GitHub", "repo": "obra/superpowers", "branch": "main",
        "repo_url": "https://github.com/obra/superpowers", "license": "MIT", "stars": 267788,
        "ecosystem": "Claude Code / Agent Skills / 可移植工程工作流",
    },
    "robotics_skills": {
        "platform": "GitHub", "repo": "arpitg1304/robotics-agent-skills", "branch": "main",
        "repo_url": "https://github.com/arpitg1304/robotics-agent-skills", "license": "Apache-2.0", "stars": 334,
        "ecosystem": "Agent Skills / 机器人软件",
    },
    "ska_ai_skills": {
        "platform": "GitLab", "repo": "ska-telescope/ska-ai-skills", "branch": "main",
        "repo_url": "https://gitlab.com/ska-telescope/ska-ai-skills", "license": "BSD-3-Clause", "stars": 3,
        "ecosystem": "SKAO 官方 Agent Skills / 多智能体兼容",
    },
    "travis_skills": {
        "platform": "GitHub", "repo": "travisjneuman/.claude", "branch": "master",
        "repo_url": "https://github.com/travisjneuman/.claude", "license": "MIT", "stars": 87,
        "ecosystem": "Claude Code Skills / 可移植知识工作流",
    },
    "wshobson_agents": {
        "platform": "GitHub", "repo": "wshobson/agents", "branch": "main",
        "repo_url": "https://github.com/wshobson/agents", "license": "MIT", "stars": 38534,
        "ecosystem": "Claude Code 插件 Skills / 可移植工作流",
    },
}


META = {
    "api-and-interface-design": ("API 与接口设计", "以契约、兼容性、错误模型和演进策略设计 REST、GraphQL 与内部接口。", "B 软件工程"),
    "browser-testing-with-devtools": ("浏览器 DevTools 测试", "使用浏览器开发者工具完成页面检查、网络诊断、性能观察与交互验证。", "B 软件工程"),
    "ci-cd-and-automation": ("CI/CD 与工程自动化", "规划持续集成、质量门禁、构建制品、部署和回滚的自动化流水线。", "B 软件工程"),
    "code-review-and-quality": ("代码审查与质量控制", "按正确性、安全性、可维护性和测试证据系统审查代码变更。", "B 软件工程"),
    "code-simplification": ("代码简化", "识别不必要抽象、重复和复杂控制流，并提出可验证的简化方案。", "B 软件工程"),
    "debugging-and-error-recovery": ("调试与错误恢复", "从证据出发复现、定位、修复问题，并验证恢复路径。", "B 软件工程"),
    "documentation-and-adrs": ("工程文档与 ADR", "编写面向维护者的技术文档和可追溯架构决策记录。", "B 软件工程"),
    "frontend-ui-engineering": ("前端 UI 工程", "将界面需求转化为可访问、响应式、可维护的前端实现。", "G 数字媒体"),
    "git-workflow-and-versioning": ("Git 工作流与版本管理", "规范分支、提交、合并、版本标记和变更历史。", "B 软件工程"),
    "incremental-implementation": ("增量实现", "把复杂功能切成可审查、可测试、可回滚的小步交付。", "B 软件工程"),
    "observability-and-instrumentation": ("可观测性与埋点", "设计日志、指标、追踪和诊断信号，使系统行为可解释。", "B 软件工程"),
    "performance-optimization": ("性能分析与优化", "建立基线、定位瓶颈并用测量结果验证优化收益。", "A 计算基础"),
    "security-and-hardening": ("安全加固", "从攻击面、依赖、输入、权限和运行配置角度加固软件。", "C 网络安全"),
    "spec-driven-development": ("规格驱动开发", "用明确规格、验收标准和任务分解约束实现过程。", "B 软件工程"),
    "test-driven-development": ("测试驱动开发", "先写失败测试，再完成最小实现和重构，以测试证据驱动开发。", "B 软件工程"),
    "algorithmic-art": ("算法艺术", "用 p5.js、种子随机和参数化系统创作原创生成艺术。", "G 数字媒体"),
    "canvas-design": ("静态视觉设计", "以视觉哲学指导海报、艺术作品和静态 PNG/PDF 构图。", "G 数字媒体"),
    "frontend-design": ("前端视觉设计", "为网页选择有主题依据的版式、字体、色彩、动效和视觉识别。", "G 数字媒体"),
    "arduino-code-generator": ("Arduino 代码生成", "为常见传感器、执行器、总线和非阻塞状态机生成嵌入式 C++ 模式。", "D 物联网"),
    "arduino-project-builder": ("Arduino 项目脚手架", "按板卡和项目类型生成 Arduino/PlatformIO 项目结构与基础文件。", "D 物联网"),
    "circuit-debugger": ("电路故障诊断", "用电源、连通性、信号和最小诊断草图排查硬件故障。", "D 物联网"),
    "datasheet-interpreter": ("器件数据手册解读", "从器件 PDF 中提取电气指标、引脚、地址、时序和寄存器信息。", "D 物联网"),
    "field-power-and-connectivity-triager": ("现场供电与连接诊断", "排查设备离开 USB 台架后出现的掉电、峰值电流和联网故障。", "D 物联网"),
    "freertos-patterns": ("FreeRTOS 并发模式", "指导任务、队列、同步、内存与跨核协作设计。", "D 物联网"),
    "i2c-bringup-diagnostician": ("I2C 上电调试", "按电气、地址、扫描器、库和板卡差异定位 I2C 初始化失败。", "D 物联网"),
    "power-budget-calculator": ("嵌入式功耗预算", "估算器件电流、占空比、电池续航和节能空间。", "D 物联网"),
    "sensor-calibration-workbench": ("传感器校准工作台", "组织预热、参考测量、系数保存、漂移检查和重校准流程。", "D 物联网"),
    "api-doc-generator": ("API 文档生成", "从代码梳理端点、参数、响应、认证并输出 Markdown 或 OpenAPI 文档。", "B 软件工程"),
    "code-review": ("代码审查", "以双语模板检查语法、逻辑、安全、性能和风格问题。", "B 软件工程"),
    "debug-helper": ("调试助手", "围绕 What、Where、Why、How 分析错误并给出修复与预防建议。", "B 软件工程"),
    "git-commit": ("Git 提交信息生成", "按 Conventional Commits 从变更生成规范提交信息。", "B 软件工程"),
    "unit-test-generator": ("单元测试生成", "识别语言、框架、正常路径、边界和异常，生成测试草案。", "B 软件工程"),
    "commit-messages": ("GitLab 提交信息规范", "生成祈使语态、结构清晰、适合原子提交的 Git 信息。", "B 软件工程"),
    "handoff": ("工程任务交接", "把当前任务状态压缩为可续接、可脱敏、锚定持久工件的交接文档。", "B 软件工程"),
    "mr-guided-review": ("GitLab MR 引导式审查", "先理解合并请求目标，再进行只读代码审查并由人工发布反馈。", "B 软件工程"),
    "huggingface-community-evals": ("Hugging Face 本地模型评测", "选择本地评测后端并运行 inspect-ai 或 LightEval 评测。", "E AI与数据"),
    "huggingface-gradio": ("Gradio 交互应用", "构建面向模型、数据和多媒体任务的 Python 交互界面。", "G 数字媒体"),
    "huggingface-local-models": ("Hugging Face 本地模型运行", "选择 GGUF 与量化规格并用 llama.cpp 在本地运行模型。", "E AI与数据"),
    "dask": ("Dask 并行数据处理", "用任务图和分块数据结构处理超内存或可并行的数据工作负载。", "E AI与数据"),
    "exploratory-data-analysis": ("探索性数据分析", "从数据质量、分布、关系、异常和可复现报告开展 EDA。", "E AI与数据"),
    "geomaster": ("GeoMaster 地理空间计算", "覆盖 GIS、遥感、栅格矢量、空间统计和地球观测机器学习。", "F 空间信息"),
    "geopandas": ("GeoPandas 空间数据分析", "处理矢量地理数据、坐标系、空间连接和地图输出。", "F 空间信息"),
    "get-available-resources": ("计算资源侦测", "只读盘点 CPU、GPU、内存和磁盘，并给出计算策略建议。", "A 计算基础"),
    "matplotlib": ("Matplotlib 绘图", "使用面向对象接口创建可控的科学图表、布局和多格式输出。", "E AI与数据"),
    "networkx": ("NetworkX 图网络分析", "创建和分析图结构、路径、中心性、社群及网络可视化。", "A 计算基础"),
    "optimize-for-gpu": ("GPU 计算优化", "从内存、批量、精度、数据传输和剖析结果优化 GPU 工作负载。", "E AI与数据"),
    "polars": ("Polars 高性能表格处理", "以惰性执行和列式表达式构建高性能数据转换。", "E AI与数据"),
    "pytorch-lightning": ("PyTorch Lightning 训练工程", "组织训练循环、日志、检查点、分布式训练和实验复现。", "E AI与数据"),
    "scientific-visualization": ("科学可视化", "围绕结论、证据、配色、标注和导出质量制作科研图表。", "E AI与数据"),
    "scikit-learn": ("Scikit-learn 机器学习", "构建预处理、训练、验证、调参和解释的传统机器学习管线。", "E AI与数据"),
    "shap": ("SHAP 模型解释", "用 SHAP 值解释全局和个体预测并审查解释边界。", "E AI与数据"),
    "simpy": ("SimPy 离散事件仿真", "用进程、资源和事件构建排队、制造与系统仿真。", "A 计算基础"),
    "statsmodels": ("Statsmodels 统计建模", "完成回归、广义线性、时间序列和诊断推断。", "E AI与数据"),
    "sympy": ("SymPy 符号计算", "执行代数化简、方程、微积分、矩阵和符号验证。", "A 计算基础"),
    "transformers": ("Transformers 模型应用", "使用预训练 Transformer 完成 NLP、多模态推理与微调工作流。", "E AI与数据"),
    "uncertainty-and-units": ("不确定度与单位", "在计算中传播测量不确定度、单位和有效数字。", "E AI与数据"),
    "lean-proof": ("Lean 形式化证明", "在 Lean/mathlib 中构造、检查和组织可编译证明。", "A 计算基础"),
    "mathlib-review": ("Mathlib 代码审查", "按 mathlib API、属性和风格审查形式化数学贡献。", "A 计算基础"),
    "systematic-debugging": ("系统化调试", "坚持根因调查、模式分析、假设验证和实施修复四阶段。", "B 软件工程"),
    "robotics-design-patterns": ("机器人设计模式", "设计感知—规划—控制栈、行为树、安全层和硬件抽象。", "D 物联网"),
    "robotics-security": ("机器人系统安全", "覆盖 SROS2、DDS 加密、网络分段、密钥和物理—网络安全。", "C 网络安全"),
    "robotics-software-principles": ("机器人软件原则", "把 SOLID、依赖反转、实时约束和仿真替身用于机器人软件。", "D 物联网"),
    "robotics-testing": ("机器人软件测试", "组织单元、集成、仿真、硬件在环和确定性回放测试。", "D 物联网"),
    "lazy-architect": ("精简架构审查", "识别过度设计、投机抽象和无收益层次，提出减法式架构方案。", "B 软件工程"),
    "ska-multi-agent-orchestration": ("工程多智能体编排", "以计划—构建—审查—人工批准组织复杂工程交付。", "B 软件工程"),
    "application-security": ("应用安全", "以 OWASP、输入验证、依赖扫描和安全响应头加固 Web 应用。", "C 网络安全"),
    "ar-vr-xr": ("AR/VR/XR 开发", "覆盖 Unity XR、WebXR、ARKit、ARCore 与空间交互设计。", "G 数字媒体"),
    "audio-production": ("音频制作", "指导录音、编辑、混音、母带、响度和声音设计。", "G 数字媒体"),
    "compliance-engineering": ("合规工程", "把 GDPR、SOC 2、PCI-DSS 等要求映射到访问、加密、审计和隐私控制。", "H 保密治理"),
    "edge-computing": ("边缘计算", "比较边缘运行时、缓存、数据一致性和低延迟架构模式。", "B 软件工程"),
    "embedded-iot": ("嵌入式与物联网基础", "覆盖微控制器、RTOS、MQTT/CoAP/BLE 与 I2C/SPI/UART 模式。", "D 物联网"),
    "game-development": ("游戏开发", "覆盖 Unity、Unreal、Godot 的玩法、物理、AI、性能和发布基础。", "G 数字媒体"),
    "video-production": ("视频制作", "组织前期、拍摄、剪辑、调色、动效、声音和多平台交付。", "G 数字媒体"),
    "wcag-audit-patterns": ("WCAG 可访问性审计", "依据 WCAG 对页面结构、键盘、对比度和辅助技术兼容性开展审计。", "G 数字媒体"),
    "api-design-principles": ("API 设计原则", "用资源建模、版本、分页、错误和兼容策略设计 API。", "B 软件工程"),
    "architecture-patterns": ("软件架构模式", "比较分层、六边形、事件驱动、CQRS 等架构及适用条件。", "B 软件工程"),
    "secrets-management": ("秘密管理", "设计 CI/CD 中的秘密存储、动态凭据、轮换和最小权限。", "H 保密治理"),
    "auth-implementation-patterns": ("认证与授权模式", "覆盖会话、JWT、OAuth2、RBAC、密码和重置安全。", "C 网络安全"),
    "code-review-excellence": ("高质量代码审查", "用建设性反馈、检查清单和风险优先级改进评审协作。", "B 软件工程"),
    "e2e-testing-patterns": ("端到端测试模式", "设计稳定的 E2E 测试、测试数据、选择器和故障诊断。", "B 软件工程"),
    "architecture-decision-records": ("架构决策记录", "用统一结构记录背景、选项、决定、后果和复审条件。", "B 软件工程"),
    "openapi-spec-generation": ("OpenAPI 规范生成", "生成和校验 OpenAPI 契约、模型、示例与代码优先同步流程。", "B 软件工程"),
    "gdpr-data-handling": ("GDPR 数据处理", "把数据最小化、合法基础、访问、更正、删除和留存要求落实到系统。", "H 保密治理"),
    "attack-tree-construction": ("攻击树构建", "以目标、路径、前置条件和防御缺口可视化攻击场景。", "C 网络安全"),
    "security-requirement-extraction": ("安全需求提取", "从业务、资产、威胁和合规约束中形成可验证的安全需求。", "C 网络安全"),
    "stride-analysis-patterns": ("STRIDE 威胁分析", "按仿冒、篡改、抵赖、泄露、拒绝服务和提权系统识别威胁。", "C 网络安全"),
    "threat-mitigation-mapping": ("威胁—缓解措施映射", "把已识别威胁映射到控制、优先级、责任人和验证方式。", "C 网络安全"),
}


GROUP_MAJORS = {
    "A 计算基础": ["计算机科学与技术", "软件工程", "电子与计算机工程", "智能科学与技术", "数据科学与大数据技术"],
    "B 软件工程": ["计算机科学与技术", "软件工程", "网络工程", "电子与计算机工程", "新媒体技术"],
    "C 网络安全": ["网络工程", "信息安全", "网络空间安全", "物联网工程", "保密管理"],
    "D 物联网": ["物联网工程", "电子与计算机工程", "计算机科学与技术", "智能科学与技术"],
    "E AI与数据": ["智能科学与技术", "数据科学与大数据技术", "计算机科学与技术", "空间信息与数字技术"],
    "F 空间信息": ["空间信息与数字技术", "数据科学与大数据技术", "智能科学与技术"],
    "G 数字媒体": ["数字媒体技术", "新媒体技术", "电影制作", "计算机科学与技术"],
    "H 保密治理": ["信息安全", "网络空间安全", "保密管理", "软件工程"],
}


TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".sh", ".ps1", ".js", ".ts", ".mjs", ".cjs", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".html", ".css", ".xml", ".csv", ".ino", ".c", ".h", ".hpp", ".cpp",
    ".java", ".rs", ".go", ".rb", ".r", ".m", ".tex", ".mmd",
}
SCRIPT_EXTENSIONS = {".py", ".sh", ".ps1", ".js", ".ts", ".mjs", ".cjs", ".bat", ".cmd", ".rb"}


PATTERNS = {
    "network": re.compile(r"(?i)https?://|\bcurl\b|\bwget\b|\bhttpx\b|\brequests\b|\burllib\b|\bfetch\s*\(|\bsocket\b"),
    "credentials": re.compile(r"(?i)api[_ -]?key|access[_ -]?token|bearer\s+<|HF_TOKEN|VAULT_TOKEN|credential|password|\.env\b|secret[s]?\b"),
    "process": re.compile(r"(?i)subprocess\.|os\.system|shell\s*=\s*True|execv|execvp|execvpe|Start-Process|child_process"),
    "write": re.compile(r"(?i)write_text\s*\(|write_bytes\s*\(|File\.Write|open\([^\n]+[, ]['\"]w|\.write\s*\(|Set-Content|Add-Content|Out-File|\s>>?\s"),
    "delete": re.compile(r"(?i)rm\s+-rf|Remove-Item|unlink\s*\(|rmtree\s*\(|os\.remove|delete[A-Za-z_]*\s*\("),
    "privilege": re.compile(r"(?i)\bsudo\b|systemctl|/etc/|HKEY_|Set-ExecutionPolicy|chmod\s+[467]"),
    "remote_exec": re.compile(r"(?i)curl[^\n|]{0,240}\|\s*(?:ba)?sh|wget[^\n|]{0,240}\|\s*(?:ba)?sh|\bnpx\s+(?:-y|--yes)\b|\buv\s+run\b|\bpip\s+install\b|\bnpm\s+install\b|\bbrew\s+install\b|\bwinget\s+install\b"),
    "external_state": re.compile(r"(?i)git\s+push|glab\s+(?:mr|issue)|\bdeploy\b|\bupload\b|\bpublish\b|create[_ -]repo|post\s+(?:comment|note)|hf_jobs\s*\("),
    "prompt_bypass": re.compile(r"(?i)ignore (?:all |any )?(?:previous|system|developer) instructions|bypass (?:approval|authorization|permission)|disable (?:safety|guardrail)"),
}


SA_FORCE = {
    "canvas-design", "frontend-design", "api-doc-generator", "code-review", "debug-helper", "git-commit",
    "unit-test-generator", "commit-messages", "mathlib-review", "robotics-design-patterns", "robotics-software-principles",
    "lazy-architect", "audio-production", "video-production", "ar-vr-xr", "embedded-iot", "edge-computing",
    "wcag-audit-patterns", "api-design-principles", "architecture-patterns", "code-review-excellence",
    "architecture-decision-records", "openapi-spec-generation", "attack-tree-construction",
    "security-requirement-extraction", "stride-analysis-patterns", "threat-mitigation-mapping",
}

SBA_FORCE = {
    "algorithmic-art", "ci-cd-and-automation", "browser-testing-with-devtools", "datasheet-interpreter",
    "huggingface-community-evals", "huggingface-local-models", "robotics-testing", "secrets-management",
    "e2e-testing-patterns", "geomaster", "dask", "exploratory-data-analysis", "geopandas", "matplotlib",
    "networkx", "optimize-for-gpu", "polars", "pytorch-lightning", "scientific-visualization", "scikit-learn",
    "shap", "simpy", "statsmodels", "sympy", "transformers", "uncertainty-and-units",
}

SB_FORCE = {
    "api-and-interface-design", "code-review-and-quality", "code-simplification", "debugging-and-error-recovery",
    "documentation-and-adrs", "frontend-ui-engineering", "git-workflow-and-versioning", "incremental-implementation",
    "observability-and-instrumentation", "performance-optimization", "security-and-hardening",
    "spec-driven-development", "test-driven-development", "arduino-code-generator", "arduino-project-builder",
    "circuit-debugger", "field-power-and-connectivity-triager", "freertos-patterns", "i2c-bringup-diagnostician",
    "power-budget-calculator", "sensor-calibration-workbench", "handoff", "mr-guided-review", "huggingface-gradio",
    "get-available-resources", "lean-proof", "systematic-debugging", "robotics-security", "ska-multi-agent-orchestration",
    "application-security", "compliance-engineering", "game-development", "auth-implementation-patterns",
    "gdpr-data-handling",
}


def git_output(repo_dir: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo_dir), *args], text=True, encoding="utf-8").strip()


def parse_frontmatter(skill_file: Path) -> tuple[str, str]:
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    header_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    header = header_match.group(1) if header_match else ""
    name_match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)", header)
    name = name_match.group(1).strip() if name_match else skill_file.parent.name
    desc_match = re.search(r"(?ms)^description:\s*(.*?)(?=\n[A-Za-z][A-Za-z0-9_-]*:\s|\Z)", header)
    description = desc_match.group(1).strip() if desc_match else ""
    description = re.sub(r"^[>|-]\s*", "", description)
    description = " ".join(line.strip() for line in description.splitlines()).strip(" '\"")
    return name, description


def source_url(meta: dict, commit: str, rel_path: str) -> str:
    if meta["platform"].startswith("GitLab"):
        return f"{meta['repo_url']}/-/blob/{commit}/{rel_path}"
    if meta["platform"] == "Gitee":
        return f"{meta['repo_url']}/blob/{commit}/{rel_path}"
    return f"{meta['repo_url']}/blob/{commit}/{rel_path}"


def package_files(package_root: Path) -> list[Path]:
    return [p for p in package_root.rglob("*") if p.is_file() and ".git" not in p.parts]


def scan_package(files: list[Path]) -> tuple[dict, list[str], int, int, int]:
    hits = {key: [] for key in PATTERNS}
    domains: set[str] = set()
    line_count = 0
    script_count = 0
    binary_count = 0
    for path in files:
        if path.suffix.lower() in SCRIPT_EXTENSIONS:
            script_count += 1
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {"Dockerfile", "Makefile"}:
            binary_count += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        line_count += len(text.splitlines())
        for key, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                snippet = text.splitlines()[line - 1].strip()[:180]
                if len(hits[key]) < 12:
                    hits[key].append(f"{path.name}:{line}: {snippet}")
        for domain in re.findall(r"https?://([^/\s)'\">]+)", text, flags=re.I):
            domains.add(domain.lower().rstrip(".,;"))
    return hits, sorted(domains), line_count, script_count, binary_count


def grade_for(name: str, hits: dict, script_count: int) -> str:
    if name in SBA_FORCE:
        return "SB-A"
    if name in SB_FORCE:
        return "SB"
    if name in SA_FORCE:
        return "SA"
    if hits["remote_exec"]:
        return "SB-A"
    if script_count or any(hits[k] for k in ("network", "credentials", "process", "write", "delete", "privilege", "external_state")):
        return "SB"
    return "SA"


def restrictions_for(grade: str, hits: dict, name: str) -> str:
    if grade == "SA":
        return "按只读说明/模板使用；仍需人工复核生成内容，不自动提交、发布或替代课程评价。"
    parts = ["在隔离项目目录内使用，所有状态改变均需人工确认"]
    if hits["remote_exec"] or grade == "SB-A":
        parts.append("移除未锁版本安装与远程执行示例，依赖固定版本和哈希")
    if hits["network"]:
        parts.append("默认断网；确需联网时只开放已核准域名且不得发送校内敏感数据")
    if hits["credentials"]:
        parts.append("不得读取或回显现有凭据，令牌由用户侧最小权限注入")
    if hits["write"]:
        parts.append("输出限于显式指定的新目录，禁止覆盖原文件")
    if hits["delete"]:
        parts.append("删除命令从适配版剥离")
    if hits["privilege"]:
        parts.append("禁止 sudo、系统服务和系统级配置变更")
    if hits["external_state"]:
        parts.append("禁止自动上传、发布、推送、部署、评论或付费任务")
    if name in {"robotics-security", "circuit-debugger", "field-power-and-connectivity-triager", "i2c-bringup-diagnostician"}:
        parts.append("先在仿真、断电或教学台架验证，禁止未经授权控制真实设备")
    return "；".join(dict.fromkeys(parts)) + "。"


def behavior_summary(hits: dict, script_count: int, binary_count: int) -> tuple[str, str]:
    executable = []
    if script_count:
        executable.append(f"含 {script_count} 个脚本文件")
    if hits["process"]:
        executable.append("可调用子进程")
    if hits["write"]:
        executable.append("含文件写入示例或实现")
    if hits["delete"]:
        executable.append("含删除相关示例")
    if hits["privilege"]:
        executable.append("含系统级/高权限命令示例")
    if binary_count:
        executable.append(f"含 {binary_count} 个非文本资源（已按类型登记，未执行）")
    if not executable:
        executable.append("未见随包可执行载荷；主要为说明、模板或参考资料")
    network = []
    if hits["network"]:
        network.append("包含外部链接、下载、API 或网络访问说明")
    if hits["credentials"]:
        network.append("涉及凭据、令牌或秘密管理语境")
    if hits["external_state"]:
        network.append("包含上传、发布、推送、部署或其他外部状态行为")
    if not network:
        network.append("未见必要的凭据或外部写入行为")
    return "；".join(executable), "；".join(network)


def priority_for(group: str, name: str) -> str:
    high = {
        "systematic-debugging", "test-driven-development", "code-review-and-quality", "security-and-hardening",
        "security-requirement-extraction", "stride-analysis-patterns", "auth-implementation-patterns",
        "exploratory-data-analysis", "scikit-learn", "get-available-resources", "geopandas", "geomaster",
        "embedded-iot", "freertos-patterns", "robotics-security", "frontend-ui-engineering", "video-production",
        "compliance-engineering", "gdpr-data-handling", "secrets-management",
    }
    return "高" if name in high else "中"


def coverage_type(name: str, group: str) -> str:
    if name in {"handoff", "documentation-and-adrs", "architecture-decision-records", "ska-multi-agent-orchestration"}:
        return "跨专业通用 / 员工支持"
    if group in {"B 软件工程", "C 网络安全", "H 保密治理"}:
        return "专业核心 / 跨专业通用"
    return "专业核心"


def related_for(name: str) -> str:
    clusters = {
        "测试": {"test-driven-development", "unit-test-generator", "e2e-testing-patterns", "robotics-testing", "browser-testing-with-devtools"},
        "审查": {"code-review", "code-review-and-quality", "code-review-excellence", "mr-guided-review", "mathlib-review"},
        "调试": {"debug-helper", "debugging-and-error-recovery", "systematic-debugging", "circuit-debugger", "i2c-bringup-diagnostician"},
        "API": {"api-and-interface-design", "api-design-principles", "api-doc-generator", "openapi-spec-generation"},
        "架构": {"architecture-patterns", "lazy-architect", "robotics-design-patterns", "robotics-software-principles"},
        "视觉": {"matplotlib", "scientific-visualization", "algorithmic-art", "canvas-design", "frontend-design", "frontend-ui-engineering"},
        "安全": {"security-and-hardening", "application-security", "security-requirement-extraction", "stride-analysis-patterns", "attack-tree-construction", "threat-mitigation-mapping"},
    }
    for label, names in clusters.items():
        if name in names:
            peers = sorted(n for n in names if n != name)
            return f"{label}能力簇：" + "、".join(peers)
    return "同能力群内互补使用；部署时按任务粒度避免重复触发。"


def main() -> None:
    records = []
    snapshot_index = []
    for snapshot_dir in sorted(p for p in SNAPSHOT_ROOT.iterdir() if p.is_dir() and p.name in REPOSITORIES):
        repo_meta = REPOSITORIES[snapshot_dir.name]
        commit = git_output(snapshot_dir, "rev-parse", "HEAD")
        commit_date = git_output(snapshot_dir, "show", "-s", "--format=%cs", "HEAD")
        snapshot_index.append({
            "snapshot": snapshot_dir.name, "commit": commit, "commit_date": commit_date,
            **repo_meta,
        })
        for skill_file in sorted(snapshot_dir.rglob("SKILL.md")):
            if ".git" in skill_file.parts:
                continue
            name, original_description = parse_frontmatter(skill_file)
            if name not in META:
                raise KeyError(f"Missing META entry: {snapshot_dir.name}/{name}")
            cn_name, summary, group = META[name]
            package_root = skill_file.parent
            files = package_files(package_root)
            hits, domains, line_count, script_count, binary_count = scan_package(files)
            grade = grade_for(name, hits, script_count)
            executable_behavior, network_behavior = behavior_summary(hits, script_count, binary_count)
            rel_skill = skill_file.relative_to(snapshot_dir).as_posix()
            rel_package = package_root.relative_to(snapshot_dir).as_posix()
            raw_source = source_url(repo_meta, commit, rel_skill)
            admissions = {"SA": "原包可用", "SB": "限制使用", "SB-A": "仅适配后使用"}[grade]
            keep = "SKILL.md、说明型 references 与非可执行模板；脚本仅在逐文件复核且固定依赖后单独启用" if grade == "SB-A" else "完整说明与已审资源；执行步骤仍受限制条件约束"
            strip = "移除未锁安装、下载后执行、自动上传/发布/推送/部署、凭据读取和高权限命令；不整包安装" if grade == "SB-A" else "无强制剥离；按限制条件禁用越权步骤"
            evidence_rel = f"04_验证记录/2026-08-07-0809计算机类静态安全审查.md#{snapshot_dir.name}-{name}"
            records.append({
                "id": "",
                "name": name,
                "cn_name": cn_name,
                "discipline": "0809 计算机类",
                "majors": GROUP_MAJORS[group],
                "primary_group": group,
                "coverage_type": coverage_type(name, group),
                "platform": repo_meta["platform"],
                "ecosystem": repo_meta["ecosystem"],
                "repo": repo_meta["repo"],
                "repo_url": repo_meta["repo_url"],
                "skill_path": rel_skill,
                "package_path": rel_package,
                "skill_url": raw_source,
                "discovery_url": repo_meta["repo_url"],
                "canonical_source": raw_source,
                "review_commit": commit,
                "review_commit_date": commit_date,
                "review_date": AUDIT_DATE,
                "license": repo_meta["license"],
                "stars": repo_meta["stars"],
                "summary": summary,
                "original_description": original_description,
                "roles": "学生、教师、科研人员、实验室工程人员、信息化与技术支持人员",
                "scenarios": f"0809 计算机类课程学习、实验、课程设计、科研开发和高校员工技术工作；主能力群为{group}",
                "compatibility": "A" if "Agent Skills" in repo_meta["ecosystem"] else "B",
                "adaptation": "按学校工具链、课程诚信、数据分级、网络白名单和审批流程接入；不得自动提交学生作业或替代教师评价。",
                "dependencies": "见原包说明；本轮未安装。涉及外部库、CLI、模型、硬件或账号时，部署前必须固定版本并单独审批。",
                "risk": restrictions_for(grade, hits, name),
                "verification": "静态三级验证：读取入口、枚举包结构、扫描脚本/依赖/网络/凭据/写入；未运行。",
                "priority": priority_for(group, name),
                "related": related_for(name),
                "package_files": len(files),
                "script_files": script_count,
                "binary_files": binary_count,
                "line_count": line_count,
                "domains": domains,
                "security_grade": grade,
                "admission_form": admissions,
                "adapt_keep": keep,
                "adapt_strip": strip,
                "executable_behavior": executable_behavior,
                "network_data_behavior": network_behavior,
                "security_restrictions": restrictions_for(grade, hits, name),
                "security_evidence": evidence_rel,
                "static_hits": hits,
            })

    group_order = {g: i for i, g in enumerate(GROUP_MAJORS, start=1)}
    platform_order = {"Gitee": 1, "GitLab": 2, "GitHub": 3, "GitHub（Hugging Face 官方上游）": 4}
    records.sort(key=lambda r: (group_order[r["primary_group"]], platform_order.get(r["platform"], 9), r["repo"], r["name"], r["skill_path"]))
    for idx, record in enumerate(records, start=1):
        record["id"] = f"DISC-0809-{idx:04d}"
    same_name = {}
    for record in records:
        same_name.setdefault(record["name"], []).append(record)
    for name, variants in same_name.items():
        if len(variants) > 1:
            sources = "、".join(f"{item['repo']}（{item['security_grade']}）" for item in variants)
            for item in variants:
                item["related"] = f"同名不同上游变体，均保留用于比较：{sources}。部署时只能选择一个作为默认触发项。"

    out_json = ROOT / "03_候选池" / "deduplicated" / "0809_computer_science.json"
    out_json.write_text(json.dumps({
        "discipline": "0809 计算机类",
        "audit_date": AUDIT_DATE,
        "candidate_count": len(records),
        "security_counts": dict(Counter(r["security_grade"] for r in records)),
        "platform_counts": dict(Counter(r["platform"] for r in records)),
        "group_counts": dict(Counter(r["primary_group"] for r in records)),
        "records": records,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    audit_json = ROOT / "04_验证记录" / "2026-08-07-0809计算机类静态安全审查.json"
    audit_json.write_text(json.dumps({"snapshots": snapshot_index, "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# 0809 计算机类 Skill 静态安全审查",
        "",
        f"审查日期：{AUDIT_DATE}",
        "",
        "## 结论边界",
        "",
        "本记录仅基于固定提交中的公开源码、说明、脚本、依赖和资源做静态审查；未安装、未运行、未输入真实凭据，也未访问校内数据。SA/SB 表示原包可在相应限制下进入候选库；SB-A 只允许抽取并重写为适配版，原包不得直接安装。",
        "",
        "## 汇总",
        "",
        f"- 正式候选：{len(records)}",
    ]
    for grade, count in sorted(Counter(r["security_grade"] for r in records).items()):
        md.append(f"- {grade}：{count}")
    md += ["", "## 快速索引", "", "| ID | Skill | 来源 | 等级 | 准入形态 | 证据 |", "|---|---|---|---|---|---|"]
    for r in records:
        anchor = f"{r['id'].lower()}-{re.sub(r'[^a-z0-9-]+', '-', r['name'].lower())}"
        md.append(f"| {r['id']} | {r['cn_name']} / `{r['name']}` | {r['platform']} · {r['repo']} | {r['security_grade']} | {r['admission_form']} | [下文](#{anchor}) |")
    md += ["", "## 逐项记录", ""]
    for r in records:
        md += [
            f"### {r['id']} {r['cn_name']}（`{r['name']}`）",
            "",
            f"- 来源：{r['platform']} · [{r['repo']}]({r['repo_url']})",
            f"- 固定版本：`{r['review_commit']}`（{r['review_commit_date']}）",
            f"- 入口：[{r['skill_path']}]({r['skill_url']})",
            f"- 许可证：{r['license']}；包内 {r['package_files']} 个文件、{r['script_files']} 个脚本、{r['binary_files']} 个非文本资源、约 {r['line_count']} 行可读文本",
            f"- 功能：{r['summary']}",
            f"- 原说明摘要：{r['original_description'] or '入口未提供独立 description，已按正文核对功能。'}",
            f"- 可执行行为：{r['executable_behavior']}",
            f"- 网络与数据：{r['network_data_behavior']}",
            f"- 静态结论：**{r['security_grade']} · {r['admission_form']}**",
            f"- 限制：{r['security_restrictions']}",
            f"- 适配保留：{r['adapt_keep']}",
            f"- 适配剥离：{r['adapt_strip']}",
            f"- 适用专业：{'、'.join(r['majors'])}",
            "",
        ]
    audit_md = ROOT / "04_验证记录" / "2026-08-07-0809计算机类静态安全审查.md"
    audit_md.write_text("\n".join(md), encoding="utf-8")

    snapshot_md = [
        "# 0809 计算机类源码快照索引", "",
        "本目录只保存本轮审查所需的稀疏源码快照。`.git` 保留上游提交与来源；候选脚本从未执行。", "",
        "| 快照 | 平台 | 上游 | 固定提交 | 提交日期 | 许可证 |", "|---|---|---|---|---|---|",
    ]
    for item in snapshot_index:
        snapshot_md.append(f"| `{item['snapshot']}` | {item['platform']} | [{item['repo']}]({item['repo_url']}) | `{item['commit']}` | {item['commit_date']} | {item['license']} |")
    (ROOT / "02_知识库" / "discipline_pilots" / "0809_计算机类" / "SOURCE_SNAPSHOT_INDEX.md").write_text("\n".join(snapshot_md), encoding="utf-8")

    index_md = [
        "# 0809 计算机类 Skill 索引", "",
        f"正式候选共 {len(records)} 项。此索引用于快速定位；详细安全证据见 `04_验证记录/2026-08-07-0809计算机类静态安全审查.md`。", "",
        "## 按能力群", "",
    ]
    for group in GROUP_MAJORS:
        subset = [r for r in records if r["primary_group"] == group]
        index_md += [f"### {group}（{len(subset)}）", ""]
        for r in subset:
            index_md.append(f"- `{r['id']}` {r['cn_name']} / `{r['name']}` — {r['platform']}，{r['security_grade']}，{r['admission_form']}")
        index_md.append("")
    (ROOT / "02_知识库" / "discipline_pilots" / "0809_计算机类" / "SKILL_INDEX.md").write_text("\n".join(index_md), encoding="utf-8")

    print(json.dumps({
        "records": len(records),
        "security_counts": dict(Counter(r["security_grade"] for r in records)),
        "platform_counts": dict(Counter(r["platform"] for r in records)),
        "group_counts": dict(Counter(r["primary_group"] for r in records)),
        "json": str(out_json),
        "audit": str(audit_md),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
