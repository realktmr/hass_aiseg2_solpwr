"""AiSEG2 integration for Home Assistant."""
from __future__ import annotations

from .const import DOMAIN

async def async_setup_entry(hass, entry):
    """Set up AiSEG2 from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "host": entry.data["host"],
        "username": entry.data["username"],
        "password": entry.data["password"],
    }
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok