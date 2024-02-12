class CreateInstantVoiceClone:
    """ """

    method = "POST"
    uri = "https://api.play.ht/api/v2/cloned-voices/instant/"
    headers = {"Accept": "application/json", "Content-Type": "multipart/form-data"}
    # one of:
    sample_file: bytes
    sample_file_url: str
    #
    voice_name: str  # form param


class ListClonedVoices:
    """
    response is a url?
    """

    method = "GET"
    uri = "https://api.play.ht/api/v2/cloned-voices"
    headers = {"Accept": "application/json"}


class DeleteClonedVoices:
    """ """

    method = "DELETE"
    uri = "https://api.play.ht/api/v2/cloned-voices/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    voice_id: str = ""
    data = {"voice_id": voice_id}
