
import time

class GardenWater():


    def processSensorData( self , data ):
        return data

    def processServerData( self , data ):

        needWaterCount = 0.0

        for device in self.sensorIdent[ self.waterIdent ]:
            self.logger.debug("Device : " + device)
            for value in data[ device ][ self.waterIdent ]:
                self.logger.debug("Value : " + value)
                if int(value):
                    needWaterCount += 1


        if (needWaterCount / len(self.sensorIdent[ self.waterIdent ]) ) < .51:
            self.logger.info(self.functionKey + " Off")
            self.waterOn = False
            return {'WATER' : 0 }

        else:
            print str( (int( time.time() ) - self.waterOnTime) )
            if self.waterOn and (int( time.time() ) - self.waterOnTime) > self.safetyLength:
                self.logger.warn("Safety Off In Progress")
                return {'WATER' : 0 }

            else:
                if not self.waterOn:
                    self.waterOnTime = int( time.time() )

                self.waterOn = True
                self.logger.info(self.functionKey + " ON")
                return {'WATER' : 1 }

    def defaultReturn(self):
        return { self.functionKey : 0 }

    def __init__(self , logger):

        # required
        self.sensorIdent = { 'c55886045a24c2f5179ca7f6d60a69fca046be2005b5a09c6c1726334c81159a' : [
                'ded2ea9e8f028eb7bc301461314fd34fd2f5172947c3dea0e71696f8b8fcd8e6',
                '7b15bcdd9f91d9b8d5558bec3437485011ffe7ba5cf8c7e24e67042363408c45',
                '247c32aad7cac61314f1e2aa8d0faa3299ca3853d4226373864e60a8278f0f6a'
            ]

        }
        self.functionKey  = 'WATER'
        self.logger       = logger
        self.initInVal    = 0
        self.waterOn      = 0
        self.waterOnTime  = 0
        self.safetyLength = 30


        # internaluse
        self.waterIdent = 'c55886045a24c2f5179ca7f6d60a69fca046be2005b5a09c6c1726334c81159a'
