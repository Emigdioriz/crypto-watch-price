from uuid import UUID

from pydantic import BaseModel


class GuidResponse(BaseModel):
    id: UUID