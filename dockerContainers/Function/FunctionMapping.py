import importlib

from GardenWater import GardenWater
from GardenLight import GardenLight

class FunctionMapping:

    def __init__(self):
        self.functionObjMap = {
            'WATER' : GardenWater,
            'LIGHT' : GardenLight,
        }

