from dataclasses import dataclass
from typing import Optional

from paho.mqtt.publish import multiple, single

from grott.extension.ha.constants import (
    MQTT_HOST_CONF_KEY,
    MQTT_PASSWORD_CONF_KEY,
    MQTT_PORT_CONF_KEY,
    MQTT_USERNAME_CONF_KEY,
)
from grott.extension.ha.ha_types import to_dict
from grott.extension.ha.interface import FakeConf
from grott.extension.ha.mappings import mapping

_client_name = "Grott - HA"


@dataclass
class Device:
    identifiers: list[str]
    name: str
    manufacturer: str


@dataclass
class MQTTConfigPayload:
    name: str
    unique_id: str
    state_topic: str
    device: Device
    value_template: Optional[str]
    state_class: Optional[str] = None
    device_class: Optional[str] = None
    icon: Optional[str] = None
    entity_category: Optional[str] = None
    unit_of_measurement: Optional[str] = None


def is_valid_mqtt_topic(key_name: str) -> bool:
    """Check if the key is a valid mqtt topic

    :param key_name: The value of the key (e.g. "ACDischarWatt")
    :return: True if the key is a valid mqtt topic, False otherwise
    """
    # Character used to bind wildcard topics
    if key_name.startswith("#"):
        return False
    # Character used to bind single level topics
    if key_name.startswith("+"):
        return False
    # should not start or end with /
    if key_name.startswith("/"):
        return False
    if key_name.endswith("/"):
        return False
    # system topics
    if key_name.startswith("$"):
        return False
    return True


def make_payload(conf: FakeConf, device: str, key: str, name: Optional[str] = None) -> dict:
    """Generate a MQTT payload for a sensor

    Use default values to create a sensor payload, then update with custom
    attributes if they exist.
    E.g., unit_of_measurement/total increasing/etc.

    :param conf: The configuration object, used to extract default divider
    :param device: Use the device name as part of the sensor name + device
    :param key: The key of the sensor sent by grott
    :param name: The name of the sensor, if you want something different
    :return: A dictionary with the MQTT configuration payload
    """

    if not device:
        msg = "device is required"
        raise AttributeError(msg)
    if not key:
        msg = "key is required"
        raise AttributeError(msg)
    if not conf.layout:
        msg = "grott config class error"
        raise AttributeError(msg)
    if conf.layout not in conf.recorddict:
        msg = "grott config class error, missing record layout"
        raise AttributeError(msg)

    if name is None:
        name = key

    sensor = mapping.get(key, None)

    value_template = None
    if sensor and sensor.value_template:
        value_template = sensor.value_template
    else:
        # Reuse the existing divide value if available and not existing
        # and apply it to the HA config
        layout = conf.recorddict[conf.layout]
        if key in layout:
            # From grottdata:207, default type is num, also process numx
            register_type = layout[key].get("type", "num")
            # The register is a numercical type
            if register_type in ("num", "numx"):
                # default divide is 1, if not found
                divider = layout[key].get("divide", "1")
                value_template = f"{{{{ value_json.{key} | float / {divider} }}}}"

    if value_template is None:
        value_template = f"{{{{ value_json.{key} }}}}"

    # Default configuration payload
    payload = MQTTConfigPayload(
        name="{name}",
        unique_id=f"grott_{device}_{key}",  # Generate a unique device ID
        state_topic=f"homeassistant/grott/{device}/state",
        device=Device(
            identifiers=[device],  # Group under a device
            name=device,
            manufacturer="GrowWatt",
        ),
        value_template=value_template,
    )

    if sensor is not None:
        # Update the payload with the sensor configuration
        payload.name = sensor.name
        payload.icon = sensor.icon
        payload.state_class = sensor.state_class
        payload.device_class = sensor.device_class
        payload.icon = sensor.icon
        payload.entity_category = sensor.entity_category
        payload.unit_of_measurement = sensor.unit_of_measurement

    # Generate the name of the key, with all the param available
    payload.name = payload.name.format(device=device, name=name, key=key)
    # HA automatically group the sensors if the device name is prepended

    return to_dict(payload)


def process_conf(conf: FakeConf):
    required_params = [
        MQTT_HOST_CONF_KEY,
        MQTT_PORT_CONF_KEY,
    ]
    if not all(param in conf.extvar for param in required_params):
        print("Missing configuration for ha_mqtt")
        raise AttributeError

    if MQTT_USERNAME_CONF_KEY in conf.extvar:
        auth = {
            "username": conf.extvar[MQTT_USERNAME_CONF_KEY],
            "password": conf.extvar[MQTT_PASSWORD_CONF_KEY],
        }
    else:
        auth = None

    # Need to convert the port if passed as a string
    port = conf.extvar[MQTT_PORT_CONF_KEY]
    if isinstance(port, str):
        port = int(port)
    return {
        "client_id": _client_name,
        "auth": auth,
        "hostname": conf.extvar[MQTT_HOST_CONF_KEY],
        "port": port,
    }


def publish_single(conf: FakeConf, topic, payload, *, retain=False):
    conf = process_conf(conf)
    return single(topic, payload=payload, retain=retain, **conf)


def publish_multiple(conf: FakeConf, msgs):
    conf = process_conf(conf)
    return multiple(msgs, **conf)
