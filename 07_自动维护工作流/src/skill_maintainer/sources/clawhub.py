"""ClawHub 只读检索适配器。"""

from urllib.parse import quote, urlencode, urlparse

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

    def identity_endpoint(self, identity: str) -> str:
        parsed = urlparse(identity)
        native_id = identity
        if parsed.scheme:
            if parsed.netloc.casefold() != "clawhub.ai":
                raise ValueError("ClawHub identity 必须是原生 ID 或 clawhub.ai 地址")
            native_id = parsed.path.rstrip("/").split("/")[-1]
        if not native_id:
            raise ValueError("ClawHub identity 不能为空")
        return f"https://clawhub.ai/api/v1/skills/{quote(native_id, safe='')}"
