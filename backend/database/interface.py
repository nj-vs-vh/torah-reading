import abc
import logging
from typing import Optional

from backend.auth import generate_signup_token
from backend.model import SignupToken, StoredUser

logger = logging.getLogger(__name__)


class DatabaseInterface(abc.ABC):
    async def setup(self) -> None:
        logger.info(f"Reading root signup token")
        root_signup_token = await self.get_root_signup_token()
        if root_signup_token is None:
            root_signup_token = await self.save_signup_token(
                SignupToken(creator_username=None, token=generate_signup_token())
            )
        logger.info(f"Root signup token: {root_signup_token}")

    # user management

    @abc.abstractmethod
    async def lookup_user(self, username: str) -> Optional[StoredUser]:
        ...

    @abc.abstractmethod
    async def save_user(self, user: StoredUser) -> StoredUser:
        ...

    # signup token management

    async def get_root_signup_token(self) -> Optional[SignupToken]:
        return await self.get_signup_token(creator_username=None)

    @abc.abstractmethod
    async def lookup_signup_token(self, token: str) -> Optional[SignupToken]:
        ...

    @abc.abstractmethod
    async def get_signup_token(self, creator_username: Optional[str]) -> Optional[SignupToken]:
        ...

    @abc.abstractmethod
    async def save_signup_token(self, signup_token: SignupToken) -> SignupToken:
        ...

    # access token management

    @abc.abstractmethod
    async def save_access_token(self, access_token: str, user: StoredUser) -> None:
        ...

    @abc.abstractmethod
    async def delete_access_token(self, access_token: str) -> None:
        ...

    @abc.abstractmethod
    async def authenticate_user(self, access_token: str) -> Optional[StoredUser]:
        ...
