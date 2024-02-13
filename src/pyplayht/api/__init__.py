"""HTTP Client for play.ht REST API"""

__version__ = "0.1.0"


class ListPlayHtVoices:
    """ """

    method = "GET"
    uri = "https://api.play.ht/api/v2/voices"
    headers = {"Accept": "application/json"}
