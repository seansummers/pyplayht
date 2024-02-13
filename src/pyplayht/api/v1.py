"""Endpoints that are V1"""

from typing import Optional


class ConvertPlainTextToSpeech:
    """ """

    method = "POST"
    uri = "https://api.play.ht/api/v1/convert"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    content: list[str]
    voice: str  # GET https://api.play.ht/api/v1/getVoices
    title: Optional[str]
    narrationStyle: Optional[str]  # from getVoices
    globalSpeed: Optional[str]  # in "xxx%" format, 20..200
    pronunciations: Optional[list[dict[str, str]]]  # {"Play.ht": "Play dot H T"}
    trimSilence: Optional[bool]
    transcriptionId: Optional[str]  # to update an existing audio file?


class ConvertSsmlToSpeech:
    """
    requires voices of /en-US-.+/
    """

    method = "POST"
    uri = "https://api.play.ht/api/v1/convert/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    ssml: list[str]
    voice: str  # must be r"^en-US-.+$"
    title: Optional[str]
    narrationStyle: Optional[str]  # from getVoices
    globalSpeed: Optional[str]  # in "xxx%" format, 20..200
    pronunciations: Optional[list[dict[str, str]]]  # {"Play.ht": "Play dot H T"}
    trimSilence: Optional[bool]
    transcriptionId: Optional[str]  # to update an existing audio file?


class GetConversionJobStatus:
    """ """

    method = "GET"
    uri = "https://api.play.ht/api/v1/articleStatus?transcriptionId={transcription_id}"
    headers = {"Accept": "application/json"}
    transcription_id: str


class GetAvailableVoices:
    """ """

    method = "GET"
    uri = "https://api.play.ht/api/v1/getVoices"
    headers = {"Accept": "application/json"}
