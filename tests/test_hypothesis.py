# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.
import typing

import pytest
from hypothesis import given
from hypothesis import strategies as st

import grott.extension.ha
from grott.extension.ha import FakeConf


@given(key_name=st.text())
def test_fuzz_is_valid_mqtt_topic(key_name: str) -> None:
    grott.extension.ha.is_valid_mqtt_topic(key_name=key_name)


@given(
    conf=st.builds(FakeConf),
    device=st.text(),
    key=st.text(),
    name=st.one_of(st.none(), st.text()),
)
def test_fuzz_make_payload(
    conf: grott.extension.ha.FakeConf, device: str, key: str, name: typing.Optional[str]
) -> None:
    with pytest.raises(AttributeError):
        grott.extension.ha.make_payload(conf=conf, device=device, key=key, name=name)


@given(
    values=st.dictionaries(
        st.text(),
        st.integers() | st.text(),
    )
)
def test_fuzz_cleanup_values(values: typing.Dict[str, any]) -> None:
    grott.extension.ha.mqtt.cleanup_mqtt_values_field(values=values)
