from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


# Схема для заявки(отображаемая пользователю)
class ApplicationCreateShema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    FIO: str
    number: PhoneNumber
    email: EmailStr
    info: str = Field(max_length=100)


class ApplicationShema(ApplicationCreateShema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status_info: int
    status: str


# Схема для запроса на создание кода
class AccessCodeCreateSchema(BaseModel):
    role: str
    FIO: str


# Схема для ответа клиенту
class AccessCodeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    role: str
    is_active: bool



# схема для маленькой, миленькой jwtешки
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

