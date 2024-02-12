"""v2 endpoints"""

from enum import StrEnum
from typing import Optional


class Format(StrEnum):
    "SRT"
    "VRT"
    "JSON"


class TimestampLevel(StrEnum):
    "WORD"
    "SENTENCE"


class TimestampFromAudio:
    """
    Response is a 201 Location /api/v2/transcriptions/{id}
    Body is {job_id, status}
    """

    method = "POST"
    uri = "https://api.play.ht/api/v2/transcriptions"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    tts_job_id: str
    format: Format
    timestamp_level: TimestampLevel
    webhook_url: Optional[str]


class GetTranscriptionsJobData:
    """
    Body is {job_id, status} maybe?
    """

    method = "GET"
    uri = "https://api.play.ht/api/v2/transcriptions/{id}"
    id: str
