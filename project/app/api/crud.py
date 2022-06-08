# project/app/api/crud.py


from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary

from typing import Union, List


async def get_all() -> List[TextSummary]:
    summaries = await TextSummary.all().values()
    return summaries


async def get(id: int) -> Union[dict, None]:  # returns dict dict or None, some as Optional
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    else:
        return None


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id