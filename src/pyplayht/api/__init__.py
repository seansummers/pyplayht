"""HTTP Client for play.ht REST API"""


class ListPlayHtVoices:
    """ """

    method = "GET"
    uri = "https://api.play.ht/api/v2/voices"
    headers = {"Accept": "application/json"}
