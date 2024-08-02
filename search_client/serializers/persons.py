from pydantic import BaseModel, Field, EmailStr


class Author(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    dai: str | None = Field(default=None)
    isni: str | None = Field(default=None)
    orcid: str | None = Field(default=None)
    external_id: str | None = Field(default=None)
