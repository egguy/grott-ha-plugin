# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import grott.extension.ha
import typing
from grott.extension.ha import FakeConf
from hypothesis import given, strategies as st



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
    try:
        grott.extension.ha.make_payload(conf=conf, device=device, key=key, name=name)
    except AttributeError:
        pass

