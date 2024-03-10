from dataclasses import dataclass
from typing import Optional

CONFIG_TOPIC = "homeassistant/{sensor_type}/grott/{device}_{attribut}/config"
STATE_TOPIC = "homeassistant/grott/{device}/state"

MQTT_HOST_CONF_KEY = "ha_mqtt_host"
MQTT_PORT_CONF_KEY = "ha_mqtt_port"
MQTT_USERNAME_CONF_KEY = "ha_mqtt_user"
MQTT_PASSWORD_CONF_KEY = "ha_mqtt_password"
MQTT_RETAIN_CONF_KEY = "ha_mqtt_retain"

# https://www.home-assistant.io/integrations/sensor.mqtt/#expire_after
MQTT_EXPIRE_AFTER = 15 * 60  # 15 minutes


@dataclass
class MQTTConfiguration:
    auth: Optional[dict]
    hostname: str
    port: int
    client_id: str = "Grott - HA"
