from dataclasses import dataclass
from typing import Optional


@dataclass
class IpResponse:
    ip: str
    network: str
    version: str
    city: str
    region: str
    region_code: str
    country: str
    country_name: str
    country_code: str
    country_code_iso3: str
    country_capital: str
    country_tld: str
    continent_code: str
    in_eu: bool
    postal: Optional[str]
    latitude: float
    longitude: float
    timezone: str
    utc_offset: str
    country_calling_code: str
    currency: str
    currency_name: str
    languages: str
    country_area: Optional[float]
    country_population: Optional[int]
    asn: str
    org: str
