from pydantic import BaseModel


class BaseSchema(BaseModel):
    pass


class BaseCreateSchema(BaseSchema):
    pass


class BaseReadSchema(BaseSchema):
    id: int

    class Config:
        from_attributes = True


class BaseUpdateSchema(BaseSchema):
    pass
