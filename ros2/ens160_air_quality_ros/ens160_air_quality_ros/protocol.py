"""Parser for the ENS160 serial protocol."""

from dataclasses import dataclass
import re


PATTERN = re.compile(
    r"^(?P<millis>\d+),CH(?P<channel>\d+),"
    r"eCO2=(?P<eco2>\d+),TVOC=(?P<tvoc>\d+),AQI=(?P<aqi>\d+),"
    r"R0=(?P<r0>\d+),R1=(?P<r1>\d+),R2=(?P<r2>\d+),R3=(?P<r3>\d+)$"
)


@dataclass(frozen=True)
class Reading:
    sensor_millis: int
    channel: int
    eco2_ppm: int
    tvoc_ppb: int
    aqi: int
    resistance_ohm: tuple[int, int, int, int]


def parse_reading(line: str) -> Reading | None:
    match = PATTERN.fullmatch(line.strip())
    if match is None:
        return None
    value = {key: int(item) for key, item in match.groupdict().items()}
    return Reading(
        value["millis"],
        value["channel"],
        value["eco2"],
        value["tvoc"],
        value["aqi"],
        (value["r0"], value["r1"], value["r2"], value["r3"]),
    )
