


class GardenLight():


    def processSensorData( self , data ):
        return data

    def processServerData( self , data ):

        for device in self.sensorIdent[ self.dataTypeIdent ]:
            self.logger.debug("Device: " + device )
            for value in data[ device ][ self.dataTypeIdent ]:
                self.logger.debug("Value: " + value )
                if not int(value):
                    self.logger.info(self.functionKey + " OFF")
                    return { self.functionKey : 0 }

        self.logger.info(self.functionKey + " ON")
        return {self.functionKey : 1 }

    def defaultReturn(self):
        self.logger.warn("Returning Default")
        return { self.functionKey : 1 }

    def __init__(self , logger):

        # required
        self.dataTypeIdent = 'ec6b93a141036a83fc36ff6fa327e05ae665c9bb048fe75477006171902ff584'

        self.sensorIdent = { self.dataTypeIdent : [
                '2bd6a6f557ea6cb77d7b2cc87894011370c20a06753c5f330a9319da2d1bd075'
            ]

        }
        self.functionKey = 'LIGHT'
        self.logger = logger
        self.initInVal = 0


