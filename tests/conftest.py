# Test section
# In the same file to keep the plugin contained
import pytest

from grott.extension.ha import FakeConf

test_serial = "NCO7410"
test_key = "pvpowerout"
test_layout = "test"


@pytest.fixture(scope="session")
def fake_config() -> FakeConf:
    """Create a fake config with a test layout"""
    conf = FakeConf()
    conf.recorddict = {
                "test": {
                    test_key: {
                        "value": 122,
                        "length": 4,
                        "type": "num",
                    }
                }
            }
    conf.layout = "test"
    conf.extvar = {}
    conf.verbose = True
    return conf
