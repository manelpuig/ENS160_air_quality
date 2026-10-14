"""Parser for the text protocol emitted by the ENS160 firmware."""

from dataclasses import asdict, dataclass
import re


_LINE_PATTERN = re.compile(
    r"^(?P<millis>\d+),CH(?P<channel>\d+),"
    r"eCO2=(?P<eco2>\d+),TVOC=(?P<tvoc>\d+),AQI=(?P<aqi>\d+),"
    r"R0=(?P<r0>\d+),R1=(?P<r1>\d+),R2=(?P<r2>\d+),R3=(?P<r3>\d+)$"
)


@dataclass(frozen=True)
class ENS160Reading:
    """One reading from one ENS160 channel."""

    sensor_millis: int
    channel: int
    eco2_ppm: int
    tvoc_ppb: int
    aqi: int
    r0_ohm: int
    r1_ohm: int
    r2_ohm: int
    r3_ohm: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


def parse_reading(line: str) -> ENS160Reading | None:
    """Parse one firmware line, returning ``None`` for non-data messages."""

    match = _LINE_PATTERN.fullmatch(line.strip())
    if match is None:
        return None

    values = {name: int(value) for name, value in match.groupdict().items()}
    return ENS160Reading(
        sensor_millis=values["millis"],
        channel=values["channel"],
        eco2_ppm=values["eco2"],
        tvoc_ppb=values["tvoc"],
        aqi=values["aqi"],
        r0_ohm=values["r0"],
        r1_ohm=values["r1"],
        r2_ohm=values["r2"],
        r3_ohm=values["r3"],
    )
