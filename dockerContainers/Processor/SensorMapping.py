import importlib

from WaterSensor import WaterSensor
from LightSensor import LightSensor

class SensorMapping:

    def __init__(self):
        self.sensorObjMap = {
            'c55886045a24c2f5179ca7f6d60a69fca046be2005b5a09c6c1726334c81159a' : WaterSensor,
            'ec6b93a141036a83fc36ff6fa327e05ae665c9bb048fe75477006171902ff584' : LightSensor,
        }

