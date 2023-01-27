# cbpi4-SimulatedSensor

**USE AT YOUR OWN RISK!**

**This simulated sensor should never be used in a production environment.**

this simulated sensor will have a value dependent of an actor. the value will increase by a configurable amount if the actor is currently heating (on) and if the actor is not heating (is off) the value will decrease by a configurable amount.

This Plugin should be used very carefully. While using this plugin you should never connect a real heating actor. With improper use of this plugin you can case a real mess and demages. I am not responsible for demages caused by using this plugin.

I use this to try and test specific functions in plugin development where i need logical temperature changes on sensors.

this plugin can be installed via ´pip install cbpi4-SimulatedSensor´


### Changelog:

- 27.01.23: (0.0.3) Added default Starttemp value to sensor config and added action to set sensor temp from dashboard. Added Power dependent temp increase for PID logic simulation.

