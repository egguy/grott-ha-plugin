from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class BaseSensor:
    name: str
    icon: Optional[str] = None
    value_template: Optional[str] = None
    state_class: Optional[str] = None
    device_class: Optional[str] = None
    unit_of_measurement: Optional[str] = None
    entity_category: Optional[str] = None


@dataclass
class DiagnosticSensor(BaseSensor):
    entity_category: str = "diagnostic"
    icon = "mdi:information-outline"


@dataclass
class MeasurementSensor(BaseSensor):
    state_class: str = "measurement"
    device_class: Optional[str] = None
    unit_of_measurement: Optional[str] = None


@dataclass
class PercentSensor(MeasurementSensor):
    unit_of_measurement: str = "%"


@dataclass
class VoltageSensor(MeasurementSensor):
    device_class: str = "voltage"
    unit_of_measurement: str = "V"


@dataclass
class CurrentSensor(MeasurementSensor):
    device_class: str = "current"
    unit_of_measurement: str = "A"


@dataclass
class PowerSensor(MeasurementSensor):
    device_class: str = "power"
    unit_of_measurement: str = "W"


@dataclass
class FrequencySensor(MeasurementSensor):
    device_class: str = "frequency"
    unit_of_measurement: str = "Hz"


@dataclass
class TemperatureSensor(MeasurementSensor):
    device_class: str = "temperature"
    unit_of_measurement: str = "°C"


@dataclass
class DurationSensor(MeasurementSensor):
    device_class: str = "duration"
    unit_of_measurement: str = "h"


@dataclass
class ApparentPower(MeasurementSensor):
    device_class: str = "apparent_power"
    unit_of_measurement: str = "VA"


@dataclass
class BatteryChargeSensor(MeasurementSensor):
    device_class: str = "battery"
    unit_of_measurement: str = "%"


@dataclass
class EnergySensor(MeasurementSensor):
    state_class: str = "total"
    device_class: str = "energy"
    unit_of_measurement: str = "kWh"


@dataclass
class IncreasingEnergySensor(MeasurementSensor):
    state_class: str = "total_increasing"
    device_class: str = "energy"
    unit_of_measurement: str = "kWh"


def to_dict(obj: Any) -> dict:
    """Convert a dataclass object to dict

    :param obj: The sensor object to convert
    :return: A dictionary representation of the object
    """
    dict_obj = asdict(obj)
    # Remove None values
    return {k: v for k, v in dict_obj.items() if v is not None}
