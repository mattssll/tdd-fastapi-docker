# project/app/models/pydantic.py


from pydantic import BaseModel


# input of post method
class SummaryPayloadSchema(BaseModel):
    url: str


# output of post method
class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
