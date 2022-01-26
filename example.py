"""Get the data from a WebThing."""
import asyncio

import aiohttp

from webthing_ws import WebThing

URL = "http://localhost"
PORT = 8888


async def main():
    """Sample code to retrieve information and the data from a WebThing."""
    async with aiohttp.ClientSession() as session:
        thing = WebThing(URL, session, port=PORT)

        # Get the WebThing's description.
        await thing.get_description()
        print("WebThing ID:", thing.description.id)
        print("WebThing title:", thing.description.title)
        print("WebThing description:", thing.description.description)
        print("WebThing type:", thing.description.type)

        # Print the state of a WebThing
        await thing.get_states()
        print("WebThing states:", thing.states)

        # Start the WebSocket consumer and print the sensor value of a WebThing sensor
        print("Sensor values:")
        await thing.start_websocket_consumer()


if __name__ == "__main__":
    asyncio.run(main())