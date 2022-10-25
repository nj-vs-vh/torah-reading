import logging
from typing import Any, Literal, Optional, Type, TypedDict, TypeVar

from aiohttp import web
from pydantic import BaseModel, ValidationError
from pydantic.error_wrappers import display_errors
from pymongo.results import InsertOneResult


logger = logging.getLogger(__name__)


class CommentData(TypedDict):
    anchor_phrase: Optional[str]
    comment: str
    format: Literal["plain", "markdown", "html"]


class VerseData(TypedDict):
    verse: int
    text: dict[str, str]
    comments: dict[str, list[CommentData]]


class ChapterData(TypedDict):
    chapter: int
    verses: list[VerseData]


class ParshaData(TypedDict):
    book: int
    parsha: int
    chapters: list[ChapterData]


T = TypeVar("T", bound=BaseModel)


class PydanticModel(BaseModel):
    class Config:
        extra = "ignore"

    @classmethod
    def from_user_data(cls: Type[T], raw: Any) -> T:
        try:
            return cls.parse_obj(raw)
        except ValidationError as e:
            raise web.HTTPBadRequest(reason=display_errors(e.errors()))


class DbSchemaModel(PydanticModel):
    id: str = "n/a"

    def is_stored(self) -> bool:
        return self.id != "n/a"

    def to_mongo_db(self) -> dict[str, Any]:
        dump = self.dict()
        dump.pop("id", None)
        return dump

    @classmethod
    def from_mongo_db(cls: Type[T], raw: Any) -> T:
        try:
            raw["id"] = str(raw["_id"])  # id field returned by MongoDB
            return cls.parse_obj(raw)
        except ValidationError:
            logger
            raise web.HTTPInternalServerError(reason="damn")

    def inserted_as(self: T, insert_one_result: InsertOneResult) -> T:
        return self.copy(update={"id": str(insert_one_result.inserted_id)})


class SubmittedUserCredentials(PydanticModel):
    class Config:
        min_anystr_length = 3
        max_anystr_length = 128

    username: str
    password: str


class StoredUser(DbSchemaModel):
    username: str
    invited_by_username: Optional[str]
    password_hash: str
    salt: str

    def dict_public(self) -> dict[str, str]:
        return self.dict(exclude={"password_hash", "salt"})


class SignupToken(DbSchemaModel):
    creator_username: Optional[str]
    token: str
