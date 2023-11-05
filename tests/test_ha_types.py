import pytest

from grottext.ha.constants import MQTT_HOST_CONF_KEY, MQTT_PASSWORD_CONF_KEY, MQTT_PORT_CONF_KEY, MQTT_USERNAME_CONF_KEY
from grottext.ha.ha_types import BaseSensor, DiagnosticSensor, to_dict
from grottext.ha.interface import FakeConf
from grottext.ha.mappings import mapping
from grottext.ha.mqtt import make_payload, process_conf

from .conftest import test_key, test_serial


def test_remove_none_value():
    sensor = BaseSensor(name="test")
    assert to_dict(sensor) == {"name": "test"}

    sensor = DiagnosticSensor(name="test", icon="icon_test")
    assert to_dict(sensor) == {"name": "test", "entity_category": "diagnostic", "icon": "icon_test"}


def test_to_dict():
    # test the to_dict function
    res = to_dict(
        BaseSensor(
            "Grott last data push",
            device_class="timestamp",
            value_template="{{value_json.grott_last_push}}",
        )
    )
    assert res["name"] == "Grott last data push"
    assert res["device_class"] == "timestamp"
    assert res["value_template"] == "{{value_json.grott_last_push}}"
    assert len(res.keys()) == 3
    # Even if present in the dataclass should not be serialized
    assert "unit_of_measurement" not in res


def test_manual_divider(fake_config: FakeConf):
    "Test that's the manual value template is not overwritten"
    # Alter the configuration
    value_template = "{{value_json.pvpowerout | float / 10000}}"
    key = "pvpowerout"
    mapping[key].value_template = value_template
    payload = make_payload(fake_config, test_serial, key)
    # Remove the alteration
    mapping[key].value_template = None

    assert payload["value_template"] == value_template


def test_unknown_mapping(fake_config: FakeConf):
    "Test that an unknown mapping still has a good divider"

    fake_config.recorddict[fake_config.layout].update(
        {
            "test": {"value": 290, "length": 4, "type": "num", "divide": 51},
            "test_not_num": {"value": 290, "length": 4, "type": "text", "divide": 51},
        }
    )

    # No mapping should use the raw divider
    payload = make_payload(fake_config, test_serial, "test")
    assert payload["value_template"] == "{{ value_json.test | float / 51 }}"

    # Type not text should return the raw value
    payload = make_payload(fake_config, test_serial, "test_not_num")
    assert payload["value_template"] == "{{ value_json.test_not_num }}"


def test_name_generation(fake_config):
    "Test the output of the name generation"

    # test date {"value" :76, "length" : 10, "type" : "text"},
    payload = make_payload(fake_config, test_serial, test_key)

    assert payload["name"] == "PV Output (Actual)"


def test_name_generation_non_mapped(fake_config):
    "Test the output of the name generation"

    # test date {"value" :76, "length" : 10, "type" : "text"},
    payload = make_payload(fake_config, test_serial, "duck")

    assert payload["name"] == "duck"


def test_process_conf():
    conf = FakeConf()
    try:
        res = process_conf(conf)
        pytest.fail("Should have raised an exception")
    except AttributeError:
        pass

    conf.extvar = {
        MQTT_HOST_CONF_KEY: "localhost",
        MQTT_PORT_CONF_KEY: "1883",
    }
    res = process_conf(conf)
    assert res["hostname"] == "localhost"
    assert res["port"] == 1883
    assert res["client_id"] == "Grott - HA"
    assert res["auth"] is None
    # test with auth
    conf.extvar[MQTT_USERNAME_CONF_KEY] = "user"
    conf.extvar[MQTT_PASSWORD_CONF_KEY] = "pass"
    res = process_conf(conf)
    assert res["auth"] == {"username": "user", "password": "pass"}
