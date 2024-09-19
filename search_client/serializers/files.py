from datetime import timedelta

from pydantic import BaseModel, Field
from pydantic.networks import HttpUrl

from search_client.serializers.core import EntityStates


class Video(BaseModel):
    embed_url: HttpUrl
    duration: timedelta


class Previews(BaseModel):
    full_size: HttpUrl
    preview: HttpUrl
    preview_small: HttpUrl


class File(BaseModel):
    srn: str
    hash: str
    access_rights: str
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    is_link: bool = Field(default=False)
    url: HttpUrl | None = Field(default=None)
    type: str | None = Field(default=None)
    title: str | None = Field(default=None)
    copyright: str | None = Field(default=None)
    mime_type: str | None = Field(default=None)
    video: Video | None = Field(default=None)
    previews: Previews | None = Field(default=None)
    priority: int = Field(default=0)
