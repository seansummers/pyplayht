from enum import StrEnum, auto, unique
from typing import Optional

headers = {"Accept": "application/json", "Content-Type": "application/json"}

ResponseFormat = {
    "audio-mpeg",
    "event-stream",
}
VoiceEngine = {
    "PlayHT1.0",
    "PlayHT2.0",
}


@unique
class Quality(StrEnum):
    draft = auto()
    low = auto()
    medium = auto()
    high = auto()
    premium = auto()


@unique
class OutputFormat(StrEnum):
    mp3 = auto()
    wav = auto()
    ogg = auto()
    flac = auto()
    mulaw = auto()


@unique
class Emotion(StrEnum):
    female_happy = auto()
    female_sad = auto()
    female_angry = auto()
    female_fearful = auto()
    female_disgust = auto()
    female_surprised = auto()
    male_happy = auto()
    male_sad = auto()
    male_angry = auto()
    male_fearful = auto()
    male_disgust = auto()
    male_surprised = auto()


@unique
class GenerateStatus(StrEnum):
    GENERATING = auto()
    COMPLETED = auto()
    ERROR = auto()


class TtsStream:
    """
    Error if not mp3
    """

    request = "POST"
    uri = "https://api.play.ht/api/v2/tts/stream"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json"}
    text: str
    voice: str
    quality: Optional[Quality]
    output_format: Optional[OutputFormat]  # error if not mp3
    speed: Optional[float]  # 0 < _ <= 5.0
    sample_rate: Optional[int]  # 8000 <= _ <= 48000
    seed: Optional[int]  #  0 <= _
    temperature: Optional[float]  # 0 <= _ <= 2
    voice_engine: Optional[VoiceEngine]  # default PlayHT2.0
    emotion: Optional[Emotion]
    voice_guidance: Optional[int]  # 1 <= _ <= 6 for uniqueness
    style_guidance: Optional[int]  # 1 <= _ <= 30 for emotiveness


class GenerateAudioFromText:
    """
    response: 201 Location /api/v2/tts/{id}
    body: same
    """

    method = "POST"
    uri = "https://api.play.ht/api/v2/tts"
    headers = {"Content-Type": "application/json"}
    # and one of
    headers |= {"Accept": "application/json"}  # job data
    headers |= {"Accept": "text/event-stream"}  # progress
    #
    text: str
    voice: str
    q_format: Optional[ResponseFormat]  # or header, but only event-stream
    quality: Optional[Quality]
    output_format: Optional[OutputFormat]
    speed: Optional[float]  # 0 < _ <= 5.0
    sample_rate: Optional[int]  # 8000 <= _ <= 48000
    seed: Optional[int]  #  0 <= _
    temperature: Optional[float]  # 0 <= _ <= 2
    voice_engine: Optional[VoiceEngine]  # default PlayHT2.0
    emotion: Optional[Emotion]
    voice_guidance: Optional[int]  # 1 <= _ <= 6 for uniqueness
    style_guidance: Optional[int]  # 1 <= _ <= 30 for emotiveness


class GetTextToSpeechJobData:
    """ """

    method = "GET"
    uri = "https://api.play.ht/api/v2/tts/{id}"
    headers = {"Content-Type": "application/json"}
    # and one of
    headers |= {"Accept": "application/json"}  # job data
    headers |= {"Accept": "text/event-stream"}  # progress
    headers |= {"Accept": "audio/mpeg"}  # 406 or MP3 bytes
    #
    id: str
    q_format: Optional[ResponseFormat]  # or accept header
