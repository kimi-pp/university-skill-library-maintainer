"""SkillHub 只读检索适配器。"""

from urllib.parse import quote, urlencode, urlparse

from .base import PagedHttpAdapter, Watermark
from ..queries import QueryJob


SKILLHUB = "https://api.skillhub.cn/api/skills"


class SkillHubAdapter(PagedHttpAdapter):
    platform = "SkillHub"

    def search_url(self, job: QueryJob, watermark: Watermark | None, page: int) -> str:
        parameters = {"query": job.query, "page": page, "limit": self.page_size}
        if watermark and watermark.observed_at:
            parameters["updated_after"] = watermark.observed_at.isoformat()
        return f"{SKILLHUB}?{urlencode(parameters)}"

    def identity_endpoint(self, identity: str) -> str:
        parsed = urlparse(identity)
        native_id = identity
        if parsed.scheme:
            if parsed.netloc.casefold() not in {"skillhub.cn", "api.skillhub.cn"}:
                raise ValueError("SkillHub identity 必须是原生 ID 或 skillhub.cn 地址")
            native_id = parsed.path.rstrip("/").split("/")[-1]
        if not native_id:
            raise ValueError("SkillHub identity 不能为空")
        return f"{SKILLHUB}/{quote(native_id, safe='')}"
