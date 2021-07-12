import logging
import requests 
import voluptuous as vol
from requests.auth import HTTPDigestAuth
from homeassistant.helpers import config_validation as cv
from homeassistant.components.switch import (
    PLATFORM_SCHEMA, 
    SwitchEntity,
)

from .const import (
    CONF_NAME,
    CONF_HOST,
    CONF_PORT,
    CONF_USERNAME,
    CONF_PASSWORD,
)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.string,
        vol.Optional(CONF_NAME, default='e cam switch'): cv.string,
        vol.Optional(CONF_USERNAME, default='admin'): cv.string,
        vol.Optional(CONF_PASSWORD, default='admin'): cv.string,
    }
)
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([testSwitch(hass, config)])
class testSwitch(SwitchEntity):
    def __init__(self, hass, config) -> None:
        super().__init__()
        self._port = config.get(CONF_PORT)
        self._host = config.get(CONF_HOST)
        self._url = 'http://'+ self._host+':'+ self._port
        self._name = config.get(CONF_NAME)
        self._username = config.get(CONF_USERNAME)
        self._password = config.get(CONF_PASSWORD)
        self._hass=hass
        self._state=None
        self.counter=0
    @property
    def is_on(self):
        return self._state == True
    @property
    def state(self):
        return self._state
    @property
    def name(self):
        return self._name
    def turn_on(self):
        if self.counter==0:
            self._state="on"
            self.async_on()
            self.counter=1
        else:
            self._state="off"
            self.async_off()
            self.counter=0
    def turn_off(self):
        self.async_info(self)
    def async_on(self,*args,**kwagrs):
        # _LOGGER.warn("host:%s,port:%s,username:%s,password:%s"%(self._host,self._port,self._username,self._password))
        r=requests.get("http://%s/set_output?rtmp_enable=1"%self._host, auth=HTTPDigestAuth(self._username,self._password))
        # _LOGGER.warn("opening reply:%s"%r.content)
        logging.warning("opening stream statu:%s"%r.text)
    def async_off(self,*args,**kwargs):
        # _LOGGER.warn("host:%s,port:%s,username:%s,password:%s"%(self._host,self._port,self._username,self._password))
        r=requests.get("http://%s/set_output?rtmp_enable=0"%self._host, auth=HTTPDigestAuth(self._username,self._password))
        logging.warning("closing stream statu:%s"%r.text)
        # _LOGGER.warn("closing reply:%s"%r.content)
    def async_info(self,*args,**kwagrs):
        r=requests.get("http://%s/reboot"%self._host, auth=HTTPDigestAuth(self._username,self._password))
        logging.warning("rebooting statu:%s"%r.text)