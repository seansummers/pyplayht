from enum import StrEnum
from typing import Optional

headers = {"Accept": "application/json", "Content-Type": "application/json"}


class ResponseFormat(StrEnum):
    "audio-mpeg"
    "event-stream"


class Quality(StrEnum):
    draft
    low
    medium
    high
    premium


class OutputFormat(StrEnum):
    mp3
    wav
    ogg
    flac
    mulaw


class VoiceEngine(StrEnum):
    "PlayHT1.0"
    "PlayHT2.0"


class Emotion(StrEnum):
    female_happy
    female_sad
    female_angry
    female_fearful
    female_disgust
    female_surprised
    male_happy
    male_sad
    male_angry
    male_fearful
    male_disgust
    male_surprised


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
