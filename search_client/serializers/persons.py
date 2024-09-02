from pydantic import BaseModel, Field, EmailStr


class Contact(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None)


class Author(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None, description="The id of the author in the source system.")
    dai: str | None = Field(default=None)
    isni: str | None = Field(default=None)
    orcid: str | None = Field(default=None)
    is_external: bool = Field(default=False, description="This means external author for the Provider of a Product.")
