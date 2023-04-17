from typing import Any

import httpx

from exception import QuotaExceeded
from response_mapper import IpResponse


class IPyAPI:
    def __init__(self):
        self.__base_url: str = "https://ipapi.co"
        self.__client = httpx.Client()

    def __del__(self):
        self.__client.close()

    def perform_request(self, url: str) -> httpx.Response:
        response = self.__client.get(url)
        if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
            raise QuotaExceeded("API quota exceeded")
        response.raise_for_status()
        return response

    def get_ip_info(self, ip_address: str = None, is_json: bool = True) -> Any | IpResponse:
        if ip_address is not None:
            url = f"{self.__base_url}/{ip_address}/json"
        else:
            url = f"{self.__base_url}/json"
        response = self.perform_request(url=url)
        if is_json:
            return response.json()
        else:
            return IpResponse(**response.json())
