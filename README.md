# grott-ha-plugin


[![ci](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/egguy/grott-ha-plugin/actions/workflows/ci.yml)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://egguy.github.io/grott-ha-plugin/)
[![pypi version](https://img.shields.io/pypi/v/grott-ha-plugin.svg)](https://pypi.org/project/grott-ha-plugin/)

[//]: # ([![gitpod]&#40;https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat&#41;]&#40;https://gitpod.io/#https://github.com/egguy/grott-ha-plugin&#41;)

Plugin to interface Home Assistant and Grott. Allow auto discovery of the devices on Home Assistant.

Compatibility:

- Python:
    - 3.8
    - 3.9
    - 3.10
    - 3.11
- Grott:
    - 2.7.X
    - 2.8.X

This plugin is tested on linux (and best effort support for macOS and Windows)

## Installation

```bash
pip install grott-ha-plugin
```

## Usage

Once installed you need to add the plugin to the Grott configuration file, `grott.ini`, here an example:

```ini
[extension]
extension=True
extname = grottext.ha
extvar = {"ha_mqtt_host": "192.168.20.2", "ha_mqtt_port": "1883", "ha_mqtt_user": "XXXXX", "ha_mqtt_password": "XXXX"}
```

## Configuration

The extension name (extname) is `grottext.ha`

The extension variable (extvar) is a json string with the following keys:

- `ha_mqtt_host`: the mqtt host of the server used by Home Assistant
- `ha_mqtt_port`: the mqtt port of the server used by Home Assistant
- `ha_mqtt_user`: the mqtt user
- `ha_mqtt_password`: the mqtt password

## Home assistant configuration

On home assistant you need to have the MQTT integration enabled
(docs: https://www.home-assistant.io/integrations/mqtt/) and configured.

You also need a MQTT broker, the recommended one is the mosquitto add-on you can install from the add-on store.

The MQTT broker needs to have a user to allow Grott to connect to it.
(This can be configured in the mosquitto add-on configuration page if you are using it)

## Home assistant add-on

There is a pre-packaged add-on existing for Home Assistant running in Home Assistant Operating System (HAOS).

If you use the mosquitto add-on, the addon will automatically configure Grott and the plugin to use the mosquitto broker.
It's a lot easier.

The add-on is available at:
- [egguy HA addons - stable](https://github.com/egguy/ha-addons): The stable version (**recommended**)
- [egguy HA addons - beta](https://github.com/egguy/ha-addons-beta): The beta version (includes the latest changes in testing)
- [egguy HA addons - edge](https://github.com/egguy/ha-addons-edge/): The edge version (includes the latest changes - **Not recommended for day-to-day usage**)
