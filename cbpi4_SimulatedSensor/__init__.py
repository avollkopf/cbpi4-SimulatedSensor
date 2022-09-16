
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
             Property.Actor(label="HeatingActor", description="the actor that will result in the simulated temperature to rise (or fall)."),
             Property.Select(label="LogSimulatedSensor",options=["Yes","No"], description="on the setting (Yes) the simulated sensor will be logged as well. On the setting (No) there wont be any logging for this simulated sensor.")])
class SimulatedSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(SimulatedSensor, self).__init__(cbpi, id, props)
        self.value = 0.0
        self.running = True
        self.logger = logging.getLogger(__name__)
        self.actor = self.cbpi.actor.find_by_id(self.props.HeatingActor)
        self.cbpi.notify(title="DEVELOPMENT ONLY", message="The cbpi4-SimulatedSensor plugin should NOT be used in production!", type=NotificationType.WARNING)
        self.logger.warning("the plugin cbpi4-SimulatedSensor should not be installed in a production environment and should only be used in the dev container")

    async def run(self):
        while self.running == True:
            HeaterState = self.cbpi.actor.find_by_id(self.props.HeatingActor).instance.state
            potentialNewValue = self.value
            if HeaterState :
                potentialNewValue = round(float(self.value) + float(self.props.HeatingRate), 2)
            else:
                potentialNewValue = round(float(self.value) - float(self.props.CoolingRate), 2)
            clampedValue = clamp(potentialNewValue,-20,120)
            if clampedValue != self.value :
                self.value = clampedValue
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