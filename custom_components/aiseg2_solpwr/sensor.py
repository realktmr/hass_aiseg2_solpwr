import logging
import requests
import re
from requests.auth import HTTPDigestAuth
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

URL_PATH = "/page/electricflow/111"


def get_kw(response, div_id):
    """HTMLから指定div_idの数値を取り出す"""
    try:
        from lxml import html
        root = html.fromstring(response.content)
        text = root.xpath(f'//div[@id="{div_id}"]')[0].text_content()
        match = re.search(r'[\d.]+', text)
        return float(match.group()) if match else 0.0
    except Exception as e:
        _LOGGER.warning("Failed to parse %s: %s", div_id, e)
        return 0.0


async def async_setup_entry(hass, entry, async_add_entities):
    """エントリ設定"""
    host = entry.data["host"]
    username = entry.data["username"]
    password = entry.data["password"]
    url = f"http://{host}{URL_PATH}"

    session = requests.Session()
    auth = HTTPDigestAuth(username, password)

    async_add_entities(
        [
            AiSEG2Sensor(hass,"発電量", url, auth, "g_capacity"),
            AiSEG2Sensor(hass,"消費量", url, auth, "u_capacity"),
            AiSEG2Sensor(hass,"余力", url, auth, None),
        ],
        update_before_add=True,
    )

class AiSEG2Sensor(Entity):
    def __init__(self, hass, name, url, auth, div_id):
        self._name = name
        self._url = url
        self._auth = auth
        self._div_id = div_id
        self._state = None
        self._hass = hass
        self._attr_unique_id = f"aiseg2_{div_id}"
        self._attr_device_info = {
            "identifiers": {("aiseg2", "unique_aiseg2_device")}, # ここで一意のデバイスIDを設定
            "name": "AiSEG2",
            "manufacturer": "Panasonic",
            "model": "AiSEG2",
		}

    @property
    def device_info(self):
        return self._attr_device_info

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "kW"

    def update(self):
        try:
            response = requests.get(self._url, auth=self._auth, timeout=10)
            if response.status_code == 200:
                if self._div_id == "g_capacity":
                    self._generation = get_kw(response, "g_capacity")
                    self._state = self._generation
                elif self._div_id == "u_capacity":
                    self._consumption = get_kw(response, "u_capacity")
                    self._state = self._consumption
                else:
                    # 差し引きは両方を参照
                    gen = get_kw(response, "g_capacity")
                    con = get_kw(response, "u_capacity")
                    self._generation = gen
                    self._consumption = con
                    self._state = gen - con
            else:
                _LOGGER.warning("HTTP error %s from AiSEG2", response.status_code)
        except Exception as e:
            _LOGGER.warning("Error updating AiSEG2 sensor %s: %s", self._name, e)
