"""SkillHub 只读检索适配器。"""

from urllib.parse import urlencode

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
