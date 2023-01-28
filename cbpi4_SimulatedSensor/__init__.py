
# -*- coding: utf-8 -*-
from email import message
import os
import datetime
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.dataclasses import NotificationType

@parameters([Property.Number(label="HeatingRate", default_value=0.1, description="Simulated: heating rate per second (decimal seperator is a dot and float can be negative to simulate a cooling actor)"), 
             Property.Number(label="CoolingRate", default_value=0.01, description="Simulated: cooling rate per second (decimal seperator is a dot and float can be negative to simulate a cooling actor)"),
             Property.Number(label="StartTemp", default_value=20.0, description="Starting Tempperature (decimal seperator is a dot)"),
             Property.Actor(label="HeatingActor", description="the actor that will result in the simulated temperature to rise (or fall)."),
             Property.Select(label="LogSimulatedSensor",options=["Yes","No"], description="on the setting (Yes) the simulated sensor will be logged as well. On the setting (No) there wont be any logging for this simulated sensor.")])
class SimulatedSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(SimulatedSensor, self).__init__(cbpi, id, props)
        self.value = float(self.props.get("StartTemp",20))
        self.running = True
        self.actionvalue=None
        self.logger = logging.getLogger(__name__)
        self.actorid=self.props.HeatingActor
        self.HeatingRate=float(self.props.get("HeatingRate",0.1))
        self.CoolingRate=float(self.props.get("CoolingRate",0.01))

        self.cbpi.notify(title="DEVELOPMENT ONLY", message="The cbpi4-SimulatedSensor plugin should NOT be used in production!", type=NotificationType.WARNING)
        self.logger.warning("the plugin cbpi4-SimulatedSensor should not be installed in a production environment and should only be used in the dev container")

    @action(key="Set Sensor Temp", parameters=[Property.Number(label="setTemp",configurable=True, default_value = 20, description="Please enter desired current temperature")])
    async def settemp(self ,setTemp=20, **kwargs):
        self.temp = float(setTemp)
        clampedValue=clamp(self.temp, -20,230)
        self.actionvalue=clampedValue
        self.push_update(self.value)

    async def get_actor_details(self):
        HeaterState=self.HeatingActor.instance.state
        HeaterPower=float(self.HeatingActor.power)/100
        HeaterData={'state': HeaterState, 'power':HeaterPower}
        return HeaterState, HeaterPower

    async def run(self):
        self.push_update(self.value)
        potentialNewValue = self.value
        self.HeatingActor=self.cbpi.actor.find_by_id(self.actorid)
        logging.info(self.HeatingActor)
        while self.running == True:
            HeaterState, HeaterPower = await self.get_actor_details()
            #logging.warning(HeaterState)
            #logging.warning(HeaterPower)

            if self.actionvalue is not None:
                self.value=self.actionvalue
                self.actionvalue=None
            if (HeaterState==True) and (HeaterPower > 0) :
                logging.info("Heating")
                potentialNewValue = round((float(self.value) + HeaterPower*self.HeatingRate), 8)
            else:
                logging.info("Cooling")
                potentialNewValue = round((float(self.value) - self.CoolingRate), 8)
            clampedValue = clamp(potentialNewValue,-20,230)
            logging.info(clampedValue)
            if clampedValue != self.value :
                self.value = round(clampedValue,3)
                self.push_update(self.value)
                if self.props.get("LogSimulatedSensor", "Yes") == "Yes":
                    self.log_data(self.value)
            await asyncio.sleep(1)
    
    def get_state(self):
        return dict(value=self.value)
    
def clamp(n : float, minn : float, maxn : float):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

def setup(cbpi):
    cbpi.plugin.register("SimulatedSensor", SimulatedSensor)
    pass
