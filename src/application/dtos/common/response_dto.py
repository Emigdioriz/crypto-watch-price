from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore',
        populate_by_name=True,
    )
