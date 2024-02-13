"""Authentication for Play.HT API"""

from functools import cached_property

from .logging_config import log_call, logging

logger = logging.getLogger(__name__)

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from struct import Struct
from typing import Annotated, Any, Callable
from urllib import request

from dotenv import dotenv_values

__all__ = ["Credentials", "Lease", "Session"]

# parse lease freshness (created, duration)
_get_freshness: Callable[[Annotated[bytes, 72]], tuple[int, int]] = Struct(
    ">64x2L"
).unpack


@dataclass
class Credentials:
    """PlayHT Authentication Credentials

    >>> Credentials('id','Bearer key','PLAY_HT_TEST_')
    Credentials(user_id='id', api_key='key', env_prefix='PLAY_HT_TEST_')

    :param user_id: PlayHT User ID
    :param api_key: PlayHT API Key
    :param env_prefix: Prefix for Environment Variables, if loading from the environment (default 'PLAY_HT_')
    """

    user_id: str
    api_key: str
    env_prefix: str = field(default="PLAY_HT_")

    @classmethod
    @log_call(include_result=False, include_args=["user_id", "env_prefix"])
    def default(
        cls, *, user_id: str = None, api_key: str = None, env_prefix="PLAY_HT_"
    ):
        """Create Credentials() with defaults from the environment (or override with keywords)"""
        env_values: dict[str, str | None] = {
            name.removeprefix(env_prefix).lower(): value
            for name, value in dotenv_values().items()
        }
        try:
            user_id = user_id or env_values.get("user_id")
            api_key = (
                (api_key or env_values.get("api_key")).removeprefix("Bearer").strip()
            )
        except AttributeError:
            raise ValueError(
                f"Unable to locate `{env_prefix}USER_ID` or `{env_prefix}API_KEY` in the environment."
            ) from None
        return cls(user_id, api_key, env_prefix)


@dataclass
class Lease:
    """PlayHT API Lease Token

    :param token: Lease Token Bytes
    :key expires: datetime of expiration
    :key grpc_addr: Token API endpoint
    :key epoch: Base UTC time for tokens
    :key meta: Various other (undocumented) keys returned by the Auth Server
    """

    token: bytes = field(init=True, compare=False)
    expires: datetime = field(init=False, compare=True)
    meta: dict[str, Any] = field(init=False, compare=False)
    epoch: datetime = field(
        default_factory=lambda: datetime(2018, 2, 21, 18, 58), init=False, compare=False
    )
    grace_secs: timedelta = field(
        default_factory=lambda: timedelta(seconds=300), compare=False
    )

    @log_call
    def __post_init__(self):
        """Parse the Lease Token to extract grpc_addr and calculate expires"""
        (created, duration), meta = _get_freshness(self.token[:72]), self.token[72:]
        self.expires = (
            self.epoch + timedelta(seconds=created) + timedelta(seconds=duration)
        )
        if self.is_expired():
            raise ValueError("Got an expired lease! Time is wrong somewhere!")

        self.meta = json.loads(meta)

    @cached_property
    @log_call
    def grpc_addr(self) -> str:
        if self.is_premium:
            return self.meta.get("premium_inference_address")
        return self.meta.get("inference_address")

    @cached_property
    @log_call
    def is_premium(self) -> bool:
        return "premium_inference_address" in self.meta

    @log_call
    def is_expired(self) -> bool:
        """Check Lease expiration against current system UTC and with a grade period"""
        return (datetime.now() - self.expires) > self.grace_secs

    @log_call(include_result=False)
    def __call__(self) -> bytes:
        """Return the Lease byte string on calling."""
        if self.is_expired():
            raise ValueError("Lease is expired!")
        return self.token


class Session:
    """Grants session access by authorizing fresh a fresh Lease when needed"""

    timeout = 60

    @log_call
    def __init__(
        self,
        credentials: Credentials,
        url="https://api.play.ht/api/v2/leases",
        timeout=60,
    ):
        """Initialize the Session.

        >>> session = Session(Credentials('id', 'key'), timeout = 59)
        {'X-User-Id': 'id', 'Authorization': 'Bearer key'}
        >>> session.timeout
        59
        >>> session.request.host
        'api.play.ht'
        >>> session.request.get_header('X-user-id')
        'id'

        :param credentials: Grant object with UserId and APIKey (default: load from Environment)
        :param url: Authentication URL (default "https://api.play.ht/api.v2/leases")
        :param timeout: HTTP timeout to wait for a response (default 60)
        """
        self.timeout = timeout
        self.request = request.Request(
            url,
            headers={
                "X-User-Id": credentials.user_id,
                "Authorization": f"Bearer {credentials.api_key.removeprefix('Bearer').strip()}",
            },
            method="POST",
        )
        self.__lease: Lease = None

    @classmethod
    @log_call(include_result=False, include_args=["url", "timeout"])
    def default(
        cls,
        *,
        credentials: Credentials = None,
        url="https://api.play.ht/api/v2/leases",
        timeout=60,
    ):
        """Initialize the Session with defaults (and optional keyword overrides)

        >>> session = Session.default()
        {'X-User-Id': 'id', 'Authorization': 'Bearer key'}
        >>> session.timeout
        59
        >>> session.request.host
        'api.play.ht'
        >>> session.request.get_header('X-user-id')
        'id'

        :param credentials: Grant object with UserId and APIKey (default: load from Environment)
        :param url: Authentication URL (default "https://api.play.ht/api.v2/leases")
        :param timeout: HTTP timeout to wait for a response (default 60)
        """
        credentials = credentials or Credentials.default()
        return cls(credentials, url, timeout)

    @property
    @log_call(include_result=False)
    def lease(self) -> Lease:
        """Return the existing lease or attempt to refresh a new one.

        :return: a Lease instance
        """
        if not self.__lease or self.__lease.is_expired():
            self._refresh()
        return self.__lease

    @log_call
    def _refresh(self):
        """Refresh the lease unconditionally."""
        with request.urlopen(self.request, timeout=self.timeout) as token:
            self.__lease = Lease(token.read())

    @log_call(include_result=False)
    def __call__(self) -> Lease:
        """Returns the lease.

        :return: a Lease instance
        """
        return self.lease


if __name__ == "__main__":
    import doctest

    doctest.testmod()
