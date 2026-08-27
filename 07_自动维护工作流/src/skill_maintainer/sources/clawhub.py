"""ClawHub 只读检索适配器。"""

from urllib.parse import urlencode

from .base import PagedHttpAdapter, Watermark
from ..queries import QueryJob


CLAWHUB = "https://clawhub.ai/api/v1/search"


class ClawHubAdapter(PagedHttpAdapter):
    platform = "ClawHub"

    def search_url(self, job: QueryJob, watermark: Watermark | None, page: int) -> str:
        parameters = {"q": job.query, "page": page, "limit": self.page_size}
        if watermark and watermark.observed_at:
            parameters["updated_after"] = watermark.observed_at.isoformat()
        return f"{CLAWHUB}?{urlencode(parameters)}"
