import time

class WaterSensor:

    # required function
    def process(self , data ):

        self.logger.debug("Current State: " + str(self.currentState) )
        self.logger.debug("Last Change  : " + str(self.lastChange) )
        self.logger.debug("State Length : " + str( int( time.time() ) - self.lastChange ) )

        if len( data ) < self.request_points:
            self.logger.warn("Not Enough Data")
            self.currentState = 0
            return 0

        # require all points to indicate dry
        for point in data:

            self.logger.debug(point)

            if int(point['created']) > self.lastDataPoint:
                self.lastDataPoint = int(point['created'])

            if int(point['value']) > self.minLevel:
                if self.currentState:
                    self.lastChange = int( time.time() )
                self.logger.info("Sensor Off")
                self.currentState = 0
                return 0


#------------------------------------------------------------------------------#
#                       Safety Checks before returning On                      #

        # make sure we're on because of steady stream of points
        if (self.lastDataPoint + self.timeSafety ) < int( time.time() ):
            if self.currentState:
                self.lastChange = int( time.time() )
            self.logger.info("Sensor Off")
            self.currentState = 0
            return 0

        #check to ensure we've not been True for too long
        if self.currentState:
            if int( time.time() ) - self.lastChange > self.onSafety:
                raise Exception('Detected Sensor Malfunction: On Too Long')

#                                                                              #
#------------------------------------------------------------------------------#
        self.logger.info("Sensor On")
        if not self.currentState:
            self.lastChange = int( time.time() )

        self.currentState = 1
        return 1

    #required function
    def defaultResponse( self ):
        return 0

    def __init__(self, logger):
            logger.info("INITTIALIZING OBJECT")
            # requred attributes
            self.request_points = 30
            self.request_time   = 60
            self.iterTime       = 1
            self.logger         = logger
            # class specific
            self.minLevel = 300
            self.currentState = 0
            self.lastChange   = int( time.time() )
            self.onSafety = 60
            self.timeSafety = 10
            self.lastDataPoint = 0




