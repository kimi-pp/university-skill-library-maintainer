---
id: GH-04-0021
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Research-Claw / 可移植工作流"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# Figshare 科研资源管理（figshare-api）

> 使用 Figshare API 检索、读取和管理公开研究数据集及文件元数据。

## 功能说明

使用 Figshare API 检索、读取和管理公开研究数据集及文件元数据。 本轮读取了 163 行说明，重点核对了Figshare API Guide、Overview、Authentication、Core Endpoints、articles: Search and Retrieve Articles。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研人员、图书馆人员
- 典型场景：馆藏发现、开放资源检索、知识库建设与服务规划
- 功能标签：Figshare、数据集、研究对象、API

## 接入判断

- 兼容等级：B
- 适配建议：将示例端点、认证方式和输出字段映射到本校图书馆系统；先以只读方式接入。
- 依赖条件：网络；部分功能需要 API 密钥、机构订阅或本地脚本
- 风险与边界：外部接口、馆藏覆盖和访问政策会变化；不得绕过权限或版权限制。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：说明已核验
- 验证结果：读取 163 行 SKILL.md；检查 skill 范围内 1 个文件，其中脚本 0 个、references/assets/templates 资源 0 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/wentorai/research-plugins/blob/main/skills/research/funding/figshare-api/SKILL.md](https://github.com/wentorai/research-plugins/blob/main/skills/research/funding/figshare-api/SKILL.md)
- 仓库：[wentorai/research-plugins](https://github.com/wentorai/research-plugins)
- 仓库元数据：270 stars；最近推送 2026-06-19；许可证 MIT（以仓库当前文件为准）
