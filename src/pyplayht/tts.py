"""gPRC Tts Client(s)"""

from .api_pb2 import TtsRequest

"""Authentication for Play.HT API"""
from .logging_config import log_call, logging

logger = logging.getLogger(__name__)

from dataclasses import asdict, dataclass, field
from random import choice, randint
from typing import Iterable

from grpc import (
    Channel,
    Compression,
    experimental,
    secure_channel,
    ssl_channel_credentials,
)

from .auth import Session

__all__ = [
    "GrpcTts",
    "HyperParameters",
    "JobParameters",
    "TtsParams",
    "Format",
    "Quality",
]

ASYNC_OPTIONS = ()
SYNC_OPTIONS = ((experimental.ChannelOptions.SingleThreadedUnaryStream, 1),)
VOICES = (
    "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    "s3://peregrine-voices/oliver_narrative2_parrot_saad/manifest.json",
)
try:
    import api_pb2 as api
    import api_pb2_grpc as api_grpc
except ImportError:
    from grpc import protos_and_services

    api, api_grpc = protos_and_services(f"{__package__}/api.proto")

Format = api.Format
Quality = api.Quality
TtsParams = api.TtsParams
TtsRequest = api.TtsRequest
TtsResponse = api.TtsResponse
TtsStub = api_grpc.TtsStub
Tts = api_grpc.Tts


@log_call
def tts_seed():
    """Generate a seed for TtsParams"""
    return randint(0, 2**31)


@dataclass
class HyperParameters:
    """HyperParameter subset of TtsParams."""

    seed: int = field(default=None)
    temperature: float = field(default=None)
    top_p: float = field(default=None)
    voice_guidance: float = field(default=None)
    text_guidance: float = field(default=None)

    @staticmethod
    @log_call(include_result=False)
    def default(**kwargs: [str, int | float]) -> TtsParams:
        """Return default settings, with optional overrides."""
        return TtsParams(**(asdict(HyperParameters(seed=tts_seed())) | kwargs))

    @staticmethod
    @log_call(include_result=False)
    def default_documented(**kwargs: [str, int | float]) -> TtsParams:
        """Return default settings as documented, with optional overrides."""
        return TtsParams(
            **asdict(HyperParameters(seed=tts_seed(), temperature=0.6, top_p=1.0))
            | kwargs
        )


@dataclass
class JobParameters:
    """JobParameter subset of TtsParams."""

    voice: str = field(default=None)
    quality: Quality = field(default=None)
    format: Format = field(default=None)
    sample_rate: int = field(default=None)
    speed: int = field(default=None)
    other: str = field(default=None)

    @staticmethod
    @log_call(include_result=False)
    def default(**kwargs) -> TtsParams:
        """Return default settings, with optional overrides."""
        return TtsParams(
            **asdict(
                JobParameters(
                    voice=choice(VOICES),
                    quality=Quality.QUALITY_MEDIUM,
                    format=Format.FORMAT_WAV,
                    sample_rate=8000,
                    speed=1,
                )
            )
            | kwargs
        )

    @staticmethod
    @log_call(include_result=False)
    def default_documented(**kwargs) -> TtsParams:
        """Return default settings as documented, with optional overrides."""
        return TtsParams(
            **asdict(
                JobParameters(
                    voice=VOICES[0],
                    quality=Quality.QUALITY_MEDIUM,
                    format=Format.FORMAT_WAV,
                    sample_rate=24000,
                    speed=1,
                )
            )
            | kwargs
        )


class GrpcTts:
    """Synchronous TTS Client service."""

    channel: Channel
    session: Session
    stub_tts: Tts
    tts_params: TtsParams

    @property
    @log_call(include_result=False)
    def lease_ticket(self) -> bytes:
        """Return the current lease's ticket."""
        return self.session.lease.token

    @property
    @log_call
    def target(self) -> str:
        """Return the current lease's .grpc_addr for the Channel.target"""
        return self.session.lease.grpc_addr

    @log_call(include_args=["options"], include_result=False)
    def __init__(
        self, session: Session = None, *params: TtsParams, options=SYNC_OPTIONS
    ):
        """Synchronous TTS GRPC Client.

        :param session: Grant Session for Authorization
        :param *params: List of TtsParams objects (later overrides earlier)
        :param options: gRPC ChannelOptions
        """
        self.session = session
        self.tts_params = TtsParams()
        for param in params:
            self.tts_params.MergeFrom(param)
        self.channel = secure_channel(
            self.target,
            credentials=ssl_channel_credentials(),
            options=options,
            compression=Compression.Gzip,
        )
        self.stub_tts: Tts = TtsStub(self.channel).Tts

    @classmethod
    @log_call(include_args=["options"], include_result=False)
    def default(
        cls,
        session: Session = None,
        *params: TtsParams,
        options: tuple[tuple[str, int]] = None,
    ) -> "GrpcTts":
        """Create a TTS gRPC client with defaults and optional overrides.

        :param session: Grant Session for Authorization
        :param *params: List of TtsParams objects (later overrides earlier)
        :param options: gRPC ChannelOptions
        """
        session = session or Session.default()
        params = (
            HyperParameters.default(),
            JobParameters.default(),
        ) + (params or ())
        options = options or SYNC_OPTIONS
        return cls(session, *params, options=options)

    @log_call(include_result=False)
    def __call__(self, texts: list[str]) -> Iterable[TtsResponse]:
        """Convert list of text strings to an audio byte stream and push
        audio chunks to a queue.

        :param texts: string to process
        :yield: TtsResponse objects
        """
        self.tts_params.ClearField("text")
        self.tts_params.MergeFrom(TtsParams(text=texts))
        request = TtsRequest(lease=self.lease_ticket, params=self.tts_params)
        # noinspection PyCallingNonCallable
        yield from self.stub_tts(request)
