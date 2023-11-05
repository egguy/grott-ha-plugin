import json
import traceback
from datetime import datetime, timezone
from typing import Dict, cast

from grott.extension.ha import __version__
from grott.extension.ha.constants import (
    CONFIG_TOPIC,
    MQTT_HOST_CONF_KEY,
    MQTT_PORT_CONF_KEY,
    MQTT_RETAIN_CONF_KEY,
    STATE_TOPIC,
)
from grott.extension.ha.interface import FakeConf
from grott.extension.ha.mqtt import (
    is_valid_mqtt_topic,
    make_payload,
    publish_multiple,
    publish_single,
)

__pv_config: Dict[str, bool] = {}


def grottext(conf: FakeConf, data: str, jsonmsg: str):
    """Allow pushing to HA MQTT bus, with auto discovery"""

    required_params = [
        MQTT_HOST_CONF_KEY,
        MQTT_PORT_CONF_KEY,
    ]
    if not all(param in conf.extvar for param in required_params):
        print("Missing configuration for ha_mqtt")
        return 1

    # Need to decode the json string
    payload = cast(dict, json.loads(jsonmsg))

    if payload.get("buffered") == "yes":
        # Skip buffered message, HA don't support them
        if conf.verbose:
            print("\t - Grott HA - skipped buffered")
        return 5

    device_serial = payload["device"]
    values = payload["values"]

    # Send the last push in UTC with TZ
    dt = datetime.now(timezone.utc)
    # Add a new value to the existing values
    values["grott_last_push"] = dt.isoformat()

    # Layout can be undefined
    if not __pv_config.get(device_serial, False) and getattr(conf, "layout", None):
        configs_payloads = []
        print(f"\tGrott HA {__version__} - creating {device_serial} config in HA, {len(values.keys())} to push")
        for key in values:
            # Prevent creating invalid MQTT topics
            if not is_valid_mqtt_topic(key):
                if conf.verbose:
                    print(f"\t[Grott HA] {__version__} skipped key: {key}")
                continue
            # Generate a configuration payload
            try:
                payload = make_payload(conf, device_serial, key)
            except AttributeError as e:
                print(f"\t[Grott HA] {__version__} error while generating key: {key}, error: {e}")
            if not payload:
                print(f"\t[Grott HA] {__version__} skipped key: {key}")
                continue

            try:
                topic = CONFIG_TOPIC.format(
                    sensor_type="sensor",
                    device=device_serial,
                    attribut=key,
                )
                configs_payloads.append(
                    {
                        "topic": topic,
                        "payload": json.dumps(payload),
                        "retain": True,
                        "qos": 1,
                    }
                )
            except Exception as e:
                print(f"\t - [grott HA] {__version__} Exception while creating new sensor {key}: {e}")
                return 6

        # Create a virtual last_push key to allow tracking when there was the last data transmission

        try:
            key = "grott_last_push"
            payload = make_payload(conf, device_serial, key)
            topic = CONFIG_TOPIC.format(
                sensor_type="sensor",
                device=device_serial,
                attribut=key,
            )
            configs_payloads.append(
                {
                    "topic": topic,
                    "payload": json.dumps(payload),
                    "retain": True,
                    "qos": 1,
                }
            )
        except Exception as e:
            print(f"\t - [grott HA] {__version__} Exception while creating new sensor last push: {e}")
            return 4
        print(f"\tPushing {len(configs_payloads)} configurations payload to HA")
        publish_multiple(conf, configs_payloads)
        print("\tConfigurations pushed")
        # Now it's configured, no need to come back
        __pv_config[device_serial] = True

    if not __pv_config.get(device_serial, False):
        print(f"\t[Grott HA] {__version__} Can't configure device: {device_serial}")
        return 7

    # Push the values to the topic
    retain = conf.extvar.get(MQTT_RETAIN_CONF_KEY, False)
    try:
        publish_single(
            conf,
            STATE_TOPIC.format(device=device_serial),
            json.dumps(values),
            retain=retain,
        )
    except Exception as e:
        print(f"[HA ext] - Exception while publishing - {e}")
        # Reset connection state in case of a problem
        if conf.verbose:
            traceback.print_exc()
        return 2
    return 0
