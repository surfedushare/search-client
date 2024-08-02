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
    url: HttpUrl
    hash: str
    type: str
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    title: str
    is_link: bool
    copyright: str
    mime_type: str
    access_rights: str
    video: Video | None = Field(default=None)
    previews: Previews | None = Field(default=None)
