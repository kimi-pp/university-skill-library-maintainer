---
id: GH-03-0023
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "生态中立 / MCP"
source_form: "社区 skill、开源仓库"
compatibility: C
priority: "中"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 本地文献与文档数据库（litdb）

> 使用 litdb 建立并查询本地科研文献与文档数据库。

## 功能说明

提供文献摄取、搜索、文档关联和 MCP 接口，仓库包含测试、构建和详细使用资料。

## 适用对象与场景

- 适用角色：科研人员、研究生、图书馆人员
- 典型场景：个人或课题组文献库、本地全文检索和研究记录
- 功能标签：文献数据库、文档索引、MCP、全文检索、研究资料

## 接入判断

- 兼容等级：C
- 适配建议：部署 litdb 与 MCP 后接入；也可借鉴其数据模型。
- 依赖条件：litdb 软件、数据库和 MCP 服务
- 风险与边界：需要维护本地索引与附件；导入版权受限全文时需遵守许可。
- 关联说明：无

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：检查仓库级 skill 包，共 82 个文件，包含实现、测试、构建和使用资料。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/jkitchin/litdb/blob/main/SKILL.md](https://github.com/jkitchin/litdb/blob/main/SKILL.md)
- 仓库：[jkitchin/litdb](https://github.com/jkitchin/litdb)
- 仓库元数据：83 stars；最近推送 2026-04-07；许可证 MIT（以仓库当前文件为准）
