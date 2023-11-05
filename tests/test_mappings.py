from grott.extension.ha import FakeConf, make_payload
from grott.extension.ha.ha_types import to_dict
from grott.extension.ha.mappings import mapping
from grott.extension.ha.mqtt import MQTTConfigPayload

from .conftest import test_key, test_serial


def test_generate_payload(fake_config):
    """Test that an auto-generated payload for MQTT configuration"""
    # Override the divider
    fake_config.recorddict["test"][test_key]["divide"] = 10
    payload = make_payload(fake_config, test_serial, test_key)
    print(payload)
    # The default divider for pvpowerout is 10
    assert payload["value_template"] == "{{ value_json.pvpowerout | float / 10 }}"
    assert payload["name"] == "PV Output (Actual)"
    assert payload["unique_id"] == "grott_NCO7410_pvpowerout"
    assert payload["state_class"] == "measurement"
    assert payload["device_class"] == "power"
    assert payload["unit_of_measurement"] == "W"


def test_generate_payload_without_divider(fake_config):
    "Test that an auto-generated payload for MQTT configuration"

    payload = make_payload(fake_config, test_serial, test_key)
    print(payload)
    # The default divider for pvpowerout is 10
    assert payload["value_template"] == "{{ value_json.pvpowerout | float / 10 }}"
    assert payload["name"] == "PV Output (Actual)"
    assert payload["unique_id"] == "grott_NCO7410_pvpowerout"
    assert payload["state_class"] == "measurement"
    assert payload["device_class"] == "power"
    assert payload["unit_of_measurement"] == "W"


def test_all_mapping_cover_config():
    "Test that all the mappings cover the attrib of the MQTTConfiguration"

    fields = MQTTConfigPayload.__dataclass_fields__.keys()
    # load all the mapping, then check the keys are matching the attributes of the MQTTConfiguration
    for key, value in mapping.items():
        # convert the mapping to a dict
        key_mapping = to_dict(value)
        # Check if the MQTTConfigPayload has the attributes
        for k in key_mapping.keys():
            assert k in fields , f"Missing attribute for {key} - {k}"
