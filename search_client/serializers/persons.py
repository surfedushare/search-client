from pydantic import BaseModel, Field, EmailStr, model_validator


class Contact(BaseModel):
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.email and not self.external_id:
            raise ValueError("Either email or external_id must be set")
        return self


class Author(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None, description="The id of the author in the source system.")
    dai: str | None = Field(default=None)
    isni: str | None = Field(default=None)
    orcid: str | None = Field(default=None)
    is_external: bool | None = Field(default=None,
                                     description="This means external author for the Provider of a Product.")
