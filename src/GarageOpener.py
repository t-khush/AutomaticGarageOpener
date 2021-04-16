import asyncio
from aiohttp import ClientSession
import pymyq
from pymyq.garagedoor import STATE_OPEN, STATE_CLOSED
import json

async def garage_control(car, openState):
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      file = open('../data/secrets.json',)
      data = json.load(file)
      myq = await pymyq.login(data["myQ_Username"], data["myQ_Password"], websession)
      devices = myq.covers
      door = devices[data[car]]
      if(openState):
          if(door.state == STATE_OPEN):
              print (f"{door.name} is already open")
          else:
              await door.open(wait_for_state=True)
              print (f"{door.name} has been opened")
      else:
          if(door.state == STATE_CLOSED):
              print (f"{door.name} is already closed")
          else:
              await door.close(wait_for_state=True)
              print (f"{door.name} has been closed")



#asyncio.get_event_loop().run_until_complete(garage_control("Camry", False))
