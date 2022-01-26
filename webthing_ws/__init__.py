"""A WebThing WebSocket consumer and API client."""
import asyncio
import collections
import json
import logging
import socket

import aiohttp
import async_timeout

from . import exceptions

_LOGGER = logging.getLogger(__name__)


class WebThing:
    """Representation of a WebThing."""

    def __init__(self, url, session, port=80):
        """Initialize the connection to the WebThing."""
        self._session = session
        self.data = None
        self._description = None
        self._properties = None
        self._states = {}
        self.base_url = url
        self.port = port

    async def get_description(self):
        """Get details of a WebThing."""
        try:
            async with async_timeout.timeout(5):
                response = await self._session.get(f"{self.base_url}:{self.port}")

            _LOGGER.info("Response from WebThing: %s", response.status)
            raw_description = await response.json()

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            _LOGGER.error("Can not load data from the WebThing's API")
            raise exceptions.WebThingWsConnectionError

        # Remove the @ in the response from the WebThing
        try:
            raw_description["context"] = raw_description.pop("@context")
            raw_description["type"] = raw_description.pop("@type")
            for _property in raw_description["properties"]:
                raw_description["properties"][_property]["type"] = raw_description[
                    "properties"
                ][_property].pop("@type")
        except KeyError:
            pass

        try:
            self._description = collections.namedtuple(
                "WebThingDescription", raw_description
            )(**raw_description)
            self._properties = collections.namedtuple(
                "WebThingProperties", self._description.properties
            )(**self._description.properties)
        except ValueError:
            pass

    async def get_states(self):
        """Get states of a WebThing from the RESTful API."""
        await self.get_description()

        for entry in self._properties:
            for link in entry["links"]:
                url_part = link["href"]
                webthing_property = url_part.split("/")[-1]

                try:
                    async with async_timeout.timeout(5):
                        response = await self._session.get(
                            f"{self.base_url}:{self.port}{url_part}"
                        )

                    _LOGGER.info("Response from WebThing: %s", response.status)
                    value = await response.json()
                    self._states[webthing_property] = value[webthing_property]
                except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
                    _LOGGER.error("Can not load data from the WebThing's RESTful API")
                    raise exceptions.WebThingWsConnectionError

    async def start_websocket_consumer(self):
        """Start the WebSocket consumer."""
        await self.get_description()

        for entry in self._description.links:
            if entry["rel"] == "alternate" and entry["href"].startswith("ws:"):
                ws_link = entry["href"]

        async with self._session.ws_connect(ws_link) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if hasattr(self._properties, "level"):
                        print(json.loads(msg.data)["data"]["level"])
                    else:
                        await ws.close()

                elif msg.tp == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.tp == aiohttp.WSMsgType.ERROR:
                    break

    @property
    def description(self):
        """Return the description of the WebThing."""
        return self._description

    @property
    def properties(self):
        """Return the properties of the WebThing."""
        return self._properties

    @property
    def states(self):
        """Return the states of the WebThing."""
        return self._states
