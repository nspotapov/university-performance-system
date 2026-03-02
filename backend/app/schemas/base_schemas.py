from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass


class BaseCreateSchema(BaseSchema):
    pass


class BaseReadSchema(BaseSchema):
    id: str

    class Config:
        from_attributes = True


class BaseUpdateSchema(BaseSchema):
    pass
