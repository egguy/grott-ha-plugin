import pytest
from grottext.ha.interface import FakeConf
from grottext.ha.mqtt import cleanup_mqtt_values_field, is_valid_mqtt_topic, make_payload


def test_is_valid_mqtt_topic():
    assert is_valid_mqtt_topic("plocaloadr") is True
    assert is_valid_mqtt_topic("#nbusvolt") is False
    assert is_valid_mqtt_topic("/test") is False
    assert is_valid_mqtt_topic("test/") is False
    assert is_valid_mqtt_topic("+test") is False
    assert is_valid_mqtt_topic("$test") is False  # System topic


def test_cleanup_values():
    values = {
        "plocaloadr": 1,
        "epv1today ": 32,
        "#nbusvolt": 2,
        "/test": 3,
        "test/": 4,
        "+test": 5,
        "$test": 6,
    }
    assert cleanup_mqtt_values_field(values) == {
        "plocaloadr": 1,
        "epv1today": 32,
    }


def test_unknown_layout(fake_config: FakeConf):
    "Test that's the manual value template is not overwritten"
    # Alter the configuration
    fake_config.layout = "FAILURE"
    with pytest.raises(AttributeError, match="grott config class error, missing record layout"):
        make_payload(fake_config, "NCO7410", "pvpowerout")
