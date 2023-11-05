from grott.extension.ha import is_valid_mqtt_topic


def test_is_valid_mqtt_topic():
    assert is_valid_mqtt_topic("plocaloadr") is True
    assert is_valid_mqtt_topic("#nbusvolt") is False
    assert is_valid_mqtt_topic("/test") is False
    assert is_valid_mqtt_topic("test/") is False
    assert is_valid_mqtt_topic("+test") is False
    assert is_valid_mqtt_topic("$test") is False  # System topic

