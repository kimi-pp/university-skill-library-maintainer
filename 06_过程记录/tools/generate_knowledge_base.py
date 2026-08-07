"""生成本轮知识库条目、分类索引、验证记录和内部落选归档说明。"""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "03_候选池" / "deduplicated"
sys.path.insert(0, str(DATA_DIR))
sys.path.insert(0, str(PROJECT_ROOT / "06_过程记录" / "tools"))

from artifact_generator import records_for_category, write_research_data  # noqa: E402
from catalog_data import AS_OF, CANDIDATES, CATEGORIES, REPOSITORIES  # noqa: E402


write_research_data(DATA_DIR, CANDIDATES, CATEGORIES, REPOSITORIES)

package_evidence = {
    "GH-01-0001": "检查 skill 目录，共 31 个文件，其中 9 个脚本、21 个 references/assets 资源。",
    "GH-01-0002": "检查 skill 目录，共 21 个文件，其中 8 个脚本、12 个 references/assets 资源。",
    "GH-01-0005": "检查 skill 目录，共 4 个文件，其中 1 个脚本、2 个 references/assets 资源。",
    "GH-01-0014": "检查 skill 目录，共 21 个文件，其中 19 个 references/assets 资源。",
    "GH-01-0020": "读取 V4 主入口并检查仓库目录：src/skill 共 55 个文件，其中 references 47 个；src/scripts 共 28 个脚本；仓库递归目录共 468 个文件。",
    "GH-02-0001": "检查 docx skill 目录，共 61 个文件，包含脚本、参考资料与模板资源。",
    "GH-02-0002": "检查 xlsx skill 目录，共 53 个文件，包含脚本、参考资料与模板资源。",
    "GH-02-0003": "检查 pptx skill 目录，共 56 个文件，包含脚本、参考资料与模板资源。",
    "GH-02-0006": "检查 PDF skill 目录，共 4 个文件，除说明外包含辅助资源。",
    "GH-03-0001": "检查 skill 目录，共 17 个文件，其中 5 个脚本、11 个 references/assets 资源。",
    "GH-03-0002": "检查 skill 目录，共 12 个文件，其中 5 个脚本、6 个 references/assets 资源。",
    "GH-03-0022": "检查仓库级 skill 包，共 43 个文件，包含说明、脚本和参考材料。",
    "GH-03-0023": "检查仓库级 skill 包，共 82 个文件，包含实现、测试、构建和使用资料。",
    "GH-03-0024": "检查 skill 目录，共 12 个文件，其中 8 个脚本、3 个 references/assets 资源。",
}


def evidence_for(row):
    """返回可复查的说明/包结构证据，不将其表述为运行验证。"""
    if row["id"] in package_evidence:
        return package_evidence[row["id"]]
    if "package_files" in row:
        return (
            f"读取 {row['line_count']} 行 SKILL.md；检查 skill 范围内 {row['package_files']} 个文件，"
            f"其中脚本 {row['script_files']} 个、references/assets/templates 资源 "
            f"{row['reference_asset_files']} 个。"
        )
    return "已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。"

domain_slugs = {
    "01": "01_学术写作引用与出版",
    "02": "02_文档表格演示文稿与办公自动化",
    "03": "03_文献检索与学术研究",
    "04": "04_图书馆与信息素养",
    "05": "05_编程数学数据分析和可视化",
}

for category, category_name in CATEGORIES.items():
    records = records_for_category(CANDIDATES, category)
    domain_dir = PROJECT_ROOT / "02_知识库" / "functional_domains" / domain_slugs[category]
    skill_dir = domain_dir / "skills"
    skill_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        f"# {category_name}",
        "",
        f"- 本轮范围：GitHub",
        f"- 数据日期：{AS_OF}",
        f"- 入选 skill：{len(records)}",
        "- 说明：仅列入选项；落选项保存在内部归档，不进入最终 Excel 或 DOCX。",
        "- 验证边界：仅读取说明和目录结构；未进行安装、依赖执行或真实任务运行。",
        "",
        "## Skill 索引",
        "",
        "| ID | Skill | 中文定位 | 生态 | 优先级 | 验证 | 条目 |",
        "|---|---|---|---|---|---|---|",
    ]

    for row in records:
        repo_meta = REPOSITORIES[row["repo"]]
        repo_url = f"https://github.com/{row['repo']}"
        skill_url = f"{repo_url}/blob/{repo_meta['branch']}/{row['path']}"
        filename = f"{row['id']}_{row['name'].replace('/', '_')}.md"
        entry_lines = [
            "---",
            f"id: {row['id']}",
            f"category: \"{category_name}\"",
            "source_scope: GitHub",
            "status: 入选",
            f"ecosystem: \"{row['ecosystem']}\"",
            f"source_form: \"{row['form']}\"",
            f"compatibility: {row['compat']}",
            f"priority: \"{row['priority']}\"",
            f"validation: \"{row['verify']}\"",
            f"as_of: {AS_OF}",
            "---",
            "",
            f"# {row['cn']}（{row['name']}）",
            "",
            f"> {row['summary']}",
            "",
            "## 功能说明",
            "",
            row["detail"],
            "",
            "## 适用对象与场景",
            "",
            f"- 适用角色：{row['roles']}",
            f"- 典型场景：{row['scenario']}",
            f"- 功能标签：{row['tags']}",
            "",
            "## 接入判断",
            "",
            f"- 兼容等级：{row['compat']}",
            f"- 适配建议：{row['adapt']}",
            f"- 依赖条件：{row['deps']}",
            f"- 风险与边界：{row['risk']}",
            f"- 关联说明：{row['related'] or '无'}",
            "",
            "## 功能验证",
            "",
            f"- 验证层级：{row['verify']}",
            f"- 验证结果：{evidence_for(row)}",
            "- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。",
            "",
            "## 来源",
            "",
            f"- Skill 地址：[{skill_url}]({skill_url})",
            f"- 仓库：[{row['repo']}]({repo_url})",
            f"- 仓库元数据：{repo_meta['stars']} stars；最近推送 {repo_meta['pushed']}；许可证 {repo_meta['license']}（以仓库当前文件为准）",
            "",
        ]
        (skill_dir / filename).write_text("\n".join(entry_lines), encoding="utf-8")
        index_lines.append(
            f"| {row['id']} | {row['name']} | {row['cn']} | {row['ecosystem']} | {row['priority']} | {row['verify']} | [查看](skills/{filename}) |"
        )

    (domain_dir / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

validation_lines = [
    "# 2026-08-06 GitHub 五类技能功能验证记录",
    "",
    "本记录只证明候选的说明或包内容已经被读取，不证明安装成功、依赖可用或真实任务效果。按照用户规则，本轮未进行最小运行验证。",
    "",
    f"- 入选总数：{len(CANDIDATES)}",
    f"- 二级包内容验证：{sum(row['verify'] == '二级包内容验证' for row in CANDIDATES)}",
    f"- 说明已核验：{sum(row['verify'] == '说明已核验' for row in CANDIDATES)}",
    "- 安装/运行验证：0",
    "",
    "| ID | 分类 | Skill | 验证层级 | 验证证据 |",
    "|---|---|---|---|---|",
]
for row in CANDIDATES:
    evidence = evidence_for(row)
    validation_lines.append(
        f"| {row['id']} | {CATEGORIES[row['cat']]} | {row['name']} | {row['verify']} | {evidence} |"
    )
(PROJECT_ROOT / "04_验证记录" / "2026-08-06-GITHUB五类技能验证总表.md").write_text(
    "\n".join(validation_lines) + "\n", encoding="utf-8"
)

excluded_lines = [
    "# 2026-08-06 GitHub 检索落选归档说明",
    "",
    "本目录仅供内部追溯。落选 skill 不进入任何最终 Excel 或 DOCX。",
    "",
    "## 本轮处理规模",
    "",
    "- 首轮三个分类的 GitHub Code Search 返回 2,600 条命中；各轮分别得到 895、977、597 个唯一 skill 路径。",
    "- 第二轮两个分类先形成 85 个重点路径；只读路径核验发现 1 个失效 OpenClaw 镜像地址并移除，84 个有效候选进入说明与目录检查。",
    "- 各轮数量不可直接视为生态总量，因为检索式、镜像与跨分类功能存在重叠。",
    f"- 去重、聚类和说明核验后，当前保留 {len(CANDIDATES)} 个入选候选。",
    "",
    "## 主要落选原因",
    "",
    "- 同一上游 skill 的镜像、搬运或聚合仓库副本。",
    "- 只有关键词命中，实际功能不属于当次任务限定分类。",
    "- 缺少可读取的 SKILL.md、README 或足够的功能说明。",
    "- 仓库或路径无法稳定定位，或内容仅为占位/示例。",
    "- 与已入选候选功能高度重复，但来源权威性、完整度或可移植性更低。",
    "- 依赖封闭产品或专有环境，且缺乏可合理适配的公开工作流说明。",
    "",
    "## 边界",
    "",
    "本轮没有对落选项做运行验证，也没有把落选项写入交付列表；后续若用户重新限定范围，可从原检索式和本归档标准继续扩展。",
]
(PROJECT_ROOT / "03_候选池" / "excluded" / "2026-08-06-GITHUB落选归档说明.md").write_text(
    "\n".join(excluded_lines) + "\n", encoding="utf-8"
)
