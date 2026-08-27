"""Excel 主台账的工作表和稳定校验码定义。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SheetSpec:
    """一个工作表的表对象和按名称解析的列定义。"""

    name: str
    table_name: str
    columns: tuple[str, ...]
    unique_keys: tuple[tuple[str, ...], ...] = ()


CURRENT_SKILL_COLUMNS = (
    "内部标识", "Skill名称", "规范名称", "入库层级", "Canonical source", "固定版本",
    "许可证", "外部联网/API 调用", "远程服务端点", "本地专业软件或运行时依赖",
    "本地脚本/插件接口", "最近核验日期", "验证状态", "验证证据位置",
)

SHEET_SPECS = (
    SheetSpec("当前Skill", "CurrentSkills", CURRENT_SKILL_COLUMNS, (("内部标识",), ("Canonical source",))),
    SheetSpec("来源别名", "SourceAliases", ("别名标识", "内部标识", "来源平台", "来源地址"), (("别名标识",),)),
    SheetSpec("专业任务映射", "ProfessionalTaskMaps", ("映射标识", "内部标识", "专业代码", "专业名称", "专业任务", "输入", "输出", "适用理由", "使用限制", "相关度"), (("映射标识",),)),
    SheetSpec("版本历史", "VersionHistory", ("版本记录标识", "内部标识", "固定版本", "变更日期", "变更摘要", "证据位置"), (("版本记录标识",),)),
    SheetSpec("候选观察", "CandidateObservations", ("观察标识", "候选名称", "Canonical source", "观察状态", "许可证", "记录日期", "原因"), (("观察标识",),)),
    SheetSpec("目录基线", "CatalogBaselines", ("目录版本", "目录名称", "公开地址", "SHA-256", "发布日期", "访问日期"), (("目录版本",),)),
    SheetSpec("来源水位", "SourceWatermarks", ("来源平台", "检索词", "水位时间", "水位标识", "备注"), (("来源平台", "检索词"),)),
    SheetSpec("运行记录", "RunRecords", ("运行标识", "运行类型", "开始时间", "成功完成时间", "状态", "摘要", "快照SHA-256"), (("运行标识",),)),
    SheetSpec("字段说明", "FieldDescriptions", ("工作表", "字段", "必填", "说明"), (("工作表", "字段"),)),
)

EXPECTED_SHEETS = tuple(spec.name for spec in SHEET_SPECS)
SHEET_SPECS_BY_NAME = {spec.name: spec for spec in SHEET_SPECS}

ERROR_DUPLICATE_STABLE_ID = "台账错误-重复稳定标识"
ERROR_DUPLICATE_CANONICAL_SOURCE = "台账错误-重复规范来源"
ERROR_MISSING_FIXED_VERSION = "台账错误-正式条目缺少固定版本"
ERROR_FORMAL_UNKNOWN_LICENSE = "台账错误-正式条目许可证未明确"
ERROR_REMOTE_ENDPOINT_REQUIRED = "台账错误-外部联网缺少远程端点"
ERROR_LOCAL_SOFTWARE_IN_REMOTE_ENDPOINT = "台账错误-本地软件误填远程端点"
