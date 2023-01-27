
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
        self.logger = logging.getLogger(__name__)
        self.actor = self.cbpi.actor.find_by_id(self.props.HeatingActor)
        self.cbpi.notify(title="DEVELOPMENT ONLY", message="The cbpi4-SimulatedSensor plugin should NOT be used in production!", type=NotificationType.WARNING)
        self.logger.warning("the plugin cbpi4-SimulatedSensor should not be installed in a production environment and should only be used in the dev container")

    @action(key="Set Sensor Temp", parameters=[Property.Number(label="setTemp",configurable=True, default_value = 20, description="Please enter desired current temperature")])
    async def settemp(self ,setTemp=20, **kwargs):
        self.temp = float(setTemp)
        clampedValue=clamp(self.temp, -20,230)
        self.value=clampedValue
        self.push_update(self.value)

    async def run(self):
        self.push_update(self.value)
        potentialNewValue = self.value
        while self.running == True:
            Heater = self.cbpi.actor.find_by_id(self.props.HeatingActor)
            HeaterState=Heater.instance.state
            HeaterPower=float(Heater.power)/100
            if HeaterState and HeaterPower > 0 :
                potentialNewValue = round(float(self.value) + HeaterPower*float((self.props.HeatingRate)), 4)
            else:
                potentialNewValue = round(float(self.value) - float(self.props.CoolingRate), 4)
            clampedValue = clamp(potentialNewValue,-20,230)
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
