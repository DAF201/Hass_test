import voluptuous as vol
import random
from homeassistant.components.camera import (
    PLATFORM_SCHEMA, 
    Camera, 
    SUPPORT_STREAM
)
from homeassistant.const import (
    CONF_NAME, 
    CONF_PASSWORD, 
    CONF_USERNAME, 
    CONF_AUTHENTICATION, 
    HTTP_DIGEST_AUTHENTICATION,
)
from .const import CONF_STREAM_SOURCE,CONF_HOST,CONF_PORT
from homeassistant.helpers import config_validation as cv



PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_STREAM_SOURCE): cv.template,
        vol.Optional(CONF_NAME, default='e cam'): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default="80"): cv.string,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([testcam(hass, config)])


class testcam(Camera):
    def __init__(self, hass, device_info):
        super().__init__()
        self.hass = hass
        self._name = device_info.get(CONF_NAME)
        self._stream_source = device_info.get(CONF_STREAM_SOURCE)
        self._supported_features = SUPPORT_STREAM
        self._host=device_info.get(CONF_HOST)
        self._port=device_info.get(CONF_PORT)
        self._unique_id=self._host+self._port

    @property
    def supported_features(self):
        return self._supported_features

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return 
    async def stream_source(self):
        if self._stream_source==None:
            return None
        else:
            return self._stream_source.async_render(parse_result=False)