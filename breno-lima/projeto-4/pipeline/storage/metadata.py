from pydantic import BaseModel


class Metadata(BaseModel):
    company: str
    reference_data: str
